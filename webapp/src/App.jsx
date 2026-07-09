import { useEffect } from 'react'
import {
  LineChart, Line, BarChart, Bar, ComposedChart, Area, Sankey,
  XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend, Rectangle,
} from 'recharts'
import { useReveal, useCountUp } from './hooks/useReveal'
import * as D from './data'
import './App.css'

const STREAMLIT_URL = 'https://govt-budget-transparency-dashboard.streamlit.app'
const REPO_URL = 'https://github.com/fahadamjad009/govt-budget-transparency-dashboard'
const INK = '#132A4C', BRASS = '#B08D57', SLATE = '#5C7A99', RED = '#7A2E2E', HAIR = '#D6D9D4'
const monoTick = { fill: SLATE, fontSize: 12, fontFamily: 'IBM Plex Mono' }
const tooltipStyle = { fontFamily: 'IBM Plex Mono', fontSize: 12, border: `1px solid ${HAIR}`, borderRadius: 3 }

function AuditStamp({ label }) {
  const [ref, revealed] = useReveal(0.6)
  return (
    <div className="stamp-wrap" ref={ref}>
      <span className={`stamp ${revealed ? 'revealed' : ''}`}>Audited · ABS Sourced</span>
      <span className="stamp-caption">{label}</span>
    </div>
  )
}

function Folio({ number, title, sub, children }) {
  const [ref, revealed] = useReveal(0.12)
  return (
    <section className={`folio ${revealed ? 'revealed' : ''}`} ref={ref}>
      <div className="folio-head">
        <span className="folio-number">Folio {number}</span>
        <h2 className="folio-title">{title}</h2>
      </div>
      {sub && <p className="folio-sub">{sub}</p>}
      {children}
    </section>
  )
}

function Ribbon() {
  return (
    <div className="ribbon">
      <div className="ribbon-item"><span className="ribbon-label">Revenue 24-25</span><span className="ribbon-value">$1,022.4b</span></div>
      <div className="ribbon-item"><span className="ribbon-label">Expenses 24-25</span><span className="ribbon-value">$1,030.5b</span></div>
      <div className="ribbon-item"><span className="ribbon-label">Net Operating Balance</span><span className="ribbon-value neg">-$8.2b</span></div>
      <div className="ribbon-item"><span className="ribbon-label">Net Debt / GDP</span><span className="ribbon-value">34.4%</span></div>
      <div className="ribbon-item"><span className="ribbon-label">Public Sector Jobs</span><span className="ribbon-value">2,597.3k</span></div>
    </div>
  )
}

function Stat({ label, prefix = '', suffix = '', target, decimals = 1, negative = false, start }) {
  const value = useCountUp(target, start)
  return (
    <div className="stat">
      <div className="stat-label">{label}</div>
      <div className={`stat-value ${negative ? 'neg' : ''}`}>{prefix}{value.toFixed(decimals)}{suffix}</div>
    </div>
  )
}

// Custom Sankey node renderer -- recharts does NOT auto-label nodes when a
// custom node component is supplied, so the name text has to be drawn
// explicitly here alongside the rectangle. Root node label sits to the
// left (right-aligned text); category nodes sit to the right (left-aligned).
function SankeyNode({ x, y, width, height, index, payload, containerWidth }) {
  const isRoot = index === 0
  const textX = isRoot ? x - 10 : x + width + 10
  const textAnchor = isRoot ? 'end' : 'start'
  return (
    <g>
      <Rectangle x={x} y={y} width={width} height={height} fill={isRoot ? INK : BRASS} fillOpacity={isRoot ? 1 : 0.85} />
      <text
        x={textX}
        y={y + height / 2}
        textAnchor={textAnchor}
        dominantBaseline="middle"
        fontFamily="Inter"
        fontSize={isRoot ? 13 : 12}
        fontWeight={isRoot ? 600 : 500}
        fill={INK}
      >
        {payload.name}
      </text>
    </g>
  )
}

