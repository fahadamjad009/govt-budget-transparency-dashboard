import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Australian Government Budget Transparency Dashboard", layout="wide", page_icon="🏛️")

BG_MAIN, BG_CARD, BORDER = "#0a120e", "#10201a", "#1f3a2e"
ACCENT, ACCENT2, ACCENT3 = "#64FFDA", "#FFD166", "#FF6B6B"
TEXT, SUBTEXT = "#e8f5ee", "#8fae9d"
FONT = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"

st.markdown(f"""
<style>
    .stApp {{ background-color: {BG_MAIN}; font-family: {FONT}; }}
    h1, h2, h3, h4 {{ font-family: {FONT} !important; color: {TEXT} !important; font-weight: 800 !important; }}
    p, span, label {{ font-family: {FONT} !important; color: {TEXT}; }}
    [data-testid="stCaptionContainer"] {{ color: {SUBTEXT} !important; }}
    [data-testid="stMetric"] {{ background-color: {BG_CARD}; border: 1px solid {BORDER}; border-left: 3px solid {ACCENT}; border-radius: 10px; padding: 16px 18px; }}
    [data-testid="stMetricLabel"] {{ color: {SUBTEXT} !important; font-size: 12.5px !important; }}
    [data-testid="stMetricValue"] {{ color: {ACCENT} !important; font-weight: 800 !important; }}
    .stTabs [data-baseweb="tab-list"] {{ gap: 4px; border-bottom: 1px solid {BORDER}; }}
    .stTabs [data-baseweb="tab"] {{ color: {SUBTEXT}; font-weight: 600; font-size: 13.5px; border-radius: 8px 8px 0 0; padding: 10px 16px; }}
    .stTabs [aria-selected="true"] {{ color: {ACCENT} !important; border-bottom: 2px solid {ACCENT} !important; }}
    [data-testid="stDataFrame"] {{ border: 1px solid {BORDER}; border-radius: 8px; }}
</style>
""", unsafe_allow_html=True)

def style_fig(fig, height=450, title=None):
    kwargs = dict(paper_bgcolor=BG_CARD, plot_bgcolor=BG_CARD, font=dict(color=TEXT, family=FONT, size=12),
                  height=height, margin=dict(t=50, l=10, r=10, b=10), legend=dict(orientation="h", y=1.08))
    if title:
        kwargs["title"] = dict(text=title, font=dict(size=14, color=TEXT))
    fig.update_layout(**kwargs)
    fig.update_xaxes(gridcolor=BORDER)
    fig.update_yaxes(gridcolor=BORDER)
    return fig

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
    }

data = load_data()
cofog24 = data["cofog"][data["cofog"]["year"] == "2024-25"].sort_values("amount_billion", ascending=False)
cofog23 = data["cofog"][data["cofog"]["year"] == "2023-24"].sort_values("amount_billion", ascending=False)

st.title("🏛️ Australian Government Budget Transparency Dashboard")
st.caption("Built from ABS Government Finance Statistics, Annual 2024-25 (published 21 April 2026) — all levels of "
           "Australian government (Commonwealth, state, territory, local), current prices, original series.")

tabs = st.tabs(["💰 Budget Flow", "📊 Category Breakdown", "📈 Fiscal Trends",
                "⚖️ Debt & Net Worth", "🔺 Growth Drivers", "🔮 Growth & Outlook"])

with tabs[0]:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total expenses 2024-25", f"${data['fiscal']['expenses_billion'].iloc[-1]:,.1f}b")
    c2.metric("Total revenue 2024-25", f"${data['fiscal']['revenue_billion'].iloc[-1]:,.1f}b")
    c3.metric("Net operating balance", f"${data['fiscal']['net_operating_balance_billion'].iloc[-1]:,.1f}b")
    c4.metric("Net debt (% GDP)", f"{data['debt']['net_debt_pct_gdp'].iloc[-1]:.1f}%")

    st.subheader("Budget allocation by function, 2024-25")
    labels = ["Total Government Expenses"] + cofog24["category"].tolist()
    sankey_fig = go.Figure(go.Sankey(
        node=dict(pad=20, thickness=18, label=labels, color=[ACCENT] + [ACCENT2] * len(cofog24)),
        link=dict(source=[0] * len(cofog24), target=list(range(1, len(cofog24) + 1)),
                  value=cofog24["amount_billion"].tolist(),
                  color="rgba(100,255,218,0.25)"),
    ))
    st.plotly_chart(style_fig(sankey_fig, 550), width="stretch")
    st.caption("Flow width is proportional to $ billion allocated to each function. Source: ABS COFOG-A classification.")

