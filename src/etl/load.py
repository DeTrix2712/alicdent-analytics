# src/etl/load.py

import pandas as pd
from pathlib import Path

from src.utils.logging import get_logger

logger = get_logger(__name__)

OUTPUT_DIR = Path("data_out")
OUTPUT_DIR.mkdir(exist_ok=True)


def save_table(df: pd.DataFrame, name: str):
    if df is None or df.empty:
        logger.info(f"Table {name} is empty. Skipping save.")
        return
    path = OUTPUT_DIR / f"{name}.csv"
    df.to_csv(path, index=False)
    logger.info("Saved table %s to %s", name, path)
