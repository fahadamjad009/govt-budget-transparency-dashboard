"""
Simple linear trend extrapolation of net debt (%GDP) and net operating balance.

IMPORTANT: This is a basic linear trend fit over 10 annual data points, not an
official fiscal forecast. Real budget forecasts (e.g. PBO, Treasury) model GDP
growth assumptions, demographics, policy settings and economic cycles explicitly.
This extrapolation exists to show the DIRECTION implied by the recent historical
trend only, and is labeled as such in the app.
"""
import numpy as np
import pandas as pd

FORECAST_YEARS = 5

def year_to_index(year_str):
    return int(year_str.split("-")[0])

def linear_forecast(years, values, n_forward):
    x = np.array([year_to_index(y) for y in years])
    y = np.array(values)
    coeffs = np.polyfit(x, y, deg=1)
    slope, intercept = coeffs
    last_year = x[-1]
    future_x = np.array([last_year + i for i in range(1, n_forward + 1)])
    future_y = slope * future_x + intercept
    future_labels = [f"{fx}-{str(fx+1)[-2:]}" for fx in future_x]
    # residual-based rough uncertainty band (not a proper confidence interval)
    fitted = slope * x + intercept
    resid_std = float(np.std(y - fitted))
    return future_labels, future_y, resid_std

def main():
    debt = pd.read_csv("data/net_worth_debt.csv")
    fiscal = pd.read_csv("data/fiscal_time_series.csv")

    debt_labels, debt_proj, debt_std = linear_forecast(
        debt["year"].tolist(), debt["net_debt_pct_gdp"].tolist(), FORECAST_YEARS
    )
    nob_labels, nob_proj, nob_std = linear_forecast(
        fiscal["year"].tolist(), fiscal["net_operating_balance_billion"].tolist(), FORECAST_YEARS
    )

    debt_out = pd.DataFrame({
        "year": debt["year"].tolist() + debt_labels,
        "net_debt_pct_gdp": debt["net_debt_pct_gdp"].tolist() + list(debt_proj),
        "is_projection": [False] * len(debt) + [True] * FORECAST_YEARS,
        "resid_std": [None] * len(debt) + [debt_std] * FORECAST_YEARS,
    })
    debt_out.to_csv("data/net_debt_projection.csv", index=False)

    nob_out = pd.DataFrame({
        "year": fiscal["year"].tolist() + nob_labels,
        "net_operating_balance_billion": fiscal["net_operating_balance_billion"].tolist() + list(nob_proj),
        "is_projection": [False] * len(fiscal) + [True] * FORECAST_YEARS,
        "resid_std": [None] * len(fiscal) + [nob_std] * FORECAST_YEARS,
    })
    nob_out.to_csv("data/net_operating_balance_projection.csv", index=False)

    # Category growth/decline: real $ and % change 2023-24 -> 2024-25
    cofog = pd.read_csv("data/cofog_expenses.csv")
    c24 = cofog[cofog["year"] == "2024-25"][["category", "amount_billion"]].rename(columns={"amount_billion": "amt_2024_25"})
    c23 = cofog[cofog["year"] == "2023-24"][["category", "amount_billion"]].rename(columns={"amount_billion": "amt_2023_24"})
    growth = c24.merge(c23, on="category")
    growth["change_billion"] = (growth["amt_2024_25"] - growth["amt_2023_24"]).round(2)
    growth["change_pct"] = ((growth["change_billion"] / growth["amt_2023_24"]) * 100).round(1)
    growth = growth.sort_values("change_pct", ascending=False)
    growth.to_csv("data/category_growth.csv", index=False)

    print(f"Net debt projection ({FORECAST_YEARS}yr, residual std ±{debt_std:.1f}pp): {debt_out.tail(FORECAST_YEARS)[['year','net_debt_pct_gdp']].to_string(index=False)}")
    print(f"\nNet operating balance projection ({FORECAST_YEARS}yr, residual std ±${nob_std:.1f}b): {nob_out.tail(FORECAST_YEARS)[['year','net_operating_balance_billion']].to_string(index=False)}")
    print(f"\nCategory growth (2023-24 -> 2024-25):\n{growth[['category','change_billion','change_pct']].to_string(index=False)}")

if __name__ == "__main__":
    main()