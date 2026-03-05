"""Runner script for the BATS 2023 DaySim processing pipeline."""

import argparse
import logging
import os
import shutil
import sys
from pathlib import Path

import geopandas as gpd
import polars as pl
import yaml

from pipeline.decoration import step
from pipeline.pipeline import Pipeline
from processing import (
    locate_parcels,
    detect_joint_trips,
    extract_tours,
    format_daysim,
    link_trips,
    load_data,
    write_data,
)
from processing.cleaning.clean_psrc_2023 import clean_2023_psrc_hts

# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

logger = logging.getLogger(__name__)

# For MTC network drives that seem to keep unmapping within python VM sessions
# Check if network drives are mapped; if not, map them
# drives = {
#     "M:": r"\\models.ad.mtc.ca.gov\data\models",
#     "X:": r"\\model3-a\Model3A-Share",
# }

# for drive, path in drives.items():
#     if not Path(drive).exists():
#         logger.info("Mapping network drive %s to %s", drive, path)
#         os.system(f"net use {drive} {path}")  # noqa: S605

# Path to the YAML config file you provided
CONFIG_PATH = Path(__file__).parent / "config.yaml"

# ---------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------
# Read output directory from config to place log file there
with CONFIG_PATH.open() as f:
    config = yaml.safe_load(f)
    output_dir = Path(config.get("output_dir", "output"))
    output_dir.mkdir(parents=True, exist_ok=True)

# Configure logging to both console and file
log_file = output_dir / "pipeline.log"
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Configure console handler with Unicode error handling for Windows
stdout_stream = (
    sys.stdout.reconfigure(errors="replace")
    if hasattr(sys.stdout, "reconfigure")
    else sys.stdout
)
console_handler = logging.StreamHandler(stream=stdout_stream)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# Get root logger, clear existing handlers, and configure it
root_logger = logging.getLogger()
root_logger.handlers.clear()
root_logger.setLevel(logging.DEBUG)
root_logger.addHandler(file_handler)
root_logger.addHandler(console_handler)

logger = logging.getLogger(__name__)
logger.info("Log file: %s", log_file)



# Set up custom steps dictionary ----------------------------------
processing_steps = [
    load_data,
    clean_2023_psrc_hts,
    locate_parcels,
    link_trips,
    detect_joint_trips,
    extract_tours,
    format_daysim,
    write_data,
]


# ---------------------------------------------------------------------
if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="PSRC HTS 2023 DaySim Processing Pipeline"
    )
    parser.add_argument(
        "--clear-cache",
        action="store_true",
        help="Clear the pipeline cache before running",
    )
    args = parser.parse_args()

    logger.info("Starting PSRC HTS 2023 DaySim Processing Pipeline")

    # Clear cache if requested
    cache_dir = Path(".cache")
    if args.clear_cache and cache_dir.exists():
        logger.info("Clearing pipeline cache at %s", cache_dir)
        shutil.rmtree(cache_dir)
        logger.info("Cache cleared")

    pipeline = Pipeline(
        config_path=CONFIG_PATH,
        steps=processing_steps,
        caching=True,
    )
    result = pipeline.run()

    logger.info("Pipeline finished successfully.")
