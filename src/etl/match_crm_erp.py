import pandas as pd


def match_leads_with_patients(
    leads: pd.DataFrame, patients: pd.DataFrame
) -> pd.DataFrame:
    patients_unique = patients[["patient_id", "phone_normalized"]].drop_duplicates()

    df = leads.merge(
        patients_unique,
        on="phone_normalized",
        how="left",
    )
    return df


def compute_revenue_features(
    leads_with_patient: pd.DataFrame,
    appointments: pd.DataFrame,
    payments: pd.DataFrame,
) -> pd.DataFrame:
    """
    На каждого лида вешаем:
    - revenue_total, revenue_30d/90d/365d
    - visits_count_total, visits_count_30d
    Считаем периоды от dt_visited (первый визит) или от created_at, если визита нет.
    """
    df = leads_with_patient.copy()

    # базовая дата отсчёта
    df["anchor_date"] = df["dt_visited"].fillna(df["created_at"])

    # джойн оплат к пациенту
    payments = payments.copy()
    payments["paid_at"] = pd.to_datetime(payments["paid_at"])

    # агрегируем по patient_id + окно в днях
    def revenue_in_days(group, days: int | None):
        if days is None:
            return group["amount"].sum()
        cutoff = group["anchor_date"].iloc[0] + pd.Timedelta(days=days)
        return group.loc[group["paid_at"] <= cutoff, "amount"].sum()

    # заранее склеим patient_id к anchor_date
    base = df[["patient_id", "anchor_date"]].dropna().copy()
    payments = payments.merge(base, on="patient_id", how="left", suffixes=("", "_lead"))

    # агрегируем по patient_id
    revenue_agg = (
        payments.groupby("patient_id")
        .apply(
            lambda g: pd.Series(
                {
                    "revenue_total": revenue_in_days(g, None),
                    "revenue_30d": revenue_in_days(g, 30),
                    "revenue_90d": revenue_in_days(g, 90),
                    "revenue_365d": revenue_in_days(g, 365),
                }
            )
        )
        .reset_index()
    )

    # визиты
    appointments = appointments.copy()
    appointments["datetime"] = pd.to_datetime(appointments["datetime"])
    visits_agg = (
        appointments.loc[appointments["status"] == "проведен"]
        .groupby("patient_id")["appointment_id"]
        .agg(visits_count_total="count")
        .reset_index()
    )

    df = df.merge(revenue_agg, on="patient_id", how="left")
    df = df.merge(visits_agg, on="patient_id", how="left")

    df[["revenue_total", "revenue_30d", "revenue_90d", "revenue_365d"]] = df[
        ["revenue_total", "revenue_30d", "revenue_90d", "revenue_365d"]
    ].fillna(0.0)
    df["visits_count_total"] = df["visits_count_total"].fillna(0).astype(int)

    # флаг клиента
    df["is_client"] = df["revenue_total"] > 0

    return df
