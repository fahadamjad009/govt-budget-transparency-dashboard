import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Australian Government Budget Transparency Dashboard", layout="wide", page_icon="🏛️")

BG_MAIN, BORDER = "#eaf3fb", "rgba(255,255,255,0.5)"
ACCENT, ACCENT2, ACCENT3 = "#2563eb", "#0ea5e9", "#f97066"
TEXT, SUBTEXT = "#1e293b", "#64748b"
FONT = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"

st.markdown(f"""
<style>
    .stApp {{
        background:
            radial-gradient(circle at 6% 10%, rgba(37,99,235,0.22) 0%, transparent 40%),
            radial-gradient(circle at 94% 20%, rgba(14,165,233,0.20) 0%, transparent 42%),
            radial-gradient(circle at 15% 85%, rgba(249,112,102,0.14) 0%, transparent 38%),
            radial-gradient(circle at 88% 90%, rgba(37,99,235,0.16) 0%, transparent 40%),
            {BG_MAIN};
        font-family: {FONT};
    }}
    h1, h2, h3, h4 {{ font-family: {FONT} !important; color: {TEXT} !important; font-weight: 800 !important; }}
    p, span, label {{ font-family: {FONT} !important; color: {TEXT}; }}
    [data-testid="stCaptionContainer"] {{ color: {SUBTEXT} !important; }}

    .wave-divider {{ margin: -6px 0 18px 0; line-height: 0; }}

    /* Liquid-glass metric cards */
    [data-testid="stMetric"] {{
        background: rgba(255,255,255,0.45);
        backdrop-filter: blur(18px) saturate(180%);
        -webkit-backdrop-filter: blur(18px) saturate(180%);
        border: 1px solid rgba(255,255,255,0.6);
        border-left: 4px solid {ACCENT};
        border-radius: 22px 22px 22px 6px;
        padding: 18px 20px;
        box-shadow: 0 8px 24px rgba(37,99,235,0.10), inset 0 1px 0 rgba(255,255,255,0.7);
        transition: transform 0.25s cubic-bezier(.2,.8,.2,1), box-shadow 0.25s ease;
    }}
    [data-testid="stMetric"]:hover {{
        transform: translateY(-4px) scale(1.01);
        box-shadow: 0 16px 34px rgba(37,99,235,0.18), inset 0 1px 0 rgba(255,255,255,0.8);
    }}
    [data-testid="stMetricLabel"] {{ color: {SUBTEXT} !important; font-size: 12.5px !important; letter-spacing: 0.02em; }}
    [data-testid="stMetricValue"] {{ color: {ACCENT} !important; font-weight: 800 !important; }}
    [data-testid="stMetricDelta"] svg {{ display: none; }}

    .stTabs [data-baseweb="tab-list"] {{ gap: 4px; border-bottom: 1px solid {BORDER}; }}
    .stTabs [data-baseweb="tab"] {{ color: {SUBTEXT}; font-weight: 600; font-size: 13.5px; border-radius: 12px 12px 0 0; padding: 10px 16px; transition: color 0.15s ease, background 0.15s ease; }}
    .stTabs [data-baseweb="tab"]:hover {{ color: {ACCENT}; background: rgba(37,99,235,0.06); }}
    .stTabs [aria-selected="true"] {{ color: {ACCENT} !important; border-bottom: 3px solid {ACCENT2} !important; }}

    /* Liquid-glass chart cards -- translucent, blurred, animated top sheen */
    [data-testid="stVerticalBlockBorderWrapper"] {{
        background: rgba(255,255,255,0.38);
        backdrop-filter: blur(22px) saturate(190%);
        -webkit-backdrop-filter: blur(22px) saturate(190%);
        border: 1px solid rgba(255,255,255,0.55);
        border-radius: 28px 28px 28px 8px;
        padding: 10px 10px 4px 10px;
        box-shadow: 0 12px 32px rgba(37,99,235,0.10), inset 0 1px 0 rgba(255,255,255,0.6);
        margin-bottom: 8px;
        position: relative;
        overflow: hidden;
        transition: transform 0.3s cubic-bezier(.2,.8,.2,1), box-shadow 0.3s ease;
    }}
    [data-testid="stVerticalBlockBorderWrapper"]:hover {{
        transform: translateY(-3px);
        box-shadow: 0 18px 40px rgba(37,99,235,0.16), inset 0 1px 0 rgba(255,255,255,0.7);
    }}
    [data-testid="stVerticalBlockBorderWrapper"]::before {{
        content: "";
        position: absolute; top: 0; left: -50%; right: -50%; height: 5px;
        background: linear-gradient(90deg, transparent, {ACCENT}, {ACCENT2}, {ACCENT}, transparent);
        background-size: 200% 100%;
        animation: shimmer 6s linear infinite;
        opacity: 0.65;
    }}
    @keyframes shimmer {{
        0% {{ background-position: 200% 0; }}
        100% {{ background-position: -200% 0; }}
    }}

    [data-testid="stDataFrame"] {{
        border: 1px solid rgba(255,255,255,0.6);
        border-radius: 14px;
        overflow: hidden;
        backdrop-filter: blur(10px);
    }}

    h3 {{ position: relative; padding-left: 16px; margin-bottom: 4px !important; }}
    h3::before {{
        content: ""; position: absolute; left: 0; top: 4px; bottom: 4px;
        width: 5px; border-radius: 6px;
        background: linear-gradient(180deg, {ACCENT} 0%, {ACCENT2} 100%);
    }}

    [data-testid="stAlert"] {{
        border-radius: 18px !important;
        background: rgba(255,255,255,0.5) !important;
        backdrop-filter: blur(14px);
    }}
</style>
""", unsafe_allow_html=True)

