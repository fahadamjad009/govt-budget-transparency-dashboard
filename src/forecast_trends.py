"""
Linear trend extrapolation of net debt (%GDP) and net operating balance, using
scikit-learn LinearRegression so fit quality (R²) is measurable and reportable.

IMPORTANT: This is a basic linear trend fit over 10 annual data points, not an
official fiscal forecast. Real budget forecasts (e.g. PBO, Treasury) model GDP
growth assumptions, demographics, policy settings and economic cycles explicitly.
A more complex ML model (e.g. gradient boosting) would be inappropriate here —
10 points cannot support a meaningful train/test split or cross-validation, and
would risk overfitting noise rather than capturing genuine signal. Linear
regression with a reported R² is the statistically honest choice at this sample
size. This extrapolation shows the DIRECTION implied by the recent historical
trend only, and is labeled as such in the app.
"""
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

FORECAST_YEARS = 5

def year_to_index(year_str):
    return int(year_str.split("-")[0])

def linear_forecast(years, values, n_forward):
    x = np.array([year_to_index(y) for y in years]).reshape(-1, 1)
    y = np.array(values)

    model = LinearRegression()
    model.fit(x, y)
    r2 = model.score(x, y)

    last_year = x[-1, 0]
    future_x = np.array([last_year + i for i in range(1, n_forward + 1)]).reshape(-1, 1)
    future_y = model.predict(future_x)
    future_labels = [f"{fx}-{str(fx+1)[-2:]}" for fx in future_x.flatten()]

    fitted = model.predict(x)
    resid_std = float(np.std(y - fitted))
    return future_labels, future_y, resid_std, r2

def main():
    debt = pd.read_csv("data/net_worth_debt.csv")
    fiscal = pd.read_csv("data/fiscal_time_series.csv")

    debt_labels, debt_proj, debt_std, debt_r2 = linear_forecast(
        debt["year"].tolist(), debt["net_debt_pct_gdp"].tolist(), FORECAST_YEARS
    )
    nob_labels, nob_proj, nob_std, nob_r2 = linear_forecast(
        fiscal["year"].tolist(), fiscal["net_operating_balance_billion"].tolist(), FORECAST_YEARS
    )

    debt_out = pd.DataFrame({
        "year": debt["year"].tolist() + debt_labels,
        "net_debt_pct_gdp": debt["net_debt_pct_gdp"].tolist() + list(debt_proj),
        "is_projection": [False] * len(debt) + [True] * FORECAST_YEARS,
        "resid_std": [None] * len(debt) + [debt_std] * FORECAST_YEARS,
        "r2": [None] * len(debt) + [debt_r2] * FORECAST_YEARS,
    })
    debt_out.to_csv("data/net_debt_projection.csv", index=False)

    nob_out = pd.DataFrame({
        "year": fiscal["year"].tolist() + nob_labels,
        "net_operating_balance_billion": fiscal["net_operating_balance_billion"].tolist() + list(nob_proj),
        "is_projection": [False] * len(fiscal) + [True] * FORECAST_YEARS,
        "resid_std": [None] * len(fiscal) + [nob_std] * FORECAST_YEARS,
        "r2": [None] * len(fiscal) + [nob_r2] * FORECAST_YEARS,
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

    print(f"Net debt trend: R\u00b2={debt_r2:.3f}, residual std \u00b1{debt_std:.2f}pp")
    print(debt_out.tail(FORECAST_YEARS)[["year", "net_debt_pct_gdp"]].to_string(index=False))
    print(f"\nNet operating balance trend: R\u00b2={nob_r2:.3f}, residual std \u00b1${nob_std:.2f}b")
    print(nob_out.tail(FORECAST_YEARS)[["year", "net_operating_balance_billion"]].to_string(index=False))
    print(f"\nCategory growth (2023-24 -> 2024-25):")
    print(growth[["category", "change_billion", "change_pct"]].to_string(index=False))

if __name__ == "__main__":
    main()