with tabs[1]:
    st.subheader("Expense treemap, 2024-25")
    fig_tree = px.treemap(cofog24, path=["category"], values="amount_billion",
                           color="amount_billion", color_continuous_scale=["#10201a", "#64FFDA"])
    st.plotly_chart(style_fig(fig_tree, 500), width="stretch")

    st.subheader("Year-over-year comparison")
    merged = cofog24.merge(cofog23, on="category", suffixes=("_2024_25", "_2023_24"))
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(x=merged["category"], y=merged["amount_billion_2023_24"], name="2023-24", marker_color=BORDER))
    fig_bar.add_trace(go.Bar(x=merged["category"], y=merged["amount_billion_2024_25"], name="2024-25", marker_color=ACCENT))
    fig_bar.update_layout(barmode="group", xaxis_tickangle=-30, yaxis_title="$ billion")
    st.plotly_chart(style_fig(fig_bar, 450), width="stretch")

with tabs[2]:
    st.subheader("Revenue vs expenses, 2015-16 to 2024-25")
    fig_fiscal = go.Figure()
    fig_fiscal.add_trace(go.Scatter(x=data["fiscal"]["year"], y=data["fiscal"]["revenue_billion"], name="Revenue", line=dict(color=ACCENT, width=3)))
    fig_fiscal.add_trace(go.Scatter(x=data["fiscal"]["year"], y=data["fiscal"]["expenses_billion"], name="Expenses", line=dict(color=ACCENT3, width=3)))
    fig_fiscal.update_layout(yaxis_title="$ billion")
    st.plotly_chart(style_fig(fig_fiscal, 450), width="stretch")

    st.subheader("Net operating balance")
    colors = [ACCENT if v >= 0 else ACCENT3 for v in data["fiscal"]["net_operating_balance_billion"]]
    fig_nob = go.Figure(go.Bar(x=data["fiscal"]["year"], y=data["fiscal"]["net_operating_balance_billion"], marker_color=colors))
    fig_nob.update_layout(yaxis_title="$ billion")
    st.plotly_chart(style_fig(fig_nob, 350), width="stretch")

with tabs[3]:
    st.subheader("Net worth vs net debt, 2015-16 to 2024-25")
    fig_debt = go.Figure()
    fig_debt.add_trace(go.Scatter(x=data["debt"]["year"], y=data["debt"]["net_worth_billion"], name="Net worth", line=dict(color=ACCENT, width=3)))
    fig_debt.add_trace(go.Scatter(x=data["debt"]["year"], y=data["debt"]["net_debt_billion"], name="Net debt", line=dict(color=ACCENT3, width=3)))
    fig_debt.update_layout(yaxis_title="$ billion")
    st.plotly_chart(style_fig(fig_debt, 450), width="stretch")

    st.subheader("Net debt as % of GDP")
    fig_pct = go.Figure(go.Bar(x=data["debt"]["year"], y=data["debt"]["net_debt_pct_gdp"], marker_color=ACCENT2))
    fig_pct.update_layout(yaxis_title="% of GDP")
    st.plotly_chart(style_fig(fig_pct, 350), width="stretch")

with tabs[4]:
    st.subheader("What drove the $70.8b increase in expenses, 2024-25")
    g = data["growth"].sort_values("contribution_billion", ascending=True)
    fig_growth = go.Figure(go.Bar(x=g["contribution_billion"], y=g["driver"], orientation="h", marker_color=ACCENT))
    fig_growth.update_layout(xaxis_title="Contribution to YoY growth ($ billion)")
    st.plotly_chart(style_fig(fig_growth, 400), width="stretch")

    st.dataframe(data["growth"].rename(columns={
        "driver": "Driver", "growth_pct": "Growth %", "contribution_billion": "$ billion",
        "pct_of_total_growth": "% of total growth"}), width="stretch", hide_index=True)

    st.subheader("Revenue composition, 2024-25")
    st.dataframe(data["revenue"].rename(columns={
        "component": "Component", "pct_of_revenue": "% of revenue", "growth_pct": "Growth %"}),
        width="stretch", hide_index=True)