WAVE_SVG = f"""
<div class="wave-divider">
<svg viewBox="0 0 1440 60" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none" style="width:100%;height:36px;">
<path d="M0,30 C240,60 480,0 720,20 C960,40 1200,10 1440,30 L1440,60 L0,60 Z" fill="{ACCENT}" opacity="0.14"/>
<path d="M0,38 C240,15 480,55 720,35 C960,15 1200,50 1440,25 L1440,60 L0,60 Z" fill="{ACCENT2}" opacity="0.18"/>
</svg>
</div>
"""

def style_fig(fig, height=450, title=None):
    kwargs = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                  font=dict(color=TEXT, family=FONT, size=12),
                  height=height, margin=dict(t=50, l=10, r=10, b=10), legend=dict(orientation="h", y=1.08, font=dict(color=TEXT)))
    if title:
        kwargs["title"] = dict(text=title, font=dict(size=14, color=TEXT))
    fig.update_layout(**kwargs)
    # Explicit tickfont color -- Plotly does not always inherit the global font
    # color for axis tick labels (esp. categorical y-axes), so set it directly.
    fig.update_xaxes(gridcolor="rgba(100,116,139,0.18)", zerolinecolor="rgba(100,116,139,0.25)",
                      tickfont=dict(color=TEXT, size=12), title_font=dict(color=TEXT))
    fig.update_yaxes(gridcolor="rgba(100,116,139,0.18)", zerolinecolor="rgba(100,116,139,0.25)",
                      tickfont=dict(color=TEXT, size=12), title_font=dict(color=TEXT))
    return fig

def card_chart(fig, subheader=None, caption=None):
    """Renders a chart inside a liquid-glass card container."""
    with st.container(border=True):
        if subheader:
            st.subheader(subheader)
        st.plotly_chart(fig, width="stretch")
        if caption:
            st.caption(caption)

@st.cache_data
def load_data():
    return {
        "cofog": pd.read_csv("data/cofog_expenses.csv"),
        "fiscal": pd.read_csv("data/fiscal_time_series.csv"),
        "debt": pd.read_csv("data/net_worth_debt.csv"),
        "growth": pd.read_csv("data/expense_growth_drivers.csv"),
        "revenue": pd.read_csv("data/revenue_breakdown.csv"),
        "debt_proj": pd.read_csv("data/net_debt_projection.csv"),
        "nob_proj": pd.read_csv("data/net_operating_balance_projection.csv"),
        "cat_growth": pd.read_csv("data/category_growth.csv"),
        "employment_state": pd.read_csv("data/public_sector_employment_by_state.csv"),
        "employment_national": pd.read_csv("data/public_sector_employment_national.csv"),
        "employment_industry": pd.read_csv("data/public_sector_employment_by_industry.csv"),
    }

