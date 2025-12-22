# src/etl/amo_debug.py
from __future__ import annotations

import json
from pathlib import Path

from src.clients.amocrm_client import AmoCRMClient
from src.utils.logging import get_logger

logger = get_logger(__name__)


def amo_smoke_test(limit: int = 10) -> None:
    """
    1) Дёргаем AmoCRM API
    2) Берём 1 лид
    3) Сохраняем сырой JSON в data_out для анализа полей
    """
    client = AmoCRMClient()
    leads = client.fetch_leads_raw(limit=limit)

    if not leads:
        logger.info(
            "AmoCRM returned 0 leads for this pipeline/filter. Nothing to save."
        )
        return

    first = leads[0]

    out_dir = Path("data_out")
    out_dir.mkdir(parents=True, exist_ok=True)

    out_path = out_dir / "amocrm_lead_sample.json"
    out_path.write_text(
        json.dumps(first, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    logger.info(f"Saved AmoCRM lead sample to {out_path}")
    logger.info(
        f"Sample lead id: {first.get('id')}, status_id: {first.get('status_id')}"
    )
