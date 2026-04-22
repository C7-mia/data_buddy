"""Universal loading utilities for tabular datasets."""

from __future__ import annotations

from io import BytesIO, StringIO
from pathlib import Path
from urllib.error import URLError
from urllib.parse import urlparse
from urllib.request import urlopen

import pandas as pd

from data_buddy.utils.config import BuddyConfig
from data_buddy.utils.errors import BuddyDataLoadError

SUPPORTED_EXTENSIONS = {".csv", ".xlsx", ".xls", ".json", ".parquet"}


def _is_url(path_or_url: str) -> bool:
    parsed = urlparse(path_or_url)
    return parsed.scheme in {"http", "https"}


def _read_csv_with_fallback(path_or_buffer, config: BuddyConfig) -> pd.DataFrame:
    last_error: Exception | None = None
    for encoding in config.fallback_encodings:
        try:
            return pd.read_csv(path_or_buffer, encoding=encoding)
        except UnicodeDecodeError as exc:
            last_error = exc
    raise BuddyDataLoadError(
        "Data Buddy couldn't read your CSV encoding. Try exporting as UTF-8 and retry."
    ) from last_error


def _read_csv_large(path: Path, config: BuddyConfig) -> pd.DataFrame:
    chunks = pd.read_csv(
        path, chunksize=config.chunk_size, encoding=config.default_encoding
    )
    return pd.concat(chunks, ignore_index=True)


def load_data(path_or_url: str, config: BuddyConfig | None = None) -> pd.DataFrame:
    """Load tabular data from local paths or remote URLs.

    Args:
        path_or_url: Local file path or URL to a supported dataset.
        config: Optional runtime configuration overrides.

    Returns:
        A pandas DataFrame containing the loaded dataset.

    Raises:
        BuddyDataLoadError: If the file cannot be loaded or format is unsupported.

    Example:
        >>> from data_buddy.preprocessing.loader import load_data
        >>> df = load_data("sales.csv")
    """

    config = config or BuddyConfig()

    if _is_url(path_or_url):
        try:
            with urlopen(path_or_url, timeout=20) as response:
                content = response.read()
        except URLError as exc:
            raise BuddyDataLoadError(
                "Data Buddy couldn't reach your URL. Please verify the link and try again."
            ) from exc

        ext = Path(urlparse(path_or_url).path).suffix.lower()
        if ext not in SUPPORTED_EXTENSIONS:
            raise BuddyDataLoadError(
                f"Data Buddy supports {sorted(SUPPORTED_EXTENSIONS)}. Received '{ext or 'unknown'}'."
            )

        if ext == ".csv":
            return _read_csv_with_fallback(
                StringIO(content.decode(config.default_encoding, errors="replace")),
                config,
            )
        if ext in {".xlsx", ".xls"}:
            return pd.read_excel(BytesIO(content))
        if ext == ".json":
            return pd.read_json(
                StringIO(content.decode(config.default_encoding, errors="replace"))
            )
        if ext == ".parquet":
            return pd.read_parquet(BytesIO(content))

    path = Path(path_or_url)
    if not path.exists():
        raise BuddyDataLoadError(
            "Data Buddy couldn't find your file. Please check the path and try again."
        )

    ext = path.suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise BuddyDataLoadError(
            f"Data Buddy supports {sorted(SUPPORTED_EXTENSIONS)}. Received '{ext or 'unknown'}'."
        )

    if ext == ".csv":
        size_mb = path.stat().st_size / (1024 * 1024)
        if size_mb >= config.large_file_threshold_mb:
            return _read_csv_large(path, config)
        return _read_csv_with_fallback(path, config)
    if ext in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    if ext == ".json":
        return pd.read_json(path)
    if ext == ".parquet":
        return pd.read_parquet(path)

    raise BuddyDataLoadError(
        "Data Buddy could not detect a supported format for this file."
    )