data = load_data()
cofog24 = data["cofog"][data["cofog"]["year"] == "2024-25"].sort_values("amount_billion", ascending=False)
cofog23 = data["cofog"][data["cofog"]["year"] == "2023-24"].sort_values("amount_billion", ascending=False)

st.title("🏛️ Australian Government Budget Transparency Dashboard")
st.caption("Built from ABS Government Finance Statistics, Annual 2024-25 (published 21 April 2026) — all levels of "
           "Australian government (Commonwealth, state, territory, local), current prices, original series.")
st.markdown(WAVE_SVG, unsafe_allow_html=True)

tabs = st.tabs(["💰 Budget Flow", "📊 Category Breakdown", "📈 Fiscal Trends",
                "⚖️ Debt & Net Worth", "🔺 Growth Drivers", "🔮 Growth & Outlook",
                "🧑‍💼 Labour Force & Productivity"])

with tabs[0]:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total expenses 2024-25", f"${data['fiscal']['expenses_billion'].iloc[-1]:,.1f}b")
    c2.metric("Total revenue 2024-25", f"${data['fiscal']['revenue_billion'].iloc[-1]:,.1f}b")
    c3.metric("Net operating balance", f"${data['fiscal']['net_operating_balance_billion'].iloc[-1]:,.1f}b")
    c4.metric("Net debt (% GDP)", f"{data['debt']['net_debt_pct_gdp'].iloc[-1]:.1f}%")

    st.write("")
    labels = ["Total Government Expenses"] + cofog24["category"].tolist()
    sankey_fig = go.Figure(go.Sankey(
        node=dict(pad=20, thickness=18, label=labels, color=[ACCENT] + [ACCENT2] * len(cofog24),
                  line=dict(color="rgba(255,255,255,0.6)", width=1)),
        link=dict(source=[0] * len(cofog24), target=list(range(1, len(cofog24) + 1)),
                  value=cofog24["amount_billion"].tolist(),
                  color="rgba(37,99,235,0.20)"),
    ))
    card_chart(style_fig(sankey_fig, 550), "Budget allocation by function, 2024-25",
               "Flow width is proportional to $ billion allocated to each function. Source: ABS COFOG-A classification.")

with tabs[1]:
    fig_tree = px.treemap(cofog24, path=["category"], values="amount_billion",
                           color="amount_billion", color_continuous_scale=["#dbeafe", "#2563eb"])
    fig_tree.update_traces(textfont=dict(color="#0f172a", size=13))
    card_chart(style_fig(fig_tree, 500), "Expense treemap, 2024-25")

    st.write("")
    merged = cofog24.merge(cofog23, on="category", suffixes=("_2024_25", "_2023_24"))
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(x=merged["category"], y=merged["amount_billion_2023_24"], name="2023-24", marker_color="#cbd5e1"))
    fig_bar.add_trace(go.Bar(x=merged["category"], y=merged["amount_billion_2024_25"], name="2024-25", marker_color=ACCENT))
    fig_bar.update_layout(barmode="group", xaxis_tickangle=-30, yaxis_title="$ billion")
    fig_bar.update_traces(marker_line_width=0)
    card_chart(style_fig(fig_bar, 450), "Year-over-year comparison")

