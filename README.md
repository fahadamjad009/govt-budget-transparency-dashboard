# 🏛️ Australian Government Budget Transparency Dashboard

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.59-FF4B4B)
![Plotly](https://img.shields.io/badge/Plotly-6.8-3F4F75)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

Interactive exploration of Australian government finances — where the money comes from, where it goes, and how the fiscal position has trended over the last decade.

**Live demo:** _(add your Streamlit Cloud URL after deploying)_

## Business context

Public budget documents are dense and hard to navigate for non-specialists. This dashboard turns official ABS Government Finance Statistics into an interactive Sankey/treemap/trend view — the kind of transparency tool a policy team, journalist, or engaged citizen would actually use.

## Data

Australian Bureau of Statistics, **Government Finance Statistics, Annual, 2024-25** (published 21 April 2026), all levels of Australian government (Commonwealth, state, territory, local), current prices, original series. Figures are transcribed directly from ABS's published release and Insights articles — no estimation or fabrication.

- https://www.abs.gov.au/statistics/economy/government/government-finance-statistics-annual/latest-release
- https://www.abs.gov.au/articles/insights-government-finance-statistics-annual-2024-25

## Architecture

```mermaid
flowchart LR
    A[ABS GFS Annual 2024-25 official published release] --> C[build_dataset.py]
    B[ABS Insights articles COFOG-A + time series] --> C
    C --> D[5 core CSVs in data/]
    D --> E[forecast_trends.py]
    E --> F[projection + growth CSVs]
    D --> G[Streamlit app]
    F --> G
```

## App

6 tabs: Budget Flow (Sankey) · Category Breakdown (treemap + YoY) · Fiscal Trends (revenue/expenses/NOB) · Debt & Net Worth · Growth Drivers · Growth & Outlook (category growth/decline, structural balance, 5-year linear trend extrapolation).

**Important honesty note baked into the app itself:** the "outlook" projections are a simple linear trend fit over 10 annual data points — not an official fiscal forecast. Real budget forecasts (PBO, Treasury) model GDP growth, demographics, and policy settings explicitly. This is presented as illustrative direction only, clearly labeled in-app. The net operating balance trend in particular carries an R² of 0.009 — essentially no linear relationship with time — and the app surfaces this explicitly rather than hiding a weak fit.

## Project structure

```
govt-budget-transparency-dashboard/
├── .streamlit/config.toml
├── .gitignore
├── LICENSE
├── README.md
├── app.py
├── requirements.txt
├── src/
│   ├── build_dataset.py       # transcribes official ABS figures into CSVs
│   └── forecast_trends.py     # linear trend extrapolation + category growth calc
└── data/
    ├── cofog_expenses.csv
    ├── fiscal_time_series.csv
    ├── net_worth_debt.csv
    ├── expense_growth_drivers.csv
    ├── revenue_breakdown.csv
    ├── net_debt_projection.csv
    ├── net_operating_balance_projection.csv
    └── category_growth.csv
```

## Data Dictionary

### `category_growth.csv`
| Column | Type | Description |
|---|---|---|
| category | string | COFOG-A expense category name |
| amt_2024_25 | float | Category expense, 2024-25, $billion |
| amt_2023_24 | float | Category expense, 2023-24, $billion |
| change_billion | float | Dollar change 2023-24 → 2024-25, $billion |
| change_pct | float | Percentage change 2023-24 → 2024-25 |

### `cofog_expenses.csv`
| Column | Type | Description |
|---|---|---|
| year | string | Financial year (e.g. 2024-25) |
| category | string | COFOG-A functional expense category |
| pct_of_total | float | Category's share of total expenses, % |
| amount_billion | float | Category expense, $billion |

### `expense_growth_drivers.csv`
| Column | Type | Description |
|---|---|---|
| driver | string | Named driver of expense growth |
| growth_pct | float | Growth rate attributed to driver, % |
| contribution_billion | float | Dollar contribution to total growth, $billion |
| pct_of_total_growth | float | Driver's share of total expense growth, % |

### `fiscal_time_series.csv`
| Column | Type | Description |
|---|---|---|
| year | string | Financial year, 2015-16 to 2024-25 |
| revenue_billion | float | Total government revenue, $billion |
| expenses_billion | float | Total government expenses, $billion |
| net_operating_balance_billion | float | Revenue minus expenses, $billion |

### `net_debt_projection.csv`
| Column | Type | Description |
|---|---|---|
| year | string | Financial year, historical + 5-year projection |
| net_debt_pct_gdp | float | Net debt as % of GDP (historical or projected) |
| is_projection | bool | True if extrapolated, False if historical ABS figure |
| resid_std | float | Residual standard deviation of the linear fit |
| r2 | float | R² of the linear trend model (0.602 — moderate signal) |

### `net_operating_balance_projection.csv`
| Column | Type | Description |
|---|---|---|
| year | string | Financial year, historical + 5-year projection |
| net_operating_balance_billion | float | NOB, historical or projected, $billion |
| is_projection | bool | True if extrapolated, False if historical ABS figure |
| resid_std | float | Residual standard deviation of the linear fit |
| r2 | float | R² of the linear trend model (0.009 — no real linear relationship) |

### `net_worth_debt.csv`
| Column | Type | Description |
|---|---|---|
| year | string | Financial year, 2015-16 to 2024-25 |
| net_worth_billion | float | Government net worth, $billion |
| net_debt_billion | float | Government net debt, $billion |
| net_debt_pct_gdp | float | Net debt as % of GDP |

### `revenue_breakdown.csv`
| Column | Type | Description |
|---|---|---|
| component | string | Revenue source category |
| pct_of_revenue | float | Share of total revenue, % |
| growth_pct | float | YoY growth rate, % |

**Source for all datasets:** ABS Government Finance Statistics, Annual 2024-25 (released 21 April 2026), all levels of Australian government, current prices, original series.

## Key figures, 2024-25

| Metric | Value |
|---|---|
| Total expenses | $1,030.5b |
| Total revenue | $1,022.4b |
| Net operating balance | -$8.2b |
| Net debt (% GDP) | 34.4% |
| Largest expense category | Social protection (30.3%, $312.2b) |
| Fastest $ growth | Social protection (+$29.1b, +10.3%) |
| Only shrinking categories | Environmental protection (-2.4%), Economic affairs (-1.4%) |

## Quickstart

```bash
python -m venv venv
venv\Scripts\Activate.ps1        # Windows
pip install -r requirements.txt
python src/build_dataset.py       # builds the 5 core CSVs from ABS figures
python src/forecast_trends.py     # builds the trend-extrapolation + growth CSVs
streamlit run app.py
```

## Tech stack

Python · Pandas · NumPy · Streamlit · Plotly (Sankey, treemap) · ABS GFS data

## Limitations

- Only 2 years of category-level (COFOG-A) detail available (2023-24, 2024-25) — deeper historical category trends aren't possible without additional ABS releases
- No productivity, output, or sector-employment data — this dataset covers fiscal flows only, not economic productivity by sector (would need a separate ABS Multifactor Productivity or Labour Force series)
- Outlook tab is a basic linear trend, not a real fiscal forecast — explicitly caveated in-app
- No automated test suite yet

## Roadmap

- Join in ABS Labour Force / Multifactor Productivity data for a genuine sector productivity view
- State/territory-level budget breakdown (currently all-levels-of-government aggregate only)
- pytest suite + CI badge
- React/Vite companion webapp

## License

MIT — see [LICENSE](LICENSE)
