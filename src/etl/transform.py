# src/etl/transform.py
from __future__ import annotations

import pandas as pd
from typing import Any

from src.utils.phone import normalize_phone
from src.utils.logging import get_logger

logger = get_logger(__name__)


def standardize_leads(df: pd.DataFrame) -> pd.DataFrame:
    """
    Приводит DataFrame лидов к единым правилам:
    - нормализация телефона
    - приведение дат
    - замена некорректных значений
    """
    df = df.copy()

    if "phone_normalized" in df.columns:
        df["phone_normalized"] = df["phone_normalized"].apply(normalize_phone)

    # даты
    date_cols = [
        "created_at",
        "dt_new",
        "dt_qualified",
        "dt_booked",
        "dt_visited",
        "dt_second_payment",
    ]
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    return df


def standardize_patients(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if "phone_normalized" in df.columns:
        df["phone_normalized"] = df["phone_normalized"].apply(normalize_phone)

    date_cols = ["first_visit_at", "last_visit_at"]
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    return df


def standardize_appointments(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if "datetime" in df.columns:
        df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")

    return df


def standardize_payments(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if "paid_at" in df.columns:
        df["paid_at"] = pd.to_datetime(df["paid_at"], errors="coerce")

    if "amount" in df.columns:
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0.0)

    return df
