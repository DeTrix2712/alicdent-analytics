# tests/test_metrics.py
import pandas as pd

from src.etl.metrics import compute_marketing_metrics


def test_compute_marketing_metrics_basic():
    leads = pd.DataFrame(
        [
            {"lead_id": 1, "utm_campaign": "camp", "utm_content": "ad"},
        ]
    )

    leads_with_revenue = pd.DataFrame(
        [
            {
                "lead_id": 1,
                "utm_campaign": "camp",
                "utm_content": "ad",
                "revenue_total": 150.0,
            },
        ]
    )

    ads_costs = pd.DataFrame(
        [
            {
                "campaign_name": "camp",
                "ad_id": "ad",
                "spend": 50.0,
                "impressions": 100,
                "clicks": 10,
            }
        ]
    )

    metrics = compute_marketing_metrics(leads, leads_with_revenue, ads_costs)

    row = metrics.iloc[0]
    assert row["AdSpend"] == 50.0
    assert row["N_leads"] == 1
    assert row["N_clients"] == 1
    assert row["Revenue"] == 150.0
    assert row["CPL"] == 50.0
    assert row["CAC"] == 50.0