with tabs[2]:
    fig_fiscal = go.Figure()
    fig_fiscal.add_trace(go.Scatter(x=data["fiscal"]["year"], y=data["fiscal"]["revenue_billion"], name="Revenue",
                                     line=dict(color=ACCENT, width=3), fill="tozeroy", fillcolor="rgba(37,99,235,0.10)"))
    fig_fiscal.add_trace(go.Scatter(x=data["fiscal"]["year"], y=data["fiscal"]["expenses_billion"], name="Expenses",
                                     line=dict(color=ACCENT3, width=3)))
    fig_fiscal.update_layout(yaxis_title="$ billion")
    card_chart(style_fig(fig_fiscal, 450), "Revenue vs expenses, 2015-16 to 2024-25")

    st.write("")
    colors = [ACCENT if v >= 0 else ACCENT3 for v in data["fiscal"]["net_operating_balance_billion"]]
    fig_nob = go.Figure(go.Bar(x=data["fiscal"]["year"], y=data["fiscal"]["net_operating_balance_billion"], marker_color=colors))
    fig_nob.update_traces(marker_line_width=0)
    fig_nob.update_layout(yaxis_title="$ billion")
    card_chart(style_fig(fig_nob, 350), "Net operating balance")

with tabs[3]:
    fig_debt = go.Figure()
    fig_debt.add_trace(go.Scatter(x=data["debt"]["year"], y=data["debt"]["net_worth_billion"], name="Net worth", line=dict(color=ACCENT, width=3)))
    fig_debt.add_trace(go.Scatter(x=data["debt"]["year"], y=data["debt"]["net_debt_billion"], name="Net debt", line=dict(color=ACCENT3, width=3)))
    fig_debt.update_layout(yaxis_title="$ billion")
    card_chart(style_fig(fig_debt, 450), "Net worth vs net debt, 2015-16 to 2024-25")

    st.write("")
    fig_pct = go.Figure(go.Bar(x=data["debt"]["year"], y=data["debt"]["net_debt_pct_gdp"], marker_color=ACCENT2))
    fig_pct.update_traces(marker_line_width=0)
    fig_pct.update_layout(yaxis_title="% of GDP")
    card_chart(style_fig(fig_pct, 350), "Net debt as % of GDP")

with tabs[4]:
    g = data["growth"].sort_values("contribution_billion", ascending=True)
    fig_growth = go.Figure(go.Bar(x=g["contribution_billion"], y=g["driver"], orientation="h", marker_color=ACCENT))
    fig_growth.update_traces(marker_line_width=0)
    fig_growth.update_layout(xaxis_title="Contribution to YoY growth ($ billion)")
    card_chart(style_fig(fig_growth, 400), "What drove the $70.8b increase in expenses, 2024-25")

    st.write("")
    with st.container(border=True):
        st.subheader("Growth drivers detail")
        st.dataframe(data["growth"].rename(columns={
            "driver": "Driver", "growth_pct": "Growth %", "contribution_billion": "$ billion",
            "pct_of_total_growth": "% of total growth"}), use_container_width=True, hide_index=True)

    st.write("")
    with st.container(border=True):
        st.subheader("Revenue composition, 2024-25")
        st.dataframe(data["revenue"].rename(columns={
            "component": "Component", "pct_of_revenue": "% of revenue", "growth_pct": "Growth %"}),
            use_container_width=True, hide_index=True)

