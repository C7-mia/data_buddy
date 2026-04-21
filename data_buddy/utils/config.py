"""Runtime configuration for Data Buddy."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(slots=True)
class BuddyConfig:
    """Configuration options for Data Buddy.

    Attributes:
        chunk_size: Row chunk size used for large CSV ingestion.
        large_file_threshold_mb: File size threshold that enables chunked loading.
        default_encoding: Encoding attempted first when reading text files.
        fallback_encodings: Additional encodings tried when decoding fails.
    """

    chunk_size: int = int(os.getenv("DATA_BUDDY_CHUNK_SIZE", "100000"))
    large_file_threshold_mb: int = int(os.getenv("DATA_BUDDY_LARGE_FILE_MB", "50"))
    default_encoding: str = os.getenv("DATA_BUDDY_ENCODING", "utf-8")
    fallback_encodings: tuple[str, ...] = ("utf-8", "latin-1", "cp1252")
