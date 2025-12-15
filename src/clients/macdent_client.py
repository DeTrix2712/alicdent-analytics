# src/clients/macdent_client.py
from __future__ import annotations

import requests
import pandas as pd
from typing import Any

from src.config import MACDENT_API_URL, MACDENT_API_TOKEN
from src.utils.logging import get_logger

logger = get_logger(__name__)


class MacDentClient:
    """
    Клиент для ERP МакДент.
    Эндпоинты зависят от конкретной установки, поэтому тут только интерфейс.
    """

    def __init__(self) -> None:
        if not MACDENT_API_URL or not MACDENT_API_TOKEN:
            logger.warning(
                "MacDent credentials are not set; client will not work against real API."
            )
        self.base_url = MACDENT_API_URL.rstrip("/") if MACDENT_API_URL else ""
        self.token = MACDENT_API_TOKEN

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def _get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        if not self.base_url:
            raise RuntimeError("MACDENT_API_URL not configured")
        url = f"{self.base_url}{path}"
        resp = requests.get(url, headers=self._headers(), params=params or {})
        resp.raise_for_status()
        return resp.json()

    # Сырые данные (эти пути/параметры ты позже подставишь реальные):

    def fetch_patients_raw(self) -> list[dict[str, Any]]:
        raise NotImplementedError("Подставь реальный endpoint МакДент для пациентов")

    def fetch_appointments_raw(self) -> list[dict[str, Any]]:
        raise NotImplementedError("Подставь реальный endpoint МакДент для приёмов")

    def fetch_payments_raw(self) -> list[dict[str, Any]]:
        raise NotImplementedError("Подставь реальный endpoint МакДент для оплат")

    # Преобразование в наши схемы (PATIENTS_COLUMNS, APPOINTMENTS_COLUMNS, PAYMENTS_COLUMNS):

    def patients_to_df(self, raw: list[dict[str, Any]]) -> pd.DataFrame:
        """Каркас: здесь нужно будет спроецировать реальные поля МакДент в нашу схему."""
        rows: list[dict[str, Any]] = []
        for item in raw:
            rows.append(
                {
                    "patient_id": item.get("id"),
                    "full_name": item.get("full_name"),
                    "phone_normalized": None,  # нормализация по utils.phone
                    "first_visit_at": item.get("first_visit_at"),
                    "last_visit_at": item.get("last_visit_at"),
                    "visits_count_total": item.get("visits_count_total"),
                }
            )
        return pd.DataFrame(rows)

    def appointments_to_df(self, raw: list[dict[str, Any]]) -> pd.DataFrame:
        rows: list[dict[str, Any]] = []
        for item in raw:
            rows.append(
                {
                    "appointment_id": item.get("id"),
                    "patient_id": item.get("patient_id"),
                    "datetime": item.get("datetime"),
                    "status": item.get("status"),
                    "doctor": item.get("doctor"),
                    "service_type": item.get("service_type"),
                    "branch": item.get("branch"),
                }
            )
        return pd.DataFrame(rows)

    def payments_to_df(self, raw: list[dict[str, Any]]) -> pd.DataFrame:
        rows: list[dict[str, Any]] = []
        for item in raw:
            rows.append(
                {
                    "payment_id": item.get("id"),
                    "patient_id": item.get("patient_id"),
                    "appointment_id": item.get("appointment_id"),
                    "paid_at": item.get("paid_at"),
                    "amount": item.get("amount"),
                    "payment_method": item.get("payment_method"),
                }
            )
        return pd.DataFrame(rows)