with tabs[5]:
    st.info("⚠️ The projections below are a simple linear trend fit over 10 annual data points, "
            "**not an official fiscal forecast**. Real budget forecasts (PBO, Treasury) model GDP growth, "
            "demographics, and policy settings explicitly. This shows only the direction implied by the "
            "recent historical trend if nothing changes — treat it as illustrative, not predictive.")

    st.subheader("Fastest-growing and shrinking expense categories, 2023-24 → 2024-25")
    cg = data["cat_growth"].sort_values("change_pct", ascending=True)
    colors_cg = [ACCENT if v >= 0 else ACCENT3 for v in cg["change_pct"]]
    fig_cg = go.Figure(go.Bar(x=cg["change_pct"], y=cg["category"], orientation="h", marker_color=colors_cg))
    fig_cg.update_layout(xaxis_title="% change in $ allocated")
    st.plotly_chart(style_fig(fig_cg, 450), width="stretch")
    st.caption("Real $ growth/decline per function, not just share-of-total change. Environmental protection and "
               "Economic affairs are the only categories that shrank in dollar terms.")

    st.subheader("Structural balance: revenue growth vs expense growth")
    fiscal_growth = data["fiscal"].copy()
    fiscal_growth["revenue_growth_pct"] = fiscal_growth["revenue_billion"].pct_change() * 100
    fiscal_growth["expense_growth_pct"] = fiscal_growth["expenses_billion"].pct_change() * 100
    fiscal_growth = fiscal_growth.dropna()
    fig_struct = go.Figure()
    fig_struct.add_trace(go.Bar(x=fiscal_growth["year"], y=fiscal_growth["revenue_growth_pct"], name="Revenue growth %", marker_color=ACCENT))
    fig_struct.add_trace(go.Bar(x=fiscal_growth["year"], y=fiscal_growth["expense_growth_pct"], name="Expense growth %", marker_color=ACCENT3))
    fig_struct.update_layout(barmode="group", yaxis_title="YoY % change")
    st.plotly_chart(style_fig(fig_struct, 400), width="stretch")
    st.caption("Years where the red bar exceeds the teal bar are years expense growth outpaced revenue growth — "
               "a structural driver of rising net debt.")

    st.subheader(f"Net debt (% GDP) — historical + 5-year linear trend extrapolation")
    dp = data["debt_proj"]
    fig_debt_proj = go.Figure()
    hist = dp[~dp["is_projection"]]
    proj = dp[dp["is_projection"]]
    fig_debt_proj.add_trace(go.Scatter(x=hist["year"], y=hist["net_debt_pct_gdp"], name="Historical", line=dict(color=ACCENT, width=3)))
    fig_debt_proj.add_trace(go.Scatter(x=proj["year"], y=proj["net_debt_pct_gdp"], name="Trend extrapolation", line=dict(color=ACCENT2, width=3, dash="dash")))
    fig_debt_proj.update_layout(yaxis_title="% of GDP")
    st.plotly_chart(style_fig(fig_debt_proj, 400), width="stretch")

    st.subheader("Net operating balance — historical + 5-year linear trend extrapolation")
    npj = data["nob_proj"]
    fig_nob_proj = go.Figure()
    hist_n = npj[~npj["is_projection"]]
    proj_n = npj[npj["is_projection"]]
    fig_nob_proj.add_trace(go.Bar(x=hist_n["year"], y=hist_n["net_operating_balance_billion"], name="Historical", marker_color=ACCENT))
    fig_nob_proj.add_trace(go.Bar(x=proj_n["year"], y=proj_n["net_operating_balance_billion"], name="Trend extrapolation", marker_color=ACCENT2))
    fig_nob_proj.update_layout(yaxis_title="$ billion")
    st.plotly_chart(style_fig(fig_nob_proj, 400), width="stretch")

st.markdown("---")
st.caption("Data: Australian Bureau of Statistics, Government Finance Statistics, Annual 2024-25. "
           "All figures current prices, original series, all levels of Australian government.")