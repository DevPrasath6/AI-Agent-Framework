"""Lightweight Kafka wrapper with in-memory fallback for tests.

This module exposes `get_producer` and `get_consumer` factories that
return an object with `send(topic, value)` / `consume()` methods. The
real backend uses `aiokafka` (optional), while tests can use the
`InMemoryBroker` class.
"""
from __future__ import annotations

import asyncio
import json
import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class InMemoryBroker:
    """Simple in-memory publish/subscribe broker for tests.

    Usage:
        broker = InMemoryBroker()
        prod = broker.create_producer()
        cons = broker.create_consumer()
    """

    def __init__(self):
        self._queues: Dict[str, asyncio.Queue] = {}

    def _get_queue(self, topic: str) -> asyncio.Queue:
        if topic not in self._queues:
            self._queues[topic] = asyncio.Queue()
        return self._queues[topic]

    def create_producer(self):
        broker = self

        class Producer:
            async def send(self, topic: str, value: Any) -> None:
                q = broker._get_queue(topic)
                await q.put(value)

        return Producer()

    def create_consumer(self, topic: str):
        broker = self

        class Consumer:
            def __aiter__(self):
                return self

            async def __anext__(self):
                q = broker._get_queue(topic)
                val = await q.get()
                return val

        return Consumer()


# Real aiokafka integration (optional)
try:
    from aiokafka import AIOKafkaProducer, AIOKafkaConsumer  # type: ignore

    async def create_aiokafka_producer(bootstrap_servers: str):
        prod = AIOKafkaProducer(bootstrap_servers=bootstrap_servers)
        await prod.start()

        class Producer:
            async def send(self, topic: str, value: Any):
                if isinstance(value, (dict, list)):
                    value = json.dumps(value).encode("utf-8")
                elif isinstance(value, str):
                    value = value.encode("utf-8")
                await prod.send_and_wait(topic, value)

        return Producer()

    async def create_aiokafka_consumer(bootstrap_servers: str, topic: str):
        cons = AIOKafkaConsumer(topic, bootstrap_servers=bootstrap_servers)
        await cons.start()

        class Consumer:
            def __aiter__(self):
                return self

            async def __anext__(self):
                msg = await cons.getone()
                try:
                    return json.loads(msg.value.decode("utf-8"))
                except Exception:
                    return msg.value

        return Consumer()

    AIOKAFKA_AVAILABLE = True
except Exception:  # pragma: no cover - optional dependency
    AIOKAFKA_AVAILABLE = False


# Factory helpers
_GLOBAL_INMEM_BROKER: Optional[InMemoryBroker] = None


def get_inmemory_broker() -> InMemoryBroker:
    global _GLOBAL_INMEM_BROKER
    if _GLOBAL_INMEM_BROKER is None:
        _GLOBAL_INMEM_BROKER = InMemoryBroker()
    return _GLOBAL_INMEM_BROKER


async def get_producer(backend: str = "inmemory", **kwargs):
    if backend == "aiokafka":
        if not AIOKAFKA_AVAILABLE:
            raise RuntimeError("aiokafka not installed")
        return await create_aiokafka_producer(kwargs.get("bootstrap_servers"))
    return get_inmemory_broker().create_producer()


async def get_consumer(backend: str = "inmemory", topic: str = "default", **kwargs):
    if backend == "aiokafka":
        if not AIOKAFKA_AVAILABLE:
            raise RuntimeError("aiokafka not installed")
        return await create_aiokafka_consumer(kwargs.get("bootstrap_servers"), topic)
    return get_inmemory_broker().create_consumer(topic)
