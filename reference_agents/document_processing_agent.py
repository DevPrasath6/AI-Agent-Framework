"""
Document Processing Agent - Reference implementation for document analysis workflows.

This agent demonstrates:
- Multi-format document ingestion
- OCR and text extraction
- Content analysis and summarization
- Metadata extraction
- Document classification
- Integration with Intel OpenVINO for model optimization
"""

import os
import mimetypes
from typing import Any, Dict, List, Optional
from datetime import datetime
from pathlib import Path

from src.core.agent_base import AgentBase, AgentCapability
from src.core.execution_context import ExecutionContext
from src.core.workflow_base import (
    WorkflowDefinition,
    WorkflowStep,
    StepType,
    SimpleDAGWorkflow,
)
from src.tools.llm_tool import LLMTool


class DocumentProcessingAgent(AgentBase):
    """
    Document processing agent for analyzing and extracting information from documents.
    """

    def __init__(
        self,
        name: str = "document_processing_agent",
        llm_config: Optional[Dict[str, Any]] = None,
        ocr_config: Optional[Dict[str, Any]] = None,
        supported_formats: Optional[List[str]] = None,
        output_formats: Optional[List[str]] = None,
        **kwargs,
    ):
        """
        Initialize document processing agent.

        Args:
            name: Agent name
            llm_config: Configuration for LLM tool
            ocr_config: Configuration for OCR processing
            supported_formats: List of supported document formats
            output_formats: List of supported output formats
            **kwargs: Additional agent configuration
        """
        super().__init__(
            name=name,
            description="AI-powered document processing and analysis agent",
            capabilities=[
                AgentCapability.DOCUMENT_ANALYSIS,
                AgentCapability.DATA_EXTRACTION,
                AgentCapability.TEXT_PROCESSING,
                AgentCapability.MULTI_MODAL,
            ],
            **kwargs,
        )

        # Initialize LLM tool for text analysis
        self.llm_tool = LLMTool(name="doc_analysis_llm", **(llm_config or {}))

        # Configuration
        self.supported_formats = supported_formats or [
            "pdf",
            "docx",
            "doc",
            "txt",
            "rtf",
            "html",
            "md",
            "jpg",
            "jpeg",
            "png",
            "tiff",
            "bmp",
        ]
        self.output_formats = output_formats or ["json", "text", "markdown", "html"]
        self.ocr_config = ocr_config or {}

        # Processing statistics
        self.documents_processed = 0
        self.total_pages_processed = 0
        self.processing_errors = 0

        # Document cache for processed documents
        self.document_cache: Dict[str, Dict[str, Any]] = {}

    async def execute(
        self, input_data: Any, context: ExecutionContext
    ) -> Dict[str, Any]:
        """Execute document processing workflow."""
        # Parse document input
        document_info = self._parse_document_input(input_data)

        # Validate document format
        validation_result = await self._validate_document(document_info, context)
        if not validation_result["valid"]:
            return {
                "status": "error",
                "error": validation_result["error"],
                "document_info": document_info,
            }

        # Ingest document
        ingestion_result = await self._ingest_document(document_info, context)

        # Extract text content
        text_extraction_result = await self._extract_text(ingestion_result, context)

        # Analyze document content
        analysis_result = await self._analyze_content(text_extraction_result, context)

        # Extract metadata
        metadata_result = await self._extract_metadata(
            document_info, text_extraction_result, analysis_result, context
        )

        # Generate summary and insights
        summary_result = await self._generate_summary(
            text_extraction_result, analysis_result, context
        )

        # Classify document
        classification_result = await self._classify_document(
            text_extraction_result, analysis_result, context
        )

        # Format output
        formatted_output = await self._format_output(
            document_info,
            text_extraction_result,
            analysis_result,
            metadata_result,
            summary_result,
            classification_result,
            context,
        )

        # Update statistics
        self.documents_processed += 1
        if text_extraction_result.get("page_count"):
            self.total_pages_processed += text_extraction_result["page_count"]

        # Cache processed document
        doc_id = document_info.get("document_id", f"doc_{self.documents_processed}")
        self.document_cache[doc_id] = formatted_output

        return formatted_output

    def _parse_document_input(self, input_data: Any) -> Dict[str, Any]:
        """Parse document input from various formats."""
        if isinstance(input_data, str):
            # Assume it's a file path or URL
            return {
                "source": input_data,
                "source_type": "file_path" if os.path.exists(input_data) else "url",
                "document_id": Path(input_data).stem
                if os.path.exists(input_data)
                else None,
            }
        elif isinstance(input_data, dict):
            return {
                "source": input_data.get(
                    "source", input_data.get("file_path", input_data.get("url"))
                ),
                "source_type": input_data.get("source_type", "unknown"),
                "document_id": input_data.get("document_id"),
                "metadata": input_data.get("metadata", {}),
                "processing_options": input_data.get("processing_options", {}),
            }
        else:
            return {
                "source": str(input_data),
                "source_type": "raw_data",
                "document_id": f"raw_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            }

    async def _validate_document(
        self, document_info: Dict[str, Any], context: ExecutionContext
    ) -> Dict[str, Any]:
        """Validate document format and accessibility."""
        source = document_info.get("source")
        if not source:
            return {"valid": False, "error": "No document source provided"}

        if document_info["source_type"] == "file_path":
            if not os.path.exists(source):
                return {"valid": False, "error": f"File not found: {source}"}

            # Check file format
            file_ext = Path(source).suffix.lower().lstrip(".")
            if file_ext not in self.supported_formats:
                return {
                    "valid": False,
                    "error": f"Unsupported format: {file_ext}. Supported: {self.supported_formats}",
                }

            # Check file size (limit to 100MB for demonstration)
            file_size = os.path.getsize(source)
            if file_size > 100 * 1024 * 1024:
                return {
                    "valid": False,
                    "error": f"File too large: {file_size} bytes (max 100MB)",
                }

        return {
            "valid": True,
            "format": file_ext
            if document_info["source_type"] == "file_path"
            else "unknown",
        }

    async def _ingest_document(
        self, document_info: Dict[str, Any], context: ExecutionContext
    ) -> Dict[str, Any]:
        """Ingest document from various sources."""
        source = document_info["source"]
        source_type = document_info["source_type"]

        try:
            if source_type == "file_path":
                return await self._ingest_from_file(source, context)
            elif source_type == "url":
                return await self._ingest_from_url(source, context)
            elif source_type == "raw_data":
                return await self._ingest_raw_data(source, context)
            else:
                raise ValueError(f"Unsupported source type: {source_type}")

        except Exception as e:
            self.processing_errors += 1
            context.add_error("document_ingestion_error", str(e))
            raise

    async def _ingest_from_file(
        self, file_path: str, context: ExecutionContext
    ) -> Dict[str, Any]:
        """Ingest document from file system."""
        file_path = Path(file_path)

        # Get basic file information
        stat = file_path.stat()
        mime_type, _ = mimetypes.guess_type(str(file_path))

        ingestion_result = {
            "source": str(file_path),
            "file_name": file_path.name,
            "file_size": stat.st_size,
            "mime_type": mime_type,
            "file_extension": file_path.suffix.lower(),
            "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "ingestion_timestamp": datetime.utcnow().isoformat(),
        }

        # Read file content based on type
        if file_path.suffix.lower() in [".txt", ".md", ".html", ".rtf"]:
            # Text-based files
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                ingestion_result["raw_content"] = f.read()
                ingestion_result["content_type"] = "text"
        else:
            # Binary files (PDFs, images, etc.)
            with open(file_path, "rb") as f:
                ingestion_result["raw_content"] = f.read()
                ingestion_result["content_type"] = "binary"

        context.add_intermediate_result("document_ingestion", ingestion_result)
        return ingestion_result

    async def _ingest_from_url(
        self, url: str, context: ExecutionContext
    ) -> Dict[str, Any]:
        """Ingest document from URL (stub implementation)."""
        # This is a stub implementation
        # In practice, you would use aiohttp or similar to fetch the document

        return {
            "source": url,
            "content_type": "url",
            "ingestion_timestamp": datetime.utcnow().isoformat(),
            "raw_content": f"Stub content from URL: {url}",
            "note": "URL ingestion not fully implemented in this demo",
        }

    async def _ingest_raw_data(
        self, raw_data: str, context: ExecutionContext
    ) -> Dict[str, Any]:
        """Ingest raw text data."""
        return {
            "source": "raw_input",
            "content_type": "text",
            "raw_content": raw_data,
            "ingestion_timestamp": datetime.utcnow().isoformat(),
            "file_size": len(raw_data.encode("utf-8")),
        }

    async def _extract_text(
        self, ingestion_result: Dict[str, Any], context: ExecutionContext
    ) -> Dict[str, Any]:
        """Extract text content from ingested document."""
        content_type = ingestion_result["content_type"]
        raw_content = ingestion_result["raw_content"]

        if content_type == "text":
            # Already text, just clean it up
            extracted_text = self._clean_text(raw_content)
            page_count = 1

        elif content_type == "binary":
            # Binary content needs processing
            file_ext = ingestion_result.get("file_extension", "").lower()

            if file_ext == ".pdf":
                extracted_text, page_count = await self._extract_from_pdf(
                    raw_content, context
                )
            elif file_ext in [".jpg", ".jpeg", ".png", ".tiff", ".bmp"]:
                extracted_text, page_count = await self._extract_from_image(
                    raw_content, context
                )
            elif file_ext in [".docx", ".doc"]:
                extracted_text, page_count = await self._extract_from_word(
                    raw_content, context
                )
            else:
                # Fallback: try to decode as text
                try:
                    extracted_text = raw_content.decode("utf-8", errors="ignore")
                    page_count = 1
                except Exception:
                    extracted_text = "Unable to extract text from this document format"
                    page_count = 0
        else:
            extracted_text = str(raw_content)
            page_count = 1

        result = {
            "extracted_text": extracted_text,
            "page_count": page_count,
            "word_count": len(extracted_text.split()) if extracted_text else 0,
            "character_count": len(extracted_text) if extracted_text else 0,
            "extraction_timestamp": datetime.utcnow().isoformat(),
            "extraction_method": self._get_extraction_method(ingestion_result),
        }

        context.add_intermediate_result("text_extraction", result)
        return result

    async def _extract_from_pdf(
        self, pdf_content: bytes, context: ExecutionContext
    ) -> tuple:
        """Extract text from PDF (stub implementation)."""
        # This is a stub implementation
        # In practice, you would use PyPDF2, pdfplumber, or similar

        return (
            f"Extracted text from PDF ({len(pdf_content)} bytes)\n[PDF extraction not fully implemented]",
            1,  # page count
        )

    async def _extract_from_image(
        self, image_content: bytes, context: ExecutionContext
    ) -> tuple:
        """Extract text from image using OCR (stub implementation)."""
        # This is a stub implementation
        # In practice, you would use Tesseract, EasyOCR, or Intel OpenVINO OCR models

        return (
            f"OCR extracted text from image ({len(image_content)} bytes)\n[OCR extraction not fully implemented]",
            1,  # page count
        )

    async def _extract_from_word(
        self, doc_content: bytes, context: ExecutionContext
    ) -> tuple:
        """Extract text from Word document (stub implementation)."""
        # This is a stub implementation
        # In practice, you would use python-docx or similar

        return (
            f"Extracted text from Word document ({len(doc_content)} bytes)\n[Word extraction not fully implemented]",
            1,  # page count
        )

    def _clean_text(self, text: str) -> str:
        """Clean and normalize extracted text."""
        if not text:
            return ""

        # Basic text cleaning
        text = text.strip()
        text = " ".join(text.split())  # Normalize whitespace

        return text

    def _get_extraction_method(self, ingestion_result: Dict[str, Any]) -> str:
        """Determine the extraction method used."""
        content_type = ingestion_result["content_type"]
        file_ext = ingestion_result.get("file_extension", "").lower()

        if content_type == "text":
            return "direct_text"
        elif file_ext == ".pdf":
            return "pdf_extraction"
        elif file_ext in [".jpg", ".jpeg", ".png", ".tiff", ".bmp"]:
            return "ocr"
        elif file_ext in [".docx", ".doc"]:
            return "word_extraction"
        else:
            return "fallback_decode"

    async def _analyze_content(
        self, text_extraction_result: Dict[str, Any], context: ExecutionContext
    ) -> Dict[str, Any]:
        """Analyze extracted text content."""
        extracted_text = text_extraction_result["extracted_text"]

        if not extracted_text or len(extracted_text.strip()) == 0:
            return {
                "status": "no_content",
                "analysis": "No text content available for analysis",
            }

        # Basic content analysis
        analysis = {
            "language_detected": self._detect_language(extracted_text),
            "sentiment": self._analyze_sentiment(extracted_text),
            "key_phrases": self._extract_key_phrases(extracted_text),
            "entities": self._extract_entities(extracted_text),
            "content_structure": self._analyze_structure(extracted_text),
            "readability": self._calculate_readability(extracted_text),
            "analysis_timestamp": datetime.utcnow().isoformat(),
        }

        context.add_intermediate_result("content_analysis", analysis)
        return analysis

    def _detect_language(self, text: str) -> str:
        """Detect document language (simplified implementation)."""
        # Simple language detection based on common words
        english_words = [
            "the",
            "and",
            "is",
            "in",
            "to",
            "of",
            "a",
            "that",
            "it",
            "with",
        ]
        spanish_words = ["el", "la", "de", "que", "y", "en", "un", "es", "se", "no"]
        french_words = ["le", "de", "et", "à", "un", "il", "être", "et", "en", "avoir"]

        text_lower = text.lower()

        english_count = sum(1 for word in english_words if word in text_lower)
        spanish_count = sum(1 for word in spanish_words if word in text_lower)
        french_count = sum(1 for word in french_words if word in text_lower)

        if english_count >= spanish_count and english_count >= french_count:
            return "english"
        elif spanish_count >= french_count:
            return "spanish"
        else:
            return "french" if french_count > 0 else "unknown"

    def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze document sentiment (simplified implementation)."""
        positive_words = [
            "good",
            "great",
            "excellent",
            "amazing",
            "wonderful",
            "positive",
            "success",
        ]
        negative_words = [
            "bad",
            "terrible",
            "awful",
            "horrible",
            "negative",
            "failure",
            "problem",
        ]

        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)

        total_sentiment_words = positive_count + negative_count

        if total_sentiment_words == 0:
            return {"polarity": "neutral", "score": 0.0}

        score = (positive_count - negative_count) / total_sentiment_words

        if score > 0.1:
            polarity = "positive"
        elif score < -0.1:
            polarity = "negative"
        else:
            polarity = "neutral"

        return {
            "polarity": polarity,
            "score": score,
            "positive_words": positive_count,
            "negative_words": negative_count,
        }

    def _extract_key_phrases(self, text: str) -> List[str]:
        """Extract key phrases from text (simplified implementation)."""
        # Very basic key phrase extraction
        words = text.lower().split()
        word_freq = {}

        # Count word frequency (ignore common words)
        stop_words = {
            "the",
            "and",
            "or",
            "but",
            "in",
            "on",
            "at",
            "to",
            "for",
            "of",
            "with",
            "by",
            "a",
            "an",
            "is",
            "are",
            "was",
            "were",
            "be",
            "been",
            "being",
            "have",
            "has",
            "had",
            "do",
            "does",
            "did",
            "will",
            "would",
            "could",
            "should",
        }

        for word in words:
            word = word.strip('.,!?;:"()[]{}')
            if len(word) > 3 and word not in stop_words:
                word_freq[word] = word_freq.get(word, 0) + 1

        # Return top 10 most frequent words as key phrases
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in sorted_words[:10]]

    def _extract_entities(self, text: str) -> List[Dict[str, str]]:
        """Extract named entities (simplified implementation)."""
        # Very basic entity extraction using simple patterns
        import re

        entities = []

        # Email addresses
        email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        emails = re.findall(email_pattern, text)
        for email in emails:
            entities.append({"text": email, "type": "email"})

        # Phone numbers (basic pattern)
        phone_pattern = r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b"
        phones = re.findall(phone_pattern, text)
        for phone in phones:
            entities.append({"text": phone, "type": "phone"})

        # Dates (basic pattern)
        date_pattern = r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b"
        dates = re.findall(date_pattern, text)
        for date in dates:
            entities.append({"text": date, "type": "date"})

        return entities

    def _analyze_structure(self, text: str) -> Dict[str, Any]:
        """Analyze document structure."""
        lines = text.split("\n")

        return {
            "total_lines": len(lines),
            "non_empty_lines": len([line for line in lines if line.strip()]),
            "average_line_length": sum(len(line) for line in lines)
            / max(len(lines), 1),
            "has_headings": any(line.strip().isupper() for line in lines),
            "has_bullet_points": any(
                line.strip().startswith(("•", "-", "*", "1.", "2.")) for line in lines
            ),
        }

    def _calculate_readability(self, text: str) -> Dict[str, Any]:
        """Calculate basic readability metrics."""
        words = text.split()
        sentences = text.split(".")

        if not words or not sentences:
            return {"score": 0, "level": "unreadable"}

        avg_words_per_sentence = len(words) / len(sentences)
        avg_chars_per_word = sum(len(word) for word in words) / len(words)

        # Simple readability score (0-100)
        readability_score = max(
            0, min(100, 100 - (avg_words_per_sentence * 2) - (avg_chars_per_word * 5))
        )

        if readability_score >= 80:
            level = "very_easy"
        elif readability_score >= 60:
            level = "easy"
        elif readability_score >= 40:
            level = "moderate"
        elif readability_score >= 20:
            level = "difficult"
        else:
            level = "very_difficult"

        return {
            "score": readability_score,
            "level": level,
            "avg_words_per_sentence": avg_words_per_sentence,
            "avg_chars_per_word": avg_chars_per_word,
        }

    async def _extract_metadata(
        self,
        document_info: Dict[str, Any],
        text_extraction_result: Dict[str, Any],
        analysis_result: Dict[str, Any],
        context: ExecutionContext,
    ) -> Dict[str, Any]:
        """Extract document metadata."""
        metadata = {
            "document_id": document_info.get("document_id"),
            "source": document_info.get("source"),
            "processing_timestamp": datetime.utcnow().isoformat(),
            "file_info": {
                "name": document_info.get("file_name"),
                "size": document_info.get("file_size"),
                "extension": document_info.get("file_extension"),
                "mime_type": document_info.get("mime_type"),
            },
            "content_metrics": {
                "page_count": text_extraction_result.get("page_count", 0),
                "word_count": text_extraction_result.get("word_count", 0),
                "character_count": text_extraction_result.get("character_count", 0),
                "language": analysis_result.get("language_detected", "unknown"),
            },
            "processing_info": {
                "extraction_method": text_extraction_result.get("extraction_method"),
                "agent_name": self.name,
                "processing_version": "1.0",
            },
        }

        context.add_intermediate_result("metadata_extraction", metadata)
        return metadata

    async def _generate_summary(
        self,
        text_extraction_result: Dict[str, Any],
        analysis_result: Dict[str, Any],
        context: ExecutionContext,
    ) -> Dict[str, Any]:
        """Generate document summary using LLM."""
        extracted_text = text_extraction_result["extracted_text"]

        if not extracted_text or len(extracted_text.strip()) == 0:
            return {
                "summary": "No content available for summarization",
                "key_points": [],
                "summary_length": 0,
            }

        # Use LLM to generate summary
        prompt = f"""Please provide a concise summary of the following document:

Document Content:
{extracted_text[:2000]}...

Please provide:
1. A brief summary (2-3 sentences)
2. Key points (3-5 bullet points)
3. Main topics covered

Format your response as:
SUMMARY: [brief summary]
KEY POINTS:
- [point 1]
- [point 2]
- [point 3]
TOPICS: [main topics]"""

        try:
            llm_response = await self.llm_tool.generate_async(prompt, context)
            summary_text = llm_response.text

            # Parse LLM response
            summary_parts = self._parse_summary_response(summary_text)

        except Exception as e:
            self.logger.error(f"LLM summary generation failed: {e}")
            # Fallback to extractive summary
            summary_parts = self._generate_extractive_summary(extracted_text)

        result = {
            "summary": summary_parts.get("summary", ""),
            "key_points": summary_parts.get("key_points", []),
            "topics": summary_parts.get("topics", []),
            "summary_length": len(summary_parts.get("summary", "")),
            "generation_method": "llm" if "summary" in summary_parts else "extractive",
            "generation_timestamp": datetime.utcnow().isoformat(),
        }

        context.add_intermediate_result("summary_generation", result)
        return result

    def _parse_summary_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM summary response."""
        lines = response.split("\n")
        result = {}
        current_section = None

        for line in lines:
            line = line.strip()
            if line.startswith("SUMMARY:"):
                result["summary"] = line[8:].strip()
            elif line.startswith("KEY POINTS:"):
                current_section = "key_points"
                result["key_points"] = []
            elif line.startswith("TOPICS:"):
                result["topics"] = [topic.strip() for topic in line[7:].split(",")]
            elif line.startswith("-") and current_section == "key_points":
                result["key_points"].append(line[1:].strip())

        return result

    def _generate_extractive_summary(self, text: str) -> Dict[str, Any]:
        """Generate extractive summary as fallback."""
        sentences = text.split(".")

        # Take first 2 sentences as summary
        summary = ". ".join(sentences[:2]).strip()
        if summary and not summary.endswith("."):
            summary += "."

        # Extract key phrases as key points
        key_phrases = self._extract_key_phrases(text)
        key_points = [f"Mentions {phrase}" for phrase in key_phrases[:3]]

        return {"summary": summary, "key_points": key_points, "topics": key_phrases[:5]}

    async def _classify_document(
        self,
        text_extraction_result: Dict[str, Any],
        analysis_result: Dict[str, Any],
        context: ExecutionContext,
    ) -> Dict[str, Any]:
        """Classify document type and category."""
        extracted_text = text_extraction_result["extracted_text"]
        key_phrases = analysis_result.get("key_phrases", [])

        # Simple rule-based classification
        classification = self._rule_based_classification(extracted_text, key_phrases)

        # Confidence scoring
        confidence = self._calculate_classification_confidence(
            extracted_text, classification
        )

        result = {
            "document_type": classification["type"],
            "category": classification["category"],
            "subcategory": classification.get("subcategory"),
            "confidence": confidence,
            "classification_features": classification.get("features", []),
            "classification_timestamp": datetime.utcnow().isoformat(),
        }

        context.add_intermediate_result("document_classification", result)
        return result

    def _rule_based_classification(
        self, text: str, key_phrases: List[str]
    ) -> Dict[str, Any]:
        """Classify document using rule-based approach."""
        text_lower = text.lower()

        # Contract/Legal documents
        if any(
            term in text_lower
            for term in ["contract", "agreement", "terms", "conditions", "legal"]
        ):
            return {
                "type": "legal",
                "category": "contract",
                "features": ["legal_terms", "formal_language"],
            }

        # Financial documents
        if any(
            term in text_lower
            for term in ["invoice", "payment", "financial", "account", "balance"]
        ):
            return {
                "type": "financial",
                "category": "accounting",
                "features": ["financial_terms", "numerical_data"],
            }

        # Technical documentation
        if any(
            term in text_lower
            for term in ["api", "function", "class", "method", "documentation"]
        ):
            return {
                "type": "technical",
                "category": "documentation",
                "features": ["technical_terms", "code_references"],
            }

        # Academic/Research papers
        if any(
            term in text_lower
            for term in [
                "abstract",
                "methodology",
                "conclusion",
                "references",
                "research",
            ]
        ):
            return {
                "type": "academic",
                "category": "research",
                "features": ["academic_structure", "citations"],
            }

        # Reports
        if any(
            term in text_lower
            for term in ["report", "analysis", "findings", "summary", "executive"]
        ):
            return {
                "type": "business",
                "category": "report",
                "features": ["structured_content", "analytical_language"],
            }

        # Default classification
        return {
            "type": "general",
            "category": "document",
            "features": ["general_content"],
        }

    def _calculate_classification_confidence(
        self, text: str, classification: Dict[str, Any]
    ) -> float:
        """Calculate confidence score for classification."""
        # Simple confidence calculation based on feature presence
        features = classification.get("features", [])
        text_lower = text.lower()

        feature_keywords = {
            "legal_terms": ["contract", "agreement", "party", "hereby", "whereas"],
            "financial_terms": ["amount", "payment", "invoice", "account", "balance"],
            "technical_terms": ["function", "method", "class", "variable", "parameter"],
            "academic_structure": [
                "abstract",
                "introduction",
                "methodology",
                "conclusion",
            ],
            "formal_language": ["shall", "whereas", "hereby", "therefore", "pursuant"],
        }

        total_keywords = 0
        found_keywords = 0

        for feature in features:
            if feature in feature_keywords:
                keywords = feature_keywords[feature]
                total_keywords += len(keywords)
                found_keywords += sum(
                    1 for keyword in keywords if keyword in text_lower
                )

        if total_keywords == 0:
            return 0.5  # Default confidence

        return min(1.0, found_keywords / total_keywords)

    async def _format_output(
        self,
        document_info: Dict[str, Any],
        text_extraction_result: Dict[str, Any],
        analysis_result: Dict[str, Any],
        metadata_result: Dict[str, Any],
        summary_result: Dict[str, Any],
        classification_result: Dict[str, Any],
        context: ExecutionContext,
    ) -> Dict[str, Any]:
        """Format final output."""
        return {
            "status": "success",
            "document_info": document_info,
            "extracted_text": text_extraction_result["extracted_text"],
            "metadata": metadata_result,
            "analysis": {
                "language": analysis_result.get("language_detected"),
                "sentiment": analysis_result.get("sentiment"),
                "key_phrases": analysis_result.get("key_phrases", []),
                "entities": analysis_result.get("entities", []),
                "structure": analysis_result.get("content_structure"),
                "readability": analysis_result.get("readability"),
            },
            "summary": summary_result,
            "classification": classification_result,
            "processing_stats": {
                "page_count": text_extraction_result.get("page_count", 0),
                "word_count": text_extraction_result.get("word_count", 0),
                "character_count": text_extraction_result.get("character_count", 0),
                "processing_time": context.get_execution_duration(),
            },
            "agent_info": {
                "agent_name": self.name,
                "agent_version": "1.0",
                "processing_timestamp": datetime.utcnow().isoformat(),
            },
        }

    def get_processing_stats(self) -> Dict[str, Any]:
        """Get document processing statistics."""
        return {
            "documents_processed": self.documents_processed,
            "total_pages_processed": self.total_pages_processed,
            "processing_errors": self.processing_errors,
            "success_rate": (
                (self.documents_processed - self.processing_errors)
                / max(self.documents_processed, 1)
            )
            * 100,
            "average_pages_per_document": self.total_pages_processed
            / max(self.documents_processed, 1),
            "supported_formats": self.supported_formats,
            "cached_documents": len(self.document_cache),
        }


# Define document processing workflow
def create_document_processing_workflow() -> SimpleDAGWorkflow:
    """Create a document processing workflow definition."""

    workflow_definition = WorkflowDefinition(
        id="doc_processing_v1",
        name="Document Processing Workflow",
        description="Comprehensive document analysis and processing",
        steps=[
            WorkflowStep(
                id="ingest",
                name="Document Ingestion",
                step_type=StepType.AGENT,
                config={"agent_name": "document_processing_agent"},
                dependencies=[],
            ),
            WorkflowStep(
                id="ocr",
                name="OCR Processing",
                step_type=StepType.TOOL,
                config={
                    "tool_name": "ocr_tool",
                    "tool_params": {"language": "eng", "confidence_threshold": 0.8},
                },
                dependencies=["ingest"],
                condition="input.get('requires_ocr', False)",
            ),
            WorkflowStep(
                id="summarize",
                name="Content Summarization",
                step_type=StepType.TOOL,
                config={
                    "tool_name": "llm_tool",
                    "tool_params": {"task": "summarization", "max_length": 500},
                },
                dependencies=["ocr"],
            ),
            WorkflowStep(
                id="classify",
                name="Document Classification",
                step_type=StepType.AGENT,
                config={"agent_name": "document_processing_agent"},
                dependencies=["summarize"],
            ),
        ],
        metadata={
            "version": "1.0",
            "author": "AI Agent Framework",
            "tags": ["document_processing", "ocr", "nlp", "classification"],
        },
    )

    # Create agent registry
    agent_registry = {"document_processing_agent": DocumentProcessingAgent()}

    # Create tool registry
    tool_registry = {
        "ocr_tool": lambda input_data, context, **kwargs: {
            "extracted_text": f"OCR result for: {str(input_data)[:100]}...",
            "confidence": 0.95,
        },
        "llm_tool": lambda input_data, context, **kwargs: {
            "summary": f"Summary of: {str(input_data)[:200]}...",
            "key_points": ["Point 1", "Point 2", "Point 3"],
        },
    }

    return SimpleDAGWorkflow(
        definition=workflow_definition,
        agent_registry=agent_registry,
        tool_registry=tool_registry,
    )


# Example usage and flow definition for legacy compatibility
flow = {
    "flow_id": "doc_processing_v1",
    "description": "Document processing flow with OCR, analysis, and summarization",
    "tasks": [
        {
            "id": "ingest",
            "action": "http_ingest",
            "config": {
                "supported_formats": ["pdf", "docx", "jpg", "png"],
                "max_file_size": "100MB",
            },
        },
        {
            "id": "ocr",
            "depends_on": ["ingest"],
            "action": "ocr_tool",
            "config": {
                "engine": "tesseract",
                "language": "eng",
                "openvino_optimization": True,
            },
        },
        {
            "id": "summarize",
            "depends_on": ["ocr"],
            "action": "llm_tool",
            "config": {
                "model": "gpt-3.5-turbo",
                "task": "summarization",
                "max_tokens": 500,
            },
        },
        {
            "id": "classify",
            "depends_on": ["summarize"],
            "action": "classification_tool",
            "config": {
                "categories": ["legal", "financial", "technical", "academic", "general"]
            },
        },
        {
            "id": "store_results",
            "depends_on": ["classify"],
            "action": "data_persistence",
            "config": {
                "store_original": True,
                "store_extracted_text": True,
                "store_analysis": True,
            },
        },
    ],
    "metadata": {
        "version": "1.0",
        "created_by": "ai_agent_framework",
        "intel_optimizations": ["openvino_ocr", "openvino_classification"],
    },
}


from src.sdk.agents import register_agent  # noqa: E402

try:
    register_agent(DocumentProcessingAgent())
except Exception:
    pass
