# tests/test_match_crm_erp.py
import pandas as pd

from src.etl.match_crm_erp import match_leads_with_patients


def test_match_leads_with_patients_basic():
    leads = pd.DataFrame(
        [
            {"lead_id": 1, "phone_normalized": "+7701"},
            {"lead_id": 2, "phone_normalized": "+7702"},
        ]
    )
    patients = pd.DataFrame(
        [
            {"patient_id": 100, "phone_normalized": "+7701"},
        ]
    )

    result = match_leads_with_patients(leads, patients)

    assert "patient_id" in result.columns
    assert result.loc[result["lead_id"] == 1, "patient_id"].iloc[0] == 100
    assert pd.isna(result.loc[result["lead_id"] == 2, "patient_id"]).iloc[0]
