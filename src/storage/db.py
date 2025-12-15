# src/storage/db.py
from __future__ import annotations

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from src.config import DB_URL
from src.utils.logging import get_logger

logger = get_logger(__name__)

_engine: Engine | None = None


def get_engine() -> Engine:
    """Ленивая инициализация SQLAlchemy Engine."""
    global _engine
    if _engine is None:
        if not DB_URL:
            raise RuntimeError("DB_URL is not set; cannot initialize DB engine")
        _engine = create_engine(DB_URL)
        logger.info("Initialized DB engine for %s", DB_URL)
    return _engine


def write_table(df: pd.DataFrame, table_name: str, if_exists: str = "replace") -> None:
    """
    Унифицированная запись DataFrame в БД.
    Пример DB_URL для Postgres:
      postgresql+psycopg2://user:password@host:5432/dbname
    """
    engine = get_engine()
    df.to_sql(table_name, engine, if_exists=if_exists, index=False)
    logger.info("Written %s rows into table %s", len(df), table_name)
