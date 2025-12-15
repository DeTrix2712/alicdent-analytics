# src/etl/schemas.py

LEADS_COLUMNS = [
    "lead_id",
    "contact_id",
    "phone_normalized",
    "created_at",
    "current_status_id",
    "current_status_name",
    "responsible_user_id",
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_content",
    "utm_term",
    "lead_source_tag",
    "dt_new",
    "dt_qualified",
    "dt_booked",
    "dt_visited",
    "dt_second_payment",
]

PATIENTS_COLUMNS = [
    "patient_id",
    "full_name",
    "phone_normalized",
    "first_visit_at",
    "last_visit_at",
    "visits_count_total",
]

APPOINTMENTS_COLUMNS = [
    "appointment_id",
    "patient_id",
    "datetime",
    "status",
    "doctor",
    "service_type",
    "branch",
]

PAYMENTS_COLUMNS = [
    "payment_id",
    "patient_id",
    "appointment_id",
    "paid_at",
    "amount",
    "payment_method",
]

ADS_COSTS_COLUMNS = [
    "date",
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
