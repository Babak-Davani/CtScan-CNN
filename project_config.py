"""Filesystem configuration shared by the project notebooks."""

from __future__ import annotations

import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = Path(os.getenv("CTSCAN_DATA_DIR", PROJECT_ROOT / "data")).expanduser().resolve()
ARTIFACT_DIR = Path(
    os.getenv("CTSCAN_ARTIFACT_DIR", PROJECT_ROOT / "artifacts")
).expanduser().resolve()

SERIES_TENSOR_DIR = ARTIFACT_DIR / "series_tensors"
PATIENT_TENSOR_DIR = ARTIFACT_DIR / "patient_tensors"
MODEL_DIR = ARTIFACT_DIR / "models"
OUTPUT_DIR = ARTIFACT_DIR / "figures"


def ensure_output_dirs() -> None:
    """Create generated-output directories without modifying the input data directory."""

    for directory in (
        SERIES_TENSOR_DIR,
        PATIENT_TENSOR_DIR,
        MODEL_DIR,
        OUTPUT_DIR,
    ):
        directory.mkdir(parents=True, exist_ok=True)