with tabs[5]:
    st.info("⚠️ The projections below are a simple linear regression fit over 10 annual data points, "
            "**not an official fiscal forecast**. Real budget forecasts (PBO, Treasury) model GDP growth, "
            "demographics, and policy settings explicitly. Fit quality (R²) is reported for each series — "
            "where it's weak, that's flagged explicitly rather than hidden. Treat all of this as illustrative "
            "direction, not prediction.")

    cg = data["cat_growth"].sort_values("change_pct", ascending=True)
    colors_cg = [ACCENT if v >= 0 else ACCENT3 for v in cg["change_pct"]]
    fig_cg = go.Figure(go.Bar(x=cg["change_pct"], y=cg["category"], orientation="h", marker_color=colors_cg))
    fig_cg.update_traces(marker_line_width=0)
    fig_cg.update_layout(xaxis_title="% change in $ allocated")
    card_chart(style_fig(fig_cg, 450), "Fastest-growing and shrinking expense categories, 2023-24 → 2024-25",
               "Real $ growth/decline per function, not just share-of-total change. Environmental protection and "
               "Economic affairs are the only categories that shrank in dollar terms.")

    st.write("")
    fiscal_growth = data["fiscal"].copy()
    fiscal_growth["revenue_growth_pct"] = fiscal_growth["revenue_billion"].pct_change() * 100
    fiscal_growth["expense_growth_pct"] = fiscal_growth["expenses_billion"].pct_change() * 100
    fiscal_growth = fiscal_growth.dropna()
    fig_struct = go.Figure()
    fig_struct.add_trace(go.Bar(x=fiscal_growth["year"], y=fiscal_growth["revenue_growth_pct"], name="Revenue growth %", marker_color=ACCENT))
    fig_struct.add_trace(go.Bar(x=fiscal_growth["year"], y=fiscal_growth["expense_growth_pct"], name="Expense growth %", marker_color=ACCENT3))
    fig_struct.update_traces(marker_line_width=0)
    fig_struct.update_layout(barmode="group", yaxis_title="YoY % change")
    card_chart(style_fig(fig_struct, 400), "Structural balance: revenue growth vs expense growth",
               "Years where the red bar exceeds the teal bar are years expense growth outpaced revenue growth — "
               "a structural driver of rising net debt.")

    st.write("")
    dp = data["debt_proj"]
    debt_r2 = dp["r2"].dropna().iloc[0]
    hist = dp[~dp["is_projection"]]
    proj = dp[dp["is_projection"]]
    fig_debt_proj = go.Figure()
    fig_debt_proj.add_trace(go.Scatter(x=hist["year"], y=hist["net_debt_pct_gdp"], name="Historical", line=dict(color=ACCENT, width=3)))
    fig_debt_proj.add_trace(go.Scatter(x=proj["year"], y=proj["net_debt_pct_gdp"], name="Trend extrapolation", line=dict(color=ACCENT2, width=3, dash="dash")))
    fig_debt_proj.update_layout(yaxis_title="% of GDP")
    debt_caption = (f"Linear fit R\u00b2 = {debt_r2:.2f} — a moderate historical trend, still only a direction indicator, not a forecast."
                     if debt_r2 >= 0.3 else f"Linear fit R\u00b2 = {debt_r2:.2f} — weak fit, low confidence in this extrapolation.")
    card_chart(style_fig(fig_debt_proj, 400), "Net debt (% GDP) — historical + 5-year linear trend extrapolation", debt_caption)

    st.write("")
    npj = data["nob_proj"]
    nob_r2 = npj["r2"].dropna().iloc[0]
    hist_n = npj[~npj["is_projection"]]
    proj_n = npj[npj["is_projection"]]
    fig_nob_proj = go.Figure()
    fig_nob_proj.add_trace(go.Bar(x=hist_n["year"], y=hist_n["net_operating_balance_billion"], name="Historical", marker_color=ACCENT))
    fig_nob_proj.add_trace(go.Bar(x=proj_n["year"], y=proj_n["net_operating_balance_billion"], name="Trend extrapolation", marker_color=ACCENT2))
    fig_nob_proj.update_traces(marker_line_width=0)
    fig_nob_proj.update_layout(yaxis_title="$ billion")
    with st.container(border=True):
        st.subheader("Net operating balance — historical + 5-year linear trend extrapolation")
        st.plotly_chart(style_fig(fig_nob_proj, 400), width="stretch")
        if nob_r2 < 0.3:
            st.error(f"⚠️ Linear fit R\u00b2 = {nob_r2:.3f} — essentially **no linear relationship with time**. "
                     f"Net operating balance swings on annual policy/economic shocks (e.g. COVID in 2020-21), not a "
                     f"smooth trend. This extrapolation line should be read as noise, not signal — shown for "
                     f"transparency about the method's limits, not as a usable projection.")
        else:
            st.caption(f"Linear fit R\u00b2 = {nob_r2:.2f}.")

