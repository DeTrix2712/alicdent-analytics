# src/storage/sheets.py
from __future__ import annotations

import json
from typing import Sequence

import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

from src.config import GOOGLE_SHEETS_CREDENTIALS_JSON
from src.utils.logging import get_logger

logger = get_logger(__name__)

_scopes: Sequence[str] = (
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
)


def _get_client() -> gspread.Client:
    """
    Создаёт gspread-клиент из JSON-ключа, который лежит в переменной окружения
    GOOGLE_SHEETS_CREDENTIALS_JSON (строка с JSON).
    """
    if not GOOGLE_SHEETS_CREDENTIALS_JSON:
        raise RuntimeError("GOOGLE_SHEETS_CREDENTIALS_JSON is not set")

    creds_dict = json.loads(GOOGLE_SHEETS_CREDENTIALS_JSON)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, _scopes)
    client = gspread.authorize(creds)
    return client


def write_dataframe(
    df: pd.DataFrame,
    spreadsheet_name: str,
    worksheet_name: str,
) -> None:
    """
    Записать DataFrame в Google Sheets (перезаписав лист).
    """
    client = _get_client()
    sh = client.open(spreadsheet_name)

    try:
        ws = sh.worksheet(worksheet_name)
    except gspread.WorksheetNotFound:
        ws = sh.add_worksheet(
            title=worksheet_name,
            rows=str(max(len(df) + 10, 100)),
            cols=str(max(len(df.columns) + 5, 20)),
        )

    ws.clear()
    if df.empty:
        logger.warning(
            "write_dataframe: DataFrame is empty for %s/%s",
            spreadsheet_name,
            worksheet_name,
        )
        return

    header = df.columns.tolist()
    values = df.astype(object).values.tolist()
    ws.update([header] + values)
    logger.info(
        "Written %s rows to Google Sheet '%s' / '%s'",
        len(df),
        spreadsheet_name,
        worksheet_name,
    )
