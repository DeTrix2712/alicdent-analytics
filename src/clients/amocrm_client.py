# src/clients/amocrm_client.py
from __future__ import annotations

import requests
import pandas as pd
from typing import Any, Iterable

from src.config import AMOCRM_BASE_URL, AMOCRM_ACCESS_TOKEN, AMO_STATUS_MAP
from src.utils.logging import get_logger

logger = get_logger(__name__)


class AmoCRMClient:
    """
    Клиент AmoCRM.
    Сейчас: каркас.
    Потом:
      - реальное обновление токена
      - пагинация
      - маппинг кастомных полей в нашу схему.
    """

    def __init__(self) -> None:
        if not AMOCRM_BASE_URL or not AMOCRM_ACCESS_TOKEN:
            logger.warning(
                "AmoCRM credentials are not set; client will not work against real API."
            )
        self.base_url = AMOCRM_BASE_URL.rstrip("/") if AMOCRM_BASE_URL else ""
        self.token = AMOCRM_ACCESS_TOKEN

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    # === НИЗКОУРОВНЕВЫЙ GET ===
    def _get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        if not self.base_url:
            raise RuntimeError("AMOCRM_BASE_URL not configured")
        url = f"{self.base_url}{path}"
        resp = requests.get(url, headers=self._headers(), params=params or {})
        resp.raise_for_status()
        return resp.json()

    # === СЫРЬЁ ИЗ API ===

    def fetch_leads_raw(self, limit: int = 250) -> list[dict[str, Any]]:
        """
        Сырой список сделок из AmoCRM.
        TODO: добавить фильтры updated_at, пагинацию.
        """
        data = self._get("/api/v4/leads", params={"limit": limit})
        return data.get("_embedded", {}).get("leads", [])

    def fetch_status_history_raw(self, lead_id: int) -> list[dict[str, Any]]:
        """
        История изменений статусов для конкретного лида.
        Конкретный endpoint зависит от настроек AmoCRM (логи, timeline, events).
        Здесь только интерфейс.
        """
        # TODO: подобрать реальный endpoint под историю статусов
        raise NotImplementedError(
            "fetch_status_history_raw: endpoint нужно настроить под конкретный аккаунт"
        )

    # === ПРЕОБРАЗОВАНИЕ В НАШУ СХЕМУ ===

    def leads_to_df(self, leads_raw: Iterable[dict[str, Any]]) -> pd.DataFrame:
        """
        Преобразует сырые сделки AmoCRM в DataFrame с нашими полями LEADS_COLUMNS.
        Сейчас только каркас; реальные маппинги нужно дописать, когда увидишь JSON.
        """
        rows: list[dict[str, Any]] = []

        for item in leads_raw:
            # TODO: достать правильные поля и кастомные поля (UTM, телефон, теги).
            row = {
                "lead_id": item.get("id"),
                "contact_id": None,  # нужно будет вытащить из _embedded['contacts'] или доп. запросов
                "phone_normalized": None,  # нормализуем из телефона контакта через utils.phone
                "created_at": item.get("created_at"),
                "current_status_id": item.get("status_id"),
                "current_status_name": AMO_STATUS_MAP.get(item.get("status_id")),
                "responsible_user_id": item.get("responsible_user_id"),
                # UTM нужно доставать из custom_fields_values
                "utm_source": None,
                "utm_medium": None,
                "utm_campaign": None,
                "utm_content": None,
                "utm_term": None,
                "lead_source_tag": None,
                "dt_new": None,
                "dt_qualified": None,
                "dt_booked": None,
                "dt_visited": None,
                "dt_second_payment": None,
            }
            rows.append(row)

        df = pd.DataFrame(rows)
        return df
