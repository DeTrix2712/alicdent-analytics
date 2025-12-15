# src/clients/meta_client.py
from __future__ import annotations

import requests
import pandas as pd
from typing import Any

from src.config import META_ADS_ACCESS_TOKEN, META_ADS_ACCOUNT_ID
from src.utils.logging import get_logger

logger = get_logger(__name__)


class MetaAdsClient:
    """
    Клиент для Facebook Marketing API (Meta Ads).
    Здесь задаём интерфейс: забрать дневные инсайты по ad_id.
    """

    BASE_URL = "https://graph.facebook.com/v19.0"

    def __init__(self) -> None:
        if not META_ADS_ACCESS_TOKEN or not META_ADS_ACCOUNT_ID:
            logger.warning(
                "Meta Ads credentials are not set; client will not work against real API."
            )
        self.access_token = META_ADS_ACCESS_TOKEN
        self.account_id = META_ADS_ACCOUNT_ID

    def _get(self, path: str, params: dict[str, Any]) -> dict[str, Any]:
        params = dict(params)
        params["access_token"] = self.access_token
        url = f"{self.BASE_URL}{path}"
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    def fetch_ads_insights_raw(
        self, date_preset: str = "last_30d"
    ) -> list[dict[str, Any]]:
        """
        Сырые инсайты.
        TODO: при реальной работе лучше использовать time_range вместо date_preset.
        """
        path = f"/act_{self.account_id}/insights"
        params = {
            "level": "ad",
            "time_increment": 1,
            "date_preset": date_preset,
            "fields": ",".join(
                [
                    "date_start",
                    "campaign_id",
                    "campaign_name",
                    "adset_id",
                    "adset_name",
                    "ad_id",
                    "ad_name",
                    "impressions",
                    "clicks",
                    "spend",
                ]
            ),
        }
        data = self._get(path, params)
        return data.get("data", [])

    def insights_to_df(self, raw: list[dict[str, Any]]) -> pd.DataFrame:
        """
        Маппинг инсайтов в нашу таблицу ads_costs (ADS_COSTS_COLUMNS).
        """
        rows: list[dict[str, Any]] = []
        for item in raw:
            rows.append(
                {
                    "date": item.get("date_start"),
                    "campaign_id": item.get("campaign_id"),
                    "campaign_name": item.get("campaign_name"),
                    "adset_id": item.get("adset_id"),
                    "adset_name": item.get("adset_name"),
                    "ad_id": item.get("ad_id"),
                    "ad_name": item.get("ad_name"),
                    "impressions": int(item.get("impressions", 0)),
                    "clicks": int(item.get("clicks", 0)),
                    "spend": float(item.get("spend", 0.0)),
                }
            )
        return pd.DataFrame(rows)
