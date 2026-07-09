// All figures transcribed directly from this project's own source-of-truth
// CSVs (data/*.csv in the govt-budget-transparency-dashboard repo), which
// are themselves transcribed from official ABS releases. No estimation.

export const fiscalSeries = [
  { year: '2015-16', revenue: 576.0, expenses: 598.5, nob: -22.5 },
  { year: '2016-17', revenue: 607.7, expenses: 621.3, nob: -13.5 },
  { year: '2017-18', revenue: 655.2, expenses: 645.0, nob: 10.2 },
  { year: '2018-19', revenue: 694.0, expenses: 677.4, nob: 16.6 },
  { year: '2019-20', revenue: 681.7, expenses: 789.7, nob: -108.1 },
  { year: '2020-21', revenue: 728.0, expenses: 873.4, nob: -145.4 },
  { year: '2021-22', revenue: 831.5, expenses: 866.3, nob: -34.8 },
  { year: '2022-23', revenue: 923.3, expenses: 885.4, nob: 37.9 },
  { year: '2023-24', revenue: 978.2, expenses: 959.7, nob: 18.4 },
  { year: '2024-25', revenue: 1022.4, expenses: 1030.5, nob: -8.2 },
]

export const netWorthDebt = [
  { year: '2015-16', netWorth: 764.3, netDebt: 390.2, netDebtPctGdp: 23.4 },
  { year: '2016-17', netWorth: 884.3, netDebt: 403.8, netDebtPctGdp: 22.9 },
  { year: '2017-18', netWorth: 921.8, netDebt: 436.1, netDebtPctGdp: 23.6 },
  { year: '2018-19', netWorth: 799.7, netDebt: 476.9, netDebtPctGdp: 24.4 },
  { year: '2019-20', netWorth: 687.7, netDebt: 634.2, netDebtPctGdp: 31.9 },
  { year: '2020-21', netWorth: 679.4, netDebt: 789.0, netDebtPctGdp: 37.7 },
  { year: '2021-22', netWorth: 1011.6, netDebt: 778.7, netDebtPctGdp: 33.3 },
  { year: '2022-23', netWorth: 1208.1, netDebt: 783.8, netDebtPctGdp: 30.4 },
  { year: '2023-24', netWorth: 1385.2, netDebt: 846.6, netDebtPctGdp: 31.6 },
  { year: '2024-25', netWorth: 1380.0, netDebt: 954.9, netDebtPctGdp: 34.4 },
]

export const cofog2425 = [
  { category: 'Social protection', billion: 312.24, pct: 30.3 },
  { category: 'Health', billion: 208.16, pct: 20.2 },
  { category: 'Education', billion: 148.39, pct: 14.4 },
  { category: 'General public services', billion: 111.29, pct: 10.8 },
  { category: 'Public order and safety', billion: 52.56, pct: 5.1 },
  { category: 'Defence', billion: 50.49, pct: 4.9 },
  { category: 'Transport', billion: 47.4, pct: 4.6 },
  { category: 'Economic affairs', billion: 46.37, pct: 4.5 },
  { category: 'Environmental protection', billion: 20.61, pct: 2.0 },
  { category: 'Recreation, culture and religion', billion: 19.58, pct: 1.9 },
  { category: 'Housing and community amenities', billion: 13.4, pct: 1.3 },
]

export const cofog2324 = {
  'Social protection': 283.11, 'Health': 192.9, 'Education': 139.16,
  'General public services': 103.65, 'Public order and safety': 48.94,
  'Defence': 48.94, 'Transport': 43.19, 'Economic affairs': 47.03,
  'Environmental protection': 21.11, 'Recreation, culture and religion': 19.19,
  'Housing and community amenities': 13.44,
}

export const categoryGrowth = [
  { category: 'Social protection', changeBillion: 29.13, changePct: 10.3 },
  { category: 'Transport', changeBillion: 4.21, changePct: 9.7 },
  { category: 'Health', changeBillion: 15.26, changePct: 7.9 },
  { category: 'Public order and safety', changeBillion: 3.62, changePct: 7.4 },
  { category: 'General public services', changeBillion: 7.64, changePct: 7.4 },
  { category: 'Education', changeBillion: 9.23, changePct: 6.6 },
  { category: 'Defence', changeBillion: 1.55, changePct: 3.2 },
  { category: 'Recreation, culture and religion', changeBillion: 0.39, changePct: 2.0 },
  { category: 'Housing and community amenities', changeBillion: -0.04, changePct: -0.3 },
  { category: 'Economic affairs', changeBillion: -0.66, changePct: -1.4 },
  { category: 'Environmental protection', changeBillion: -0.5, changePct: -2.4 },
]

export const expenseGrowthDrivers = [
  { driver: 'Employee expenses', growthPct: 8.6, contributionBillion: 22.1, pctOfTotalGrowth: 31.3 },
  { driver: 'Social benefits to households in goods and services', growthPct: 12.3, contributionBillion: 20.6, pctOfTotalGrowth: 29.1 },
  { driver: 'Current monetary transfers to households', growthPct: 6.8, contributionBillion: 10.7, pctOfTotalGrowth: 15.1 },
  { driver: 'Use of goods and services', growthPct: 4.4, contributionBillion: 8.1, pctOfTotalGrowth: 11.4 },
  { driver: 'Interest expense', growthPct: 9.9, contributionBillion: 6.0, pctOfTotalGrowth: 8.5 },
]

