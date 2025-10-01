"""
Production database adapter with PostgreSQL support.

This module provides PostgreSQL integration for the AI Agent Framework,
replacing the JSON-lines fallback with production-ready database operations.
"""
from __future__ import annotations

import json
import logging
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from contextlib import asynccontextmanager
import asyncio

# Optional database dependencies with graceful fallback
try:
    import asyncpg
    import psycopg2
    from psycopg2 import pool
    DATABASE_AVAILABLE = True
except ImportError:
    asyncpg = None
    psycopg2 = None
    pool = None
    DATABASE_AVAILABLE = False

from src.state_memory.persistence import save_record, read_records

logger = logging.getLogger(__name__)


class PostgreSQLAdapter:
    """Production PostgreSQL adapter for state and memory persistence."""

    def __init__(
        self,
        connection_string: str,
        pool_size: int = 10,
        max_overflow: int = 20,
        async_mode: bool = True
    ):
        self.connection_string = connection_string
        self.pool_size = pool_size
        self.max_overflow = max_overflow
        self.async_mode = async_mode
        self._pool = None
        self._async_pool = None
        self.logger = logging.getLogger(__name__)

    async def initialize(self):
        """Initialize database connection pools."""
        if not DATABASE_AVAILABLE:
            self.logger.warning("Database dependencies not available - falling back to JSON-lines")
            return False

        try:
            if self.async_mode:
                # Create async connection pool
                self._async_pool = await asyncpg.create_pool(
                    self.connection_string,
                    min_size=1,
                    max_size=self.pool_size
                )
            else:
                # Create sync connection pool
                self._pool = psycopg2.pool.ThreadedConnectionPool(
                    1,
                    self.pool_size,
                    self.connection_string
                )

            # Initialize schema
            await self._initialize_schema()
            self.logger.info("PostgreSQL adapter initialized successfully")
            return True

        except Exception as e:
            self.logger.error(f"Failed to initialize PostgreSQL adapter: {e}")
            return False

    async def _initialize_schema(self):
        """Create necessary tables if they don't exist."""
        schema_sql = """
        CREATE TABLE IF NOT EXISTS ai_framework_records (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            table_name VARCHAR(255) NOT NULL,
            data JSONB NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );

        CREATE INDEX IF NOT EXISTS idx_records_table_name
        ON ai_framework_records(table_name);

        CREATE INDEX IF NOT EXISTS idx_records_created_at
        ON ai_framework_records(created_at);

        CREATE INDEX IF NOT EXISTS idx_records_data_gin
        ON ai_framework_records USING GIN (data);

        CREATE TABLE IF NOT EXISTS ai_framework_vector_embeddings (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            record_id UUID REFERENCES ai_framework_records(id) ON DELETE CASCADE,
            embedding VECTOR(1536),  -- Assuming OpenAI embedding dimensions
            metadata JSONB,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );

        CREATE INDEX IF NOT EXISTS idx_embeddings_vector
        ON ai_framework_vector_embeddings USING hnsw (embedding vector_cosine_ops);
        """

        if self.async_mode and self._async_pool:
            async with self._async_pool.acquire() as conn:
                await conn.execute(schema_sql)
        elif self._pool:
            conn = self._pool.getconn()
            try:
                with conn.cursor() as cur:
                    cur.execute(schema_sql)
                    conn.commit()
            finally:
                self._pool.putconn(conn)

    async def save_record(self, table: str, obj: Dict[str, Any]) -> Dict[str, Any]:
        """Save a record to PostgreSQL."""
        if not self._is_available():
            # Fallback to JSON-lines
            return save_record(table, obj)

        # Ensure record has an id
        if "id" not in obj:
            obj["id"] = str(uuid.uuid4())

        try:
            if self.async_mode and self._async_pool:
                async with self._async_pool.acquire() as conn:
                    result = await conn.fetchrow(
                        """
                        INSERT INTO ai_framework_records (id, table_name, data)
                        VALUES ($1, $2, $3)
                        ON CONFLICT (id) DO UPDATE SET
                            data = $3,
                            updated_at = NOW()
                        RETURNING *
                        """,
                        uuid.UUID(obj["id"]), table, json.dumps(obj)
                    )
                    return obj

            elif self._pool:
                conn = self._pool.getconn()
                try:
                    with conn.cursor() as cur:
                        cur.execute(
                            """
                            INSERT INTO ai_framework_records (id, table_name, data)
                            VALUES (%s, %s, %s)
                            ON CONFLICT (id) DO UPDATE SET
                                data = %s,
                                updated_at = NOW()
                            """,
                            (obj["id"], table, json.dumps(obj), json.dumps(obj))
                        )
                        conn.commit()
                        return obj
                finally:
                    self._pool.putconn(conn)

        except Exception as e:
            self.logger.error(f"Failed to save record to PostgreSQL: {e}")
            # Fallback to JSON-lines
            return save_record(table, obj)

    async def read_records(self, table: str, limit: Optional[int] = None, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Read records from PostgreSQL."""
        if not self._is_available():
            # Fallback to JSON-lines
            return read_records(table)

        try:
            query = "SELECT data FROM ai_framework_records WHERE table_name = $1"
            params = [table]

            if filters:
                # Simple JSONB filtering
                for key, value in filters.items():
                    query += f" AND data->>'{key}' = ${len(params) + 1}"
                    params.append(str(value))

            if limit:
                query += f" LIMIT ${len(params) + 1}"
                params.append(limit)

            if self.async_mode and self._async_pool:
                async with self._async_pool.acquire() as conn:
                    rows = await conn.fetch(query, *params)
                    return [json.loads(row['data']) for row in rows]

            elif self._pool:
                conn = self._pool.getconn()
                try:
                    with conn.cursor() as cur:
                        cur.execute(query.replace('$', '%s'), params)
                        rows = cur.fetchall()
                        return [json.loads(row[0]) for row in rows]
                finally:
                    self._pool.putconn(conn)

        except Exception as e:
            self.logger.error(f"Failed to read records from PostgreSQL: {e}")
            # Fallback to JSON-lines
            return read_records(table)

    async def search_records(self, table: str, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search records using PostgreSQL full-text search."""
        if not self._is_available():
            # Fallback to simple JSON-lines search
            records = read_records(table)
            return [r for r in records if query.lower() in str(r).lower()][:limit]

        try:
            search_query = """
            SELECT data, ts_rank(to_tsvector('english', data::text), plainto_tsquery('english', $2)) as rank
            FROM ai_framework_records
            WHERE table_name = $1
            AND to_tsvector('english', data::text) @@ plainto_tsquery('english', $2)
            ORDER BY rank DESC
            LIMIT $3
            """

            if self.async_mode and self._async_pool:
                async with self._async_pool.acquire() as conn:
                    rows = await conn.fetch(search_query, table, query, limit)
                    return [json.loads(row['data']) for row in rows]

            elif self._pool:
                conn = self._pool.getconn()
                try:
                    with conn.cursor() as cur:
                        cur.execute(search_query.replace('$', '%s'), (table, query, limit))
                        rows = cur.fetchall()
                        return [json.loads(row[0]) for row in rows]
                finally:
                    self._pool.putconn(conn)

        except Exception as e:
            self.logger.error(f"Failed to search records in PostgreSQL: {e}")
            return []

    async def store_embedding(
        self,
        record_id: str,
        embedding: List[float],
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Store vector embedding for semantic search."""
        if not self._is_available():
            self.logger.warning("Vector embeddings require PostgreSQL with pgvector extension")
            return False

        try:
            if self.async_mode and self._async_pool:
                async with self._async_pool.acquire() as conn:
                    await conn.execute(
                        """
                        INSERT INTO ai_framework_vector_embeddings (record_id, embedding, metadata)
                        VALUES ($1, $2, $3)
                        """,
                        uuid.UUID(record_id), embedding, json.dumps(metadata or {})
                    )
                    return True

            elif self._pool:
                conn = self._pool.getconn()
                try:
                    with conn.cursor() as cur:
                        cur.execute(
                            """
                            INSERT INTO ai_framework_vector_embeddings (record_id, embedding, metadata)
                            VALUES (%s, %s, %s)
                            """,
                            (record_id, embedding, json.dumps(metadata or {}))
                        )
                        conn.commit()
                        return True
                finally:
                    self._pool.putconn(conn)

        except Exception as e:
            self.logger.error(f"Failed to store embedding: {e}")
            return False

    async def similarity_search(
        self,
        embedding: List[float],
        table: str,
        limit: int = 10,
        threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """Perform semantic similarity search using vector embeddings."""
        if not self._is_available():
            return []

        try:
            search_query = """
            SELECT r.data, 1 - (e.embedding <=> $1) as similarity
            FROM ai_framework_vector_embeddings e
            JOIN ai_framework_records r ON e.record_id = r.id
            WHERE r.table_name = $2
            AND 1 - (e.embedding <=> $1) > $3
            ORDER BY similarity DESC
            LIMIT $4
            """

            if self.async_mode and self._async_pool:
                async with self._async_pool.acquire() as conn:
                    rows = await conn.fetch(search_query, embedding, table, threshold, limit)
                    return [
                        {
                            'data': json.loads(row['data']),
                            'similarity': row['similarity']
                        }
                        for row in rows
                    ]

        except Exception as e:
            self.logger.error(f"Failed to perform similarity search: {e}")
            return []

    def _is_available(self) -> bool:
        """Check if PostgreSQL connection is available."""
        return DATABASE_AVAILABLE and (self._pool is not None or self._async_pool is not None)

    async def close(self):
        """Close database connections."""
        if self._async_pool:
            await self._async_pool.close()
        if self._pool:
            self._pool.closeall()


# Global database adapter instance
_db_adapter: Optional[PostgreSQLAdapter] = None


async def get_database_adapter() -> PostgreSQLAdapter:
    """Get or create the global database adapter."""
    global _db_adapter

    if _db_adapter is None:
        # Try to get connection string from Django settings
        try:
            from django.conf import settings

            # Convert Django database config to PostgreSQL connection string
            db_config = settings.DATABASES.get('default', {})
            if db_config.get('ENGINE') == 'django.db.backends.postgresql':
                connection_string = (
                    f"postgresql://{db_config.get('USER', '')}:"
                    f"{db_config.get('PASSWORD', '')}@"
                    f"{db_config.get('HOST', 'localhost')}:"
                    f"{db_config.get('PORT', 5432)}/"
                    f"{db_config.get('NAME', '')}"
                )

                _db_adapter = PostgreSQLAdapter(connection_string)
                await _db_adapter.initialize()

        except Exception as e:
            logger.warning(f"Failed to initialize PostgreSQL adapter: {e}")

        # If still None, create a fallback adapter
        if _db_adapter is None:
            _db_adapter = PostgreSQLAdapter("postgresql://localhost:5432/ai_framework")

    return _db_adapter


# Async-friendly persistence functions
async def save_record_async(table: str, obj: Dict[str, Any]) -> Dict[str, Any]:
    """Async version of save_record using PostgreSQL adapter."""
    adapter = await get_database_adapter()
    return await adapter.save_record(table, obj)


async def read_records_async(table: str, limit: Optional[int] = None, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """Async version of read_records using PostgreSQL adapter."""
    adapter = await get_database_adapter()
    return await adapter.read_records(table, limit, filters)
