# src/etl/extract.py

import pandas as pd
from datetime import datetime, timedelta

from src.etl.schemas import (
    LEADS_COLUMNS,
    PATIENTS_COLUMNS,
    APPOINTMENTS_COLUMNS,
    PAYMENTS_COLUMNS,
    ADS_COSTS_COLUMNS,
)


def extract_leads_mock() -> pd.DataFrame:
    """Фейковые данные лидов для отладки логики."""
    data = [
        {
            "lead_id": 1,
            "contact_id": 101,
            "phone_normalized": "+77010000001",
            "created_at": datetime.now() - timedelta(days=10),
            "current_status_id": 11,
            "current_status_name": "Пришел / был на встрече",
            "responsible_user_id": 1,
            "utm_source": "meta",
            "utm_medium": "cpc",
            "utm_campaign": "implants_dec",
            "utm_content": "ad_001",
            "utm_term": None,
            "lead_source_tag": "META",
            "dt_new": datetime.now() - timedelta(days=10),
            "dt_qualified": datetime.now() - timedelta(days=9),
            "dt_booked": datetime.now() - timedelta(days=8),
            "dt_visited": datetime.now() - timedelta(days=7),
            "dt_second_payment": None,
        },
        # добавь ещё 2–3 строки, чтобы было что считать
    ]
    df = pd.DataFrame(data, columns=LEADS_COLUMNS)
    return df


def extract_patients_mock() -> pd.DataFrame:
    data = [
        {
            "patient_id": 1001,
            "full_name": "Иванов Иван",
            "phone_normalized": "+77010000001",
            "first_visit_at": datetime.now() - timedelta(days=7),
            "last_visit_at": datetime.now() - timedelta(days=3),
            "visits_count_total": 2,
        },
    ]
    return pd.DataFrame(data, columns=PATIENTS_COLUMNS)


def extract_appointments_mock() -> pd.DataFrame:
    data = [
        {
            "appointment_id": 5001,
            "patient_id": 1001,
            "datetime": datetime.now() - timedelta(days=7),
            "status": "проведен",
            "doctor": "Доктор А",
            "service_type": "Имплантация",
            "branch": "Центр",
        },
    ]
    return pd.DataFrame(data, columns=APPOINTMENTS_COLUMNS)


def extract_payments_mock() -> pd.DataFrame:
    data = [
        {
            "payment_id": 9001,
            "patient_id": 1001,
            "appointment_id": 5001,
            "paid_at": datetime.now() - timedelta(days=7),
            "amount": 150000.0,
            "payment_method": "безнал",
        },
    ]
    return pd.DataFrame(data, columns=PAYMENTS_COLUMNS)


def extract_ads_costs_mock() -> pd.DataFrame:
    data = [
        {
            "date": datetime.now().date(),
            "campaign_id": "cmp_1",
            "campaign_name": "implants_dec",
            "adset_id": "set_1",
            "adset_name": "set_main",
            "ad_id": "ad_001",
            "ad_name": "Креатив 1",
            "impressions": 1000,
            "clicks": 100,
            "spend": 20000.0,
        },
    ]
    return pd.DataFrame(data, columns=ADS_COSTS_COLUMNS)