export default function App() {
  const [heroRef, heroRevealed] = useReveal(0.1)

  useEffect(() => { document.title = 'Australian Government Budget — The Ledger' }, [])

  const yoyBars = D.cofog2425.map(c => ({
    category: c.category, '2023-24': D.cofog2324[c.category], '2024-25': c.billion,
  }))

  return (
    <>
      <Ribbon />
      <div className="app">
        <header className="hero" ref={heroRef}>
          <div className="hero-eyebrow">2024–25 Financial Year · Companion Reader</div>
          <h1>Every dollar the Commonwealth spent, entered in the ledger.</h1>
          <p>
            A folio-by-folio walk through Australia's 2024-25 government finances —
            revenue, expenditure, debt, and the public sector workforce that delivers it —
            drawn entirely from the Australian Bureau of Statistics' Government Finance
            Statistics. Full parity companion to the interactive dashboard: every chart here
            mirrors one in the full app.
          </p>
          <div className="hero-links">
            <a className="hero-btn primary" href={STREAMLIT_URL} target="_blank" rel="noreferrer">Open the full dashboard →</a>
            <a className="hero-btn secondary" href={REPO_URL} target="_blank" rel="noreferrer">View source on GitHub</a>
          </div>
        </header>

        <Folio number="01" title="Budget flow" sub="How $1,030.5b in total expenses splits across the eleven COFOG-A functions of government.">
          <div className="chart-wrap">
            <ResponsiveContainer width="100%" height={460}>
              <Sankey
                data={D.sankeyData}
                node={<SankeyNode />}
                link={{ stroke: BRASS, strokeOpacity: 0.25 }}
                nodePadding={22}
                margin={{ top: 10, right: 190, bottom: 10, left: 190 }}
              >
                <Tooltip contentStyle={tooltipStyle} formatter={(v) => [`$${v}b`, 'Allocation']} />
              </Sankey>
            </ResponsiveContainer>
          </div>
          <AuditStamp label="ABS COFOG-A classification, 2024-25" />
        </Folio>

        <Folio number="02" title="Category breakdown" sub="Year-over-year change per function, 2023-24 → 2024-25 — real dollar movement, not just share-of-total.">
          <div className="chart-wrap">
            <ResponsiveContainer width="100%" height={340}>
              <BarChart data={yoyBars} margin={{ top: 10, right: 16, bottom: 60, left: 0 }}>
                <CartesianGrid stroke={HAIR} vertical={false} />
                <XAxis dataKey="category" tick={{ ...monoTick, fontSize: 10.5 }} angle={-32} textAnchor="end" interval={0} axisLine={{ stroke: HAIR }} tickLine={false} />
                <YAxis tick={monoTick} axisLine={false} tickLine={false} width={44} />
                <Tooltip contentStyle={tooltipStyle} formatter={(v) => [`$${v}b`]} />
                <Legend wrapperStyle={{ fontFamily: 'Inter', fontSize: 13 }} />
                <Bar dataKey="2023-24" fill="#C9CFC9" radius={[2, 2, 0, 0]} />
                <Bar dataKey="2024-25" fill={INK} radius={[2, 2, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
          <AuditStamp label="ABS Government Finance Statistics, Annual 2024-25" />
        </Folio>

        <Folio number="03" title="Revenue & expenses, ten years in the ledger" sub="Revenue caught up to expenses through the pandemic recovery and the 2022-23 commodity-price surge — but 2024-25 tipped back into deficit.">
          <div className="chart-wrap">
            <ResponsiveContainer width="100%" height={280}>
              <LineChart data={D.fiscalSeries} margin={{ top: 10, right: 16, bottom: 4, left: 0 }}>
                <CartesianGrid stroke={HAIR} vertical={false} />
                <XAxis dataKey="year" tick={monoTick} axisLine={{ stroke: HAIR }} tickLine={false} />
                <YAxis tick={monoTick} axisLine={false} tickLine={false} width={50} />
                <Tooltip contentStyle={tooltipStyle} />
                <Legend wrapperStyle={{ fontFamily: 'Inter', fontSize: 13 }} />
                <Line type="monotone" dataKey="revenue" name="Revenue ($b)" stroke={INK} strokeWidth={2.5} dot={{ r: 3 }} />
                <Line type="monotone" dataKey="expenses" name="Expenses ($b)" stroke={RED} strokeWidth={2.5} dot={{ r: 3 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
          <div className="chart-wrap" style={{ marginTop: 16 }}>
            <ResponsiveContainer width="100%" height={220}>
              <BarChart data={D.fiscalSeries} margin={{ top: 10, right: 16, bottom: 4, left: 0 }}>
                <CartesianGrid stroke={HAIR} vertical={false} />
                <XAxis dataKey="year" tick={monoTick} axisLine={{ stroke: HAIR }} tickLine={false} />
                <YAxis tick={monoTick} axisLine={false} tickLine={false} width={50} />
                <Tooltip contentStyle={tooltipStyle} formatter={(v) => [`$${v}b`, 'Net operating balance']} />
                <Bar dataKey="nob" name="Net operating balance ($b)" radius={[2, 2, 0, 0]}>
                  {D.fiscalSeries.map((d, i) => <Rectangle key={i} fill={d.nob >= 0 ? INK : RED} />)}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div className="stat-row">
            <Stat label="Net Operating Balance" prefix="$" suffix="b" target={-8.2} negative start={heroRevealed} />
            <Stat label="Revenue growth, 10yr" suffix="%" target={((1022.4 - 576.0) / 576.0) * 100} decimals={0} start={heroRevealed} />
          </div>
          <AuditStamp label="ABS Government Finance Statistics, Annual 2024-25" />
        </Folio>

        <Folio number="04" title="Debt & net worth" sub="Net debt has grown faster than net worth since 2019-20, driven by pandemic-era borrowing that has not since unwound.">
          <div className="chart-wrap">
            <ResponsiveContainer width="100%" height={260}>
              <LineChart data={D.netWorthDebt} margin={{ top: 10, right: 16, bottom: 4, left: 0 }}>
                <CartesianGrid stroke={HAIR} vertical={false} />
                <XAxis dataKey="year" tick={monoTick} axisLine={{ stroke: HAIR }} tickLine={false} />
                <YAxis tick={monoTick} axisLine={false} tickLine={false} width={50} />
                <Tooltip contentStyle={tooltipStyle} />
                <Legend wrapperStyle={{ fontFamily: 'Inter', fontSize: 13 }} />
                <Line type="monotone" dataKey="netWorth" name="Net worth ($b)" stroke={INK} strokeWidth={2.5} dot={{ r: 3 }} />
                <Line type="monotone" dataKey="netDebt" name="Net debt ($b)" stroke={RED} strokeWidth={2.5} dot={{ r: 3 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
          <div className="chart-wrap" style={{ marginTop: 16 }}>
            <ResponsiveContainer width="100%" height={220}>
              <BarChart data={D.netWorthDebt} margin={{ top: 10, right: 16, bottom: 4, left: 0 }}>
                <CartesianGrid stroke={HAIR} vertical={false} />
                <XAxis dataKey="year" tick={monoTick} axisLine={{ stroke: HAIR }} tickLine={false} />
                <YAxis tick={monoTick} axisLine={false} tickLine={false} width={44} unit="%" />
                <Tooltip contentStyle={tooltipStyle} formatter={(v) => [`${v}%`, 'Net debt / GDP']} />
                <Bar dataKey="netDebtPctGdp" fill={BRASS} radius={[2, 2, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div className="stat-row">
            <Stat label="Net Debt, % of GDP" suffix="%" target={34.4} start={heroRevealed} />
          </div>
          <AuditStamp label="ABS Government Finance Statistics, Annual 2024-25" />
        </Folio>

        <Folio number="05" title="Growth drivers" sub="What drove the $70.8b increase in expenses in 2024-25, and where 2024-25 revenue came from.">
          <div className="chart-wrap">
            <ResponsiveContainer width="100%" height={260}>
              <BarChart data={D.expenseGrowthDrivers} layout="vertical" margin={{ top: 10, right: 24, bottom: 4, left: 8 }}>
                <CartesianGrid stroke={HAIR} horizontal={false} />
                <XAxis type="number" tick={monoTick} axisLine={{ stroke: HAIR }} tickLine={false} />
                <YAxis type="category" dataKey="driver" tick={{ fill: INK, fontSize: 11.5, fontFamily: 'Inter' }} width={220} axisLine={false} tickLine={false} />
                <Tooltip contentStyle={tooltipStyle} formatter={(v) => [`$${v}b`, 'Contribution']} />
                <Bar dataKey="contributionBillion" fill={INK} radius={[0, 2, 2, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div className="ledger-table" style={{ marginTop: 20 }}>
            <div className="ledger-row ledger-head">
              <span>Revenue component</span><span>% of revenue</span><span>Growth %</span>
            </div>
            {D.revenueBreakdown.map(r => (
              <div className="ledger-row" key={r.component}>
                <span>{r.component}</span>
                <span>{r.pctOfRevenue !== null ? `${r.pctOfRevenue}%` : '—'}</span>
                <span className={r.growthPct < 0 ? 'neg-text' : ''}>{r.growthPct > 0 ? '+' : ''}{r.growthPct}%</span>
              </div>
            ))}
          </div>
          <AuditStamp label="ABS Government Finance Statistics, Annual 2024-25" />
        </Folio>

        <Folio number="06" title="Growth & outlook" sub="Fastest-moving categories, the structural balance between revenue and expense growth, and two linear trend extrapolations shown with their fit quality (R²) rather than hidden.">
          <div className="chart-wrap">
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={[...D.categoryGrowth].reverse()} layout="vertical" margin={{ top: 10, right: 24, bottom: 4, left: 8 }}>
                <CartesianGrid stroke={HAIR} horizontal={false} />
                <XAxis type="number" tick={monoTick} axisLine={{ stroke: HAIR }} tickLine={false} unit="%" />
                <YAxis type="category" dataKey="category" tick={{ fill: INK, fontSize: 11.5, fontFamily: 'Inter' }} width={200} axisLine={false} tickLine={false} />
                <Tooltip contentStyle={tooltipStyle} formatter={(v) => [`${v}%`, '% change in $ allocated']} />
                <Bar dataKey="changePct" radius={[0, 2, 2, 0]}>
                  {[...D.categoryGrowth].reverse().map((d, i) => <Rectangle key={i} fill={d.changePct >= 0 ? INK : RED} />)}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div className="note">
            Environmental protection and Economic affairs are the only categories that shrank
            in real dollar terms, 2023-24 → 2024-25.
          </div>

          <h3 className="sub-head">Net debt (% GDP) — historical + 5-year linear trend extrapolation</h3>
          <div className="chart-wrap">
            <ResponsiveContainer width="100%" height={240}>
              <ComposedChart data={D.netDebtProjection} margin={{ top: 10, right: 16, bottom: 4, left: 0 }}>
                <CartesianGrid stroke={HAIR} vertical={false} />
                <XAxis dataKey="year" tick={monoTick} axisLine={{ stroke: HAIR }} tickLine={false} />
                <YAxis tick={monoTick} axisLine={false} tickLine={false} width={44} unit="%" />
                <Tooltip contentStyle={tooltipStyle} formatter={(v) => [`${v.toFixed(1)}%`]} />
                <Area type="monotone" dataKey={(d) => d.isProjection ? null : d.value} name="Historical" stroke={INK} fill={INK} fillOpacity={0.06} strokeWidth={2.5} connectNulls={false} />
                <Line type="monotone" dataKey={(d) => d.isProjection ? d.value : null} name="Trend extrapolation" stroke={BRASS} strokeWidth={2.5} strokeDasharray="6 4" dot={{ r: 3 }} connectNulls />
              </ComposedChart>
            </ResponsiveContainer>
          </div>
          <div className="note">Linear fit R² = {D.netDebtR2.toFixed(2)} — a moderate historical trend, still only a direction indicator, not a forecast.</div>

          <h3 className="sub-head">Net operating balance — historical + 5-year linear trend extrapolation</h3>
          <div className="chart-wrap">
            <ResponsiveContainer width="100%" height={240}>
              <BarChart data={D.nobProjection} margin={{ top: 10, right: 16, bottom: 4, left: 0 }}>
                <CartesianGrid stroke={HAIR} vertical={false} />
                <XAxis dataKey="year" tick={monoTick} axisLine={{ stroke: HAIR }} tickLine={false} />
                <YAxis tick={monoTick} axisLine={false} tickLine={false} width={50} />
                <Tooltip contentStyle={tooltipStyle} formatter={(v) => [`$${v.toFixed(1)}b`]} />
                <Bar dataKey="value" radius={[2, 2, 0, 0]}>
                  {D.nobProjection.map((d, i) => <Rectangle key={i} fill={d.isProjection ? BRASS : INK} />)}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div className="note warn">
            ⚠️ Linear fit R² = {D.nobR2.toFixed(3)} — essentially no linear relationship with time.
            Net operating balance swings on annual policy/economic shocks (e.g. COVID in 2020-21),
            not a smooth trend. Read the extrapolation line as noise, not signal.
          </div>
          <AuditStamp label="Linear regression (scikit-learn), fit on ABS historical figures 2015-16 to 2024-25" />
        </Folio>

        <Folio number="07" title="Who keeps the ledger" sub="2,597,300 people are employed across Commonwealth, state, and local government.">
          <div className="chart-wrap">
            <ResponsiveContainer width="100%" height={240}>
              <BarChart data={D.employmentNational} margin={{ top: 10, right: 16, bottom: 4, left: 0 }}>
                <CartesianGrid stroke={HAIR} vertical={false} />
                <XAxis dataKey="level" tick={monoTick} axisLine={{ stroke: HAIR }} tickLine={false} />
                <YAxis tick={monoTick} axisLine={false} tickLine={false} width={44} unit="%" />
                <Tooltip contentStyle={tooltipStyle} />
                <Legend wrapperStyle={{ fontFamily: 'Inter', fontSize: 13 }} />
                <Bar dataKey="jobsGrowthPct" name="Jobs growth %" fill={INK} radius={[2, 2, 0, 0]} />
                <Bar dataKey="wagesGrowthPct" name="Wages growth %" fill={RED} radius={[2, 2, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div className="note">
            Where the wages bar exceeds the jobs bar, average pay per job rose — a cost-intensity
            signal, not a labour productivity measure (no output data exists to compute genuine
            productivity here).
          </div>

          <h3 className="sub-head">Employee jobs by state/territory and level of government, Jun-25</h3>
          <div className="chart-wrap">
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={D.jobsByState} margin={{ top: 10, right: 16, bottom: 4, left: 0 }}>
                <CartesianGrid stroke={HAIR} vertical={false} />
                <XAxis dataKey="state" tick={monoTick} axisLine={{ stroke: HAIR }} tickLine={false} />
                <YAxis tick={monoTick} axisLine={false} tickLine={false} width={44} />
                <Tooltip contentStyle={tooltipStyle} />
                <Legend wrapperStyle={{ fontFamily: 'Inter', fontSize: 13 }} />
                <Bar dataKey="Commonwealth" stackId="a" fill={BRASS} />
                <Bar dataKey="State" stackId="a" fill={INK} />
                <Bar dataKey="Local" stackId="a" fill={SLATE} radius={[2, 2, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <h3 className="sub-head">Cash wages by industry, 2024-25</h3>
          <div className="chart-wrap">
            <ResponsiveContainer width="100%" height={340}>
              <BarChart data={D.employmentByIndustry} layout="vertical" margin={{ top: 10, right: 24, bottom: 4, left: 8 }}>
                <CartesianGrid stroke={HAIR} horizontal={false} />
                <XAxis type="number" tick={monoTick} axisLine={{ stroke: HAIR }} tickLine={false} />
                <YAxis type="category" dataKey="industry" tick={{ fill: INK, fontSize: 10.5, fontFamily: 'Inter' }} width={210} axisLine={false} tickLine={false} />
                <Tooltip contentStyle={tooltipStyle} formatter={(v) => [`$${v}m`, 'Cash wages']} />
                <Bar dataKey="wagesM" fill={INK} radius={[0, 2, 2, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div className="stat-row">
            <Stat label="Total public sector jobs" suffix="k" target={2597.3} start={heroRevealed} />
            <Stat label="Total cash wages" prefix="$" suffix="b" target={249.5} start={heroRevealed} />
            <Stat label="Avg wage per job" prefix="$" suffix="k" target={96.1} start={heroRevealed} />
          </div>
          <AuditStamp label="ABS Public Sector Employment and Earnings, cat. 6248.0.55.002" />
        </Folio>

        <footer className="footer">
          <span>Every figure on this page traces to a cited ABS release — see the full dashboard for sourcing, methodology, and limitations.</span>
          <a href={STREAMLIT_URL} target="_blank" rel="noreferrer">govt-budget-transparency-dashboard →</a>
        </footer>
      </div>
    </>
  )
}
