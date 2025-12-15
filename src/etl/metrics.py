# src/etl/metrics.py

import pandas as pd


def compute_marketing_metrics(
    leads: pd.DataFrame,
    leads_with_revenue: pd.DataFrame,
    ads_costs: pd.DataFrame,
) -> pd.DataFrame:
    """
    Считаем CPL, CAC, ROMI по связке utm_campaign + ad_id (через utm_content).
    Предполагаем: utm_campaign ↔ campaign_name, utm_content ↔ ad_id.
    """

    # 1) агрегируем лиды по кампании/креативу
    leads_group = (
        leads.groupby(["utm_campaign", "utm_content"])
        .agg(N_leads=("lead_id", "nunique"))
        .reset_index()
    )

    # 2) считаем N_clients (лиды с revenue_total > 0)
    leads_with_revenue["is_client"] = leads_with_revenue["revenue_total"] > 0
    clients_group = (
        leads_with_revenue.groupby(["utm_campaign", "utm_content"])
        .agg(
            N_clients=("is_client", "sum"),
            Revenue=("revenue_total", "sum"),
        )
        .reset_index()
    )

    # 3) расходы по рекламе по (campaign_name, ad_id)
    ads_group = (
        ads_costs.groupby(["campaign_name", "ad_id"])
        .agg(AdSpend=("spend", "sum"))
        .reset_index()
        .rename(
            columns={
                "campaign_name": "utm_campaign",
                "ad_id": "utm_content",
            }
        )
    )

    # 4) объединяем все три
    df = ads_group.merge(leads_group, on=["utm_campaign", "utm_content"], how="left")
    df = df.merge(clients_group, on=["utm_campaign", "utm_content"], how="left")

    df[["N_leads", "N_clients", "Revenue"]] = df[
        ["N_leads", "N_clients", "Revenue"]
    ].fillna(0)

    # 5) формулы
    df["CPL"] = df.apply(
        lambda row: row["AdSpend"] / row["N_leads"] if row["N_leads"] > 0 else 0,
        axis=1,
    )

    df["CAC"] = df.apply(
        lambda row: row["AdSpend"] / row["N_clients"] if row["N_clients"] > 0 else 0,
        axis=1,
    )

    df["AvgCheck"] = df.apply(
        lambda row: row["Revenue"] / row["N_clients"] if row["N_clients"] > 0 else 0,
        axis=1,
    )

    df["ROMI"] = df.apply(
        lambda row: (
            ((row["Revenue"] - row["AdSpend"]) / row["AdSpend"] * 100)
            if row["AdSpend"] > 0
            else 0
        ),
        axis=1,
    )

    return df


FUNNEL_STEPS = [
    ("dt_new", "Новый лид"),
    ("dt_qualified", "Квалифицирован"),
    ("dt_booked", "Записан"),
    ("dt_visited", "Пришел / был на встрече"),
    ("dt_second_payment", "Вторичная оплата"),
]


def compute_funnel_metrics(leads: pd.DataFrame) -> pd.DataFrame:
    """
    Считаем количество лидов на каждом шаге и конверсии между шагами
    в разрезе utm_source / utm_campaign / utm_content.
    """
    group_cols = ["utm_source", "utm_campaign", "utm_content"]

    # наличие этапа = не null в dt_*
    base = leads.copy()
    for col, _name in FUNNEL_STEPS:
        base[col + "_flag"] = base[col].notna()

    agg_dict = {col + "_flag": "sum" for col, _ in FUNNEL_STEPS}

    counts = (
        base.groupby(group_cols)
        .agg(agg_dict)
        .reset_index()
        .rename(
            columns={col + "_flag": col.replace("dt_", "n_") for col, _ in FUNNEL_STEPS}
        )
    )

    # считаем конверсии между соседними шагами
    for i in range(len(FUNNEL_STEPS) - 1):
        from_col = FUNNEL_STEPS[i][0].replace("dt_", "n_")
        to_col = FUNNEL_STEPS[i + 1][0].replace("dt_", "n_")
        conv_col = f"conv_{from_col}_to_{to_col}"
        counts[conv_col] = counts.apply(
            lambda row: row[to_col] / row[from_col] * 100 if row[from_col] > 0 else 0,
            axis=1,
        )

    return counts
