# src/clients/amocrm_client.py
from __future__ import annotations

import requests
import pandas as pd
from typing import Any, Iterable

from src.config import AMOCRM_BASE_URL, AMOCRM_TOKEN, AMOCRM_PIPELINE_ID
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
        if not AMOCRM_BASE_URL or not AMOCRM_TOKEN:
            logger.warning(
                "AmoCRM credentials are not set; client will not work against real API."
            )
        self.base_url = AMOCRM_BASE_URL.rstrip("/") if AMOCRM_BASE_URL else ""
        self.token = AMOCRM_TOKEN

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

        # Если не 2xx — покажем тело ответа (часто HTML с ошибкой/авторизацией)
        if not resp.ok:
            preview = (resp.text or "")[:800]
            raise RuntimeError(
                f"AmoCRM GET {url} failed: {resp.status_code}\n"
                f"Response preview:\n{preview}"
            )

        # Если 2xx, но пришло не JSON — тоже покажем превью
        try:
            return resp.json()
        except ValueError:
            preview = (resp.text or "")[:800]
            raise RuntimeError(
                f"AmoCRM GET {url} returned non-JSON body (status {resp.status_code}).\n"
                f"Response preview:\n{preview}"
            )

    # === СЫРЬЁ ИЗ API ===

    def fetch_leads_raw(
        self,
        limit: int = 250,
        pipeline_id: int | None = None,
    ) -> list[dict[str, Any]]:
        """
        Сырой список сделок из AmoCRM (только из нужной воронки).
        TODO: добавить фильтры updated_at, пагинацию.
        """
        pid = pipeline_id or AMOCRM_PIPELINE_ID
        if not pid:
            raise RuntimeError("AMOCRM_PIPELINE_ID is not set (set it in .env)")

        data = self._get(
            "/api/v4/leads",
            params={
                "limit": limit,
                "filter[pipeline_id]": pid,
            },
        )
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
                "contact_id": None,
                "phone_normalized": None,
                "created_at": item.get("created_at"),
                "updated_at": item.get("updated_at"),
                "current_status_id": item.get("status_id"),
                "current_status_name": None,
                "pipeline_id": item.get("pipeline_id"),
                "responsible_user_id": item.get("responsible_user_id"),
                # === Маркетинг (вводится вручную в AmoCRM) ===
                "traffic_source": None,  # напр. "Инстаграм", "2ГИС", "Сайт", ...
                "creative_key": None,  # ваш "креатив/реклама" (лучше хранить ad_id или внутренний ключ)
                # === Запись / визит (по скрину из сделки) ===
                "budget": None,  # Бюджет
                "appointment_status": None,  # Статус записи
                "doctor_name": None,  # ФИО врача
                "appointment_datetime": None,  # Дата и время приёма
                "appointment_created_at": None,  # Дата и время создания (записи)
                "appointment_creator_name": None,  # ФИО создавшего запись
                "visit_type": None,  # Тип приёма (первичный/повторный)
                "services_codes": None,  # Коды оказанных услуг (если это поле в Amo)
                "services_amount": None,  # Сумма оказанных услуг
                "amount_received": None,  # Фактически получен
                "discount": None,  # Скидка
                "branch": None,  # Филиал
                # === Коммуникации ===
                "topic": None,  # Тема обращения
                "call_result": None,  # Результат звонка
            }
            rows.append(row)

        df = pd.DataFrame(rows)
        return df