export const revenueBreakdown = [
  { component: 'Taxation revenue', pctOfRevenue: 82.8, growthPct: 4.3 },
  { component: 'Royalty income', pctOfRevenue: null, growthPct: -21.2 },
]

export const netDebtProjection = [
  { year: '2015-16', value: 23.4, isProjection: false },
  { year: '2016-17', value: 22.9, isProjection: false },
  { year: '2017-18', value: 23.6, isProjection: false },
  { year: '2018-19', value: 24.4, isProjection: false },
  { year: '2019-20', value: 31.9, isProjection: false },
  { year: '2020-21', value: 37.7, isProjection: false },
  { year: '2021-22', value: 33.3, isProjection: false },
  { year: '2022-23', value: 30.4, isProjection: false },
  { year: '2023-24', value: 31.6, isProjection: false },
  { year: '2024-25', value: 34.4, isProjection: false },
  { year: '2025-26', value: 36.91, isProjection: true },
  { year: '2026-27', value: 38.28, isProjection: true },
  { year: '2027-28', value: 39.65, isProjection: true },
  { year: '2028-29', value: 41.02, isProjection: true },
  { year: '2029-30', value: 42.40, isProjection: true },
]
export const netDebtR2 = 0.602

export const nobProjection = [
  { year: '2015-16', value: -22.5, isProjection: false },
  { year: '2016-17', value: -13.5, isProjection: false },
  { year: '2017-18', value: 10.2, isProjection: false },
  { year: '2018-19', value: 16.6, isProjection: false },
  { year: '2019-20', value: -108.1, isProjection: false },
  { year: '2020-21', value: -145.4, isProjection: false },
  { year: '2021-22', value: -34.8, isProjection: false },
  { year: '2022-23', value: 37.9, isProjection: false },
  { year: '2023-24', value: 18.4, isProjection: false },
  { year: '2024-25', value: -8.2, isProjection: false },
  { year: '2025-26', value: -14.97, isProjection: true },
  { year: '2026-27', value: -13.16, isProjection: true },
  { year: '2027-28', value: -11.35, isProjection: true },
  { year: '2028-29', value: -9.54, isProjection: true },
  { year: '2029-30', value: -7.72, isProjection: true },
]
export const nobR2 = 0.00882

export const employmentNational = [
  { level: 'Commonwealth', jobsGrowthPct: 5.61, wagesGrowthPct: 9.48, avgWageK: 105.9 },
  { level: 'State', jobsGrowthPct: 2.94, wagesGrowthPct: 7.33, avgWageK: 95.9 },
  { level: 'Local', jobsGrowthPct: 2.11, wagesGrowthPct: 6.88, avgWageK: 80.6 },
]
export const employmentTotals = {
  jobsK: 2597.3, jobsGrowthPct: 3.26, wagesB: 249.513, wagesGrowthPct: 7.64, avgWageK: 96.1,
}

export const jobsByState = [
  { state: 'NSW', Commonwealth: 91.6, State: 566.1, Local: 65.2 },
  { state: 'Vic', Commonwealth: 65.6, State: 493.2, Local: 58.1 },
  { state: 'Qld', Commonwealth: 52.9, State: 425.4, Local: 48.8 },
  { state: 'WA', Commonwealth: 20.0, State: 232.3, Local: 26.5 },
  { state: 'SA', Commonwealth: 23.2, State: 149.3, Local: 11.7 },
  { state: 'ACT', Commonwealth: 117.1, State: 38.2, Local: 0 },
  { state: 'Tas', Commonwealth: 5.8, State: 56.3, Local: 4.8 },
  { state: 'NT', Commonwealth: 9.7, State: 32.4, Local: 3.0 },
]

export const employmentByIndustry = [
  { industry: 'Public administration and safety', wagesM: 90195.8 },
  { industry: 'Health care and social assistance', wagesM: 66169.2 },
  { industry: 'Education and training', wagesM: 61399.3 },
  { industry: 'Electricity, gas, water and waste services', wagesM: 9144.3 },
  { industry: 'Transport, postal and warehousing', wagesM: 9062.7 },
  { industry: 'Professional, scientific and technical services', wagesM: 4149.3 },
  { industry: 'Financial and insurance services', wagesM: 2498.9 },
  { industry: 'Information media and telecommunications', wagesM: 1945.2 },
  { industry: 'Arts and recreation services', wagesM: 1634.5 },
  { industry: 'Other industries', wagesM: 1616.1 },
  { industry: 'Construction', wagesM: 993.3 },
  { industry: 'Rental, hiring and real estate services', wagesM: 704.5 },
]

export const sankeyData = {
  nodes: [{ name: 'Total Government Expenses' }, ...cofog2425.map(c => ({ name: c.category }))],
  links: cofog2425.map((c, i) => ({ source: 0, target: i + 1, value: c.billion })),
}
