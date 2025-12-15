# src/main.py

from src.utils.logging import get_logger
from src.etl.extract import (
    extract_leads_mock,
    extract_patients_mock,
    extract_appointments_mock,
    extract_payments_mock,
    extract_ads_costs_mock,
)
from src.etl.match_crm_erp import (
    match_leads_with_patients,
    compute_revenue_features,
)
from src.etl.metrics import compute_marketing_metrics, compute_funnel_metrics
from src.etl.load import save_table
from src.etl.transform import (
    standardize_leads,
    standardize_patients,
    standardize_appointments,
    standardize_payments,
)


logger = get_logger(__name__)


def run_mock_etl():
    logger.info("Starting mock ETL run")

    leads = standardize_leads(extract_leads_mock())
    patients = standardize_patients(extract_patients_mock())
    appointments = standardize_appointments(extract_appointments_mock())
    payments = standardize_payments(extract_payments_mock())
    ads_costs = extract_ads_costs_mock()

    leads_with_patient = match_leads_with_patients(leads, patients)
    leads_with_revenue = compute_revenue_features(
        leads_with_patient,
        appointments=appointments,
        payments=payments,
    )

    marketing_metrics = compute_marketing_metrics(
        leads=leads,
        leads_with_revenue=leads_with_revenue,
        ads_costs=ads_costs,
    )
    funnel_metrics = compute_funnel_metrics(leads_with_revenue)

    save_table(leads_with_revenue, "leads_with_revenue")
    save_table(marketing_metrics, "marketing_metrics")
    save_table(funnel_metrics, "funnel_metrics")

    logger.info("Mock ETL finished")


if __name__ == "__main__":
    run_mock_etl()
