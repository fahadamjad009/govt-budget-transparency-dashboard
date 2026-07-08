"""
Build structured CSVs from officially published ABS Government Finance Statistics data.

Source: Australian Bureau of Statistics
- Government Finance Statistics, Annual, 2024-25 financial year
  https://www.abs.gov.au/statistics/economy/government/government-finance-statistics-annual/latest-release
- Insights into Government Finance Statistics, Annual, 2024-25
  https://www.abs.gov.au/articles/insights-government-finance-statistics-annual-2024-25
- Insights into Government Finance Statistics, Annual, 2023-24 (comparison year)
  https://www.abs.gov.au/articles/insights-government-finance-statistics-annual-2023-24
- Insights into Government Finance Statistics, June 2025
  https://www.abs.gov.au/articles/insights-government-finance-statistics-june-2025

All figures below are transcribed directly from ABS's published charts/tables (current
prices, original series, all levels of Australian government) as of the 2024-25 release,
published 21 April 2026. No figures are estimated or fabricated.
"""
import pandas as pd
from pathlib import Path

Path("data").mkdir(exist_ok=True)

# --- COFOG-A functional classification: expenses by purpose ---
# Total expenses 2024-25: $1,030.5b · 2023-24: $959.7b
cofog_2024_25 = {
    "Social protection": 30.3, "Health": 20.2, "Education": 14.4,
    "General public services": 10.8, "Public order and safety": 5.1, "Defence": 4.9,
    "Transport": 4.6, "Economic affairs": 4.5, "Environmental protection": 2.0,
    "Recreation, culture and religion": 1.9, "Housing and community amenities": 1.3,
}
cofog_2023_24 = {
    "Social protection": 29.5, "Health": 20.1, "Education": 14.5,
    "General public services": 10.8, "Public order and safety": 5.1, "Defence": 5.1,
    "Economic affairs": 4.9, "Transport": 4.5, "Environmental protection": 2.2,
    "Recreation, culture and religion": 2.0, "Housing and community amenities": 1.4,
}
TOTAL_2024_25 = 1030.5
TOTAL_2023_24 = 959.7

rows = []
for cat, pct in cofog_2024_25.items():
    rows.append({"year": "2024-25", "category": cat, "pct_of_total": pct,
                 "amount_billion": round(pct / 100 * TOTAL_2024_25, 2)})
for cat, pct in cofog_2023_24.items():
    rows.append({"year": "2023-24", "category": cat, "pct_of_total": pct,
                 "amount_billion": round(pct / 100 * TOTAL_2023_24, 2)})
pd.DataFrame(rows).to_csv("data/cofog_expenses.csv", index=False)

# --- Fiscal time series 2015-16 to 2024-25 ($ billion, all levels of Australian government) ---
years = ["2015-16","2016-17","2017-18","2018-19","2019-20","2020-21","2021-22","2022-23","2023-24","2024-25"]
revenue = [576, 607.7, 655.2, 694, 681.7, 728, 831.5, 923.3, 978.2, 1022.4]
expenses = [598.5, 621.3, 645, 677.4, 789.7, 873.4, 866.3, 885.4, 959.7, 1030.5]
net_operating_balance = [-22.5, -13.5, 10.2, 16.6, -108.1, -145.4, -34.8, 37.9, 18.4, -8.2]

pd.DataFrame({
    "year": years, "revenue_billion": revenue, "expenses_billion": expenses,
    "net_operating_balance_billion": net_operating_balance,
}).to_csv("data/fiscal_time_series.csv", index=False)

# --- Net worth & net debt time series 2015-16 to 2024-25 ($ billion / % GDP) ---
net_worth = [764.3, 884.3, 921.8, 799.7, 687.7, 679.4, 1011.6, 1208.1, 1385.2, 1380.0]
net_debt_billion = [390.2, 403.8, 436.1, 476.9, 634.2, 789.0, 778.7, 783.8, 846.6, 954.9]
net_debt_pct_gdp = [23.4, 22.9, 23.6, 24.4, 31.9, 37.7, 33.3, 30.4, 31.6, 34.4]

pd.DataFrame({
    "year": years, "net_worth_billion": net_worth,
    "net_debt_billion": net_debt_billion, "net_debt_pct_gdp": net_debt_pct_gdp,
}).to_csv("data/net_worth_debt.csv", index=False)

# --- 2024-25 expense growth drivers (contribution to the $70.8b YoY increase in expenses) ---
growth_drivers = [
    {"driver": "Employee expenses", "growth_pct": 8.6, "contribution_billion": 22.1, "pct_of_total_growth": 31.3},
    {"driver": "Social benefits to households in goods and services", "growth_pct": 12.3, "contribution_billion": 20.6, "pct_of_total_growth": 29.1},
    {"driver": "Current monetary transfers to households", "growth_pct": 6.8, "contribution_billion": 10.7, "pct_of_total_growth": 15.1},
    {"driver": "Use of goods and services", "growth_pct": 4.4, "contribution_billion": 8.1, "pct_of_total_growth": 11.4},
    {"driver": "Interest expense", "growth_pct": 9.9, "contribution_billion": 6.0, "pct_of_total_growth": 8.5},
]
pd.DataFrame(growth_drivers).to_csv("data/expense_growth_drivers.csv", index=False)

# --- 2024-25 revenue composition ---
revenue_breakdown = [
    {"component": "Taxation revenue", "pct_of_revenue": 82.8, "growth_pct": 4.3},
    {"component": "Royalty income", "pct_of_revenue": None, "growth_pct": -21.2},
]
pd.DataFrame(revenue_breakdown).to_csv("data/revenue_breakdown.csv", index=False)

print("Built 5 CSVs in data/:")
for f in ["cofog_expenses.csv", "fiscal_time_series.csv", "net_worth_debt.csv",
          "expense_growth_drivers.csv", "revenue_breakdown.csv"]:
    df = pd.read_csv(f"data/{f}")
    print(f"  {f}: {len(df)} rows")