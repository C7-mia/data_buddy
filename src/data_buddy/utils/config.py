"""Runtime configuration for Data Buddy."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class BuddyConfig:
    """Configuration options for Data Buddy.

    Attributes:
        chunk_size: Row chunk size used for large CSV ingestion.
        large_file_threshold_mb: File size threshold that enables chunked loading.
        default_encoding: Encoding attempted first when reading text files.
        fallback_encodings: Additional encodings tried when decoding fails.
        extracted_data_dir: Directory where zip extractions are written.
        default_chart_output: Default destination for generated chart images.
        default_generated_script: Default destination for generated Python scripts.
    """

    chunk_size: int = int(os.getenv("DATA_BUDDY_CHUNK_SIZE", "100000"))
    large_file_threshold_mb: int = int(os.getenv("DATA_BUDDY_LARGE_FILE_MB", "50"))
    default_encoding: str = os.getenv("DATA_BUDDY_ENCODING", "utf-8")
    fallback_encodings: tuple[str, ...] = ("utf-8", "latin-1", "cp1252")
    extracted_data_dir: Path = Path(
        os.getenv("DATA_BUDDY_EXTRACTED_DATA_DIR", "extracted_data")
    )
    default_chart_output: Path = Path(
        os.getenv("DATA_BUDDY_DEFAULT_CHART_PATH", "business_chart.png")
    )
    default_generated_script: Path = Path(
        os.getenv("DATA_BUDDY_GENERATED_SCRIPT_PATH", "generated_analysis.py")
    )
