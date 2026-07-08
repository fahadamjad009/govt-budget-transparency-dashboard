\# 🏛️ Australian Government Budget Transparency Dashboard



!\[Python](https://img.shields.io/badge/Python-3.11-blue)

!\[Streamlit](https://img.shields.io/badge/Streamlit-1.59-FF4B4B)

!\[Plotly](https://img.shields.io/badge/Plotly-6.8-3F4F75)

!\[License](https://img.shields.io/badge/License-MIT-lightgrey)



Interactive exploration of Australian government finances — where the money comes from, where it goes, and how the fiscal position has trended over the last decade.



\*\*Live demo:\*\* \_(add your Streamlit Cloud URL after deploying)\_



\## Business context

Public budget documents are dense and hard to navigate for non-specialists. This dashboard turns official ABS Government Finance Statistics into an interactive Sankey/treemap/trend view — the kind of transparency tool a policy team, journalist, or engaged citizen would actually use.



\## Data

Australian Bureau of Statistics, \*\*Government Finance Statistics, Annual, 2024-25\*\* (published 21 April 2026), all levels of Australian government (Commonwealth, state, territory, local), current prices, original series. Figures are transcribed directly from ABS's published release and Insights articles — no estimation or fabrication.

\- https://www.abs.gov.au/statistics/economy/government/government-finance-statistics-annual/latest-release

\- https://www.abs.gov.au/articles/insights-government-finance-statistics-annual-2024-25



\## Architecture



```mermaid

flowchart LR

&#x20;   A\[ABS GFS Annual 2024-25<br/>official published release] --> C\[build\_dataset.py]

&#x20;   B\[ABS Insights articles<br/>COFOG-A + time series] --> C

&#x20;   C --> D\[5 core CSVs<br/>data/]

&#x20;   D --> E\[forecast\_trends.py]

&#x20;   E --> F\[projection + growth CSVs]

&#x20;   D --> G\[Streamlit app]

&#x20;   F --> G

```





\## App

6 tabs: Budget Flow (Sankey) · Category Breakdown (treemap + YoY) · Fiscal Trends (revenue/expenses/NOB) · Debt \& Net Worth · Growth Drivers · Growth \& Outlook (category growth/decline, structural balance, 5-year linear trend extrapolation).







\*\*Important honesty note baked into the app itself:\*\* the "outlook" projections are a simple linear trend fit over 10 annual data points — not an official fiscal forecast. Real budget forecasts (PBO, Treasury) model GDP growth, demographics, and policy settings explicitly. This is presented as illustrative direction only, clearly labeled in-app.



\## Project structure

```

govt-budget-transparency-dashboard/

├── .streamlit/config.toml

├── .gitignore

├── LICENSE

├── README.md

├── app.py

├── requirements.txt

├── src/

│   ├── build\_dataset.py       # transcribes official ABS figures into CSVs

│   └── forecast\_trends.py     # linear trend extrapolation + category growth calc

└── data/

&#x20;   ├── cofog\_expenses.csv

&#x20;   ├── fiscal\_time\_series.csv

&#x20;   ├── net\_worth\_debt.csv

&#x20;   ├── expense\_growth\_drivers.csv

&#x20;   ├── revenue\_breakdown.csv

&#x20;   ├── net\_debt\_projection.csv

&#x20;   ├── net\_operating\_balance\_projection.csv

&#x20;   └── category\_growth.csv

```



\## Key figures, 2024-25

| Metric | Value |

|---|---|

| Total expenses | $1,030.5b |

| Total revenue | $1,022.4b |

| Net operating balance | -$8.2b |

| Net debt (% GDP) | 34.4% |

| Largest expense category | Social protection (30.3%, $312.2b) |

| Fastest $ growth | Social protection (+$29.1b, +10.3%) |

| Only shrinking categories | Environmental protection (-2.4%), Economic affairs (-1.4%) |



\## Quickstart

```bash

python -m venv venv

venv\\Scripts\\Activate.ps1        # Windows

pip install -r requirements.txt

python src/build\_dataset.py       # builds the 5 core CSVs from ABS figures

python src/forecast\_trends.py     # builds the trend-extrapolation + growth CSVs

streamlit run app.py

```



\## Tech stack

Python · Pandas · NumPy · Streamlit · Plotly (Sankey, treemap) · ABS GFS data



\## Limitations

\- Only 2 years of category-level (COFOG-A) detail available (2023-24, 2024-25) — deeper historical category trends aren't possible without additional ABS releases

\- No productivity, output, or sector-employment data — this dataset covers fiscal flows only, not economic productivity by sector (would need a separate ABS Multifactor Productivity or Labour Force series)

\- Outlook tab is a basic linear trend, not a real fiscal forecast — explicitly caveated in-app

\- No automated test suite yet



\## Roadmap

\- Join in ABS Labour Force / Multifactor Productivity data for a genuine sector productivity view

\- State/territory-level budget breakdown (currently all-levels-of-government aggregate only)

\- pytest suite + CI badge

\- React/Vite companion webapp



\## License

MIT — see \[LICENSE](LICENSE)