with tabs[6]:
    st.info("📌 Source: ABS Public Sector Employment and Earnings, Australia (cat. 6248.0.55.002), 2024-25 "
            "financial year, released 6 November 2025. Employee job counts relate to June of the given year; "
            "cash wages relate to the full financial year. Only two years of data are shown (June 2024 vs June "
            "2025) — matching the same data-availability limitation already noted for COFOG-A category detail.")

    en = data["employment_national"]
    c1, c2, c3, c4 = st.columns(4)
    total_row = en[en["level_of_government"] == "Total Public Sector"].iloc[0]
    c1.metric("Total public sector jobs, Jun-25", f"{total_row['employee_jobs_thousands_jun25']:,.0f}k",
              f"{total_row['jobs_growth_pct']:+.1f}%")
    c2.metric("Total cash wages, 2024-25", f"${total_row['cash_wages_millions_2024_25']/1000:,.1f}b",
              f"{total_row['wages_growth_pct']:+.1f}%")
    c3.metric("Avg wage per job, 2024-25", f"${total_row['avg_wage_per_job_2024_25_thousands']:,.1f}k")
    c4.metric("Fastest wage growth", "Commonwealth", f"{en[en['level_of_government']=='Commonwealth']['wages_growth_pct'].iloc[0]:+.1f}%")

    st.write("")
    en_plot = en[en["level_of_government"] != "Total Public Sector"]
    fig_prod = go.Figure()
    fig_prod.add_trace(go.Bar(x=en_plot["level_of_government"], y=en_plot["jobs_growth_pct"], name="Jobs growth %", marker_color=ACCENT))
    fig_prod.add_trace(go.Bar(x=en_plot["level_of_government"], y=en_plot["wages_growth_pct"], name="Wages growth %", marker_color=ACCENT3))
    fig_prod.update_traces(marker_line_width=0)
    fig_prod.update_layout(barmode="group", yaxis_title="YoY % change, 2023-24 → 2024-25")
    card_chart(style_fig(fig_prod, 400), "Jobs growth vs wages growth by level of government",
               "Where the wages bar exceeds the jobs bar, average pay per job rose — either wage growth outpacing "
               "headcount growth, or a shift toward higher-paid roles. This is a cost-intensity signal, not a "
               "labour productivity measure (no output data exists to compute genuine productivity here).")

    st.write("")
    es = data["employment_state"]
    fig_state = px.bar(es, x="state", y="employee_jobs_thousands_jun25", color="level_of_government",
                        color_discrete_map={"Commonwealth": ACCENT2, "State": ACCENT, "Local": ACCENT3},
                        barmode="stack")
    fig_state.update_traces(marker_line_width=0)
    fig_state.update_layout(yaxis_title="Employee jobs ('000)", legend=dict(font=dict(color=TEXT)))
    card_chart(style_fig(fig_state, 450), "Public sector employee jobs by state/territory and level of government, Jun-25")

    st.write("")
    ei = data["employment_industry"].sort_values("cash_wages_millions_2024_25", ascending=True)
    fig_ind = go.Figure(go.Bar(x=ei["cash_wages_millions_2024_25"], y=ei["industry"], orientation="h", marker_color=ACCENT))
    fig_ind.update_traces(marker_line_width=0)
    fig_ind.update_layout(xaxis_title="Cash wages, $ million")
    card_chart(style_fig(fig_ind, 450), "Cash wages by industry, 2024-25",
               "Public administration and safety, Education and training, and Health care and social assistance "
               "are the three largest public sector wage bills by industry — consistent with those categories' "
               "dominance in the COFOG-A expense breakdown elsewhere in this dashboard.")

    st.write("")
    with st.container(border=True):
        st.subheader("Detail by state/territory and level of government")
        st.dataframe(es.rename(columns={
            "state": "State/Territory", "level_of_government": "Level of Government",
            "employee_jobs_thousands_jun24": "Jobs Jun-24 ('000)", "employee_jobs_thousands_jun25": "Jobs Jun-25 ('000)",
            "cash_wages_millions_2023_24": "Wages 2023-24 ($m)", "cash_wages_millions_2024_25": "Wages 2024-25 ($m)"}),
            use_container_width=True, hide_index=True)

st.markdown("---")
st.caption("Data: Australian Bureau of Statistics, Government Finance Statistics, Annual 2024-25; and Public "
           "Sector Employment and Earnings, Australia, 2024-25. All figures current prices, original series, "
           "all levels of Australian government.")
