"""
Checksum utility functions for deterministic integrity verification.
"""

import hashlib
from pathlib import Path
from typing import Union
import pandas as pd


def sha256_bytes(data: bytes) -> str:
    """Compute hex SHA-256 digest of raw bytes."""
    hasher = hashlib.sha256()
    hasher.update(data)
    return hasher.hexdigest()


def sha256_file(filepath: Union[str, Path]) -> str:
    """Compute hex SHA-256 digest of a file on disk."""
    path = Path(filepath)
    if not path.is_file():
        raise FileNotFoundError(f"File not found for hashing: {path}")
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def sha256_dataframe(df: pd.DataFrame) -> str:
    """
    Compute a deterministic SHA-256 hash of a pandas DataFrame.
    Converts DataFrame to canonical CSV representation before hashing.
    """
    csv_bytes = df.to_csv(index=False, lineterminator="\n").encode("utf-8")
    return sha256_bytes(csv_bytes)


def verify_file_checksum(filepath: Union[str, Path], expected_sha256: str) -> bool:
    """Verify that a file matches an expected SHA-256 digest."""
    calculated = sha256_file(filepath)
    return calculated.lower() == expected_sha256.lower()
