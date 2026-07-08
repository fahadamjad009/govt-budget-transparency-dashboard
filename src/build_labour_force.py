"""
Transcribes official ABS Public Sector Employment and Earnings figures
(cat. 6248.0.55.002, 2024-25 financial year, released 06/11/2025) into
clean CSVs. All figures manually sourced from the ABS release page table,
no estimation or fabrication.

Source: https://www.abs.gov.au/statistics/labour/employment-and-unemployment/
        public-sector-employment-and-earnings/latest-release
"""
import pandas as pd

def build_employment_by_state():
    # employee jobs ('000) and cash wages ($m), by state/territory and level
    # of government. Jobs relate to June of the given year; wages relate to
    # the full financial year. ACT local government is combined into ACT
    # state figures per ABS convention (ACT Legislative Assembly holds both
    # state and local responsibilities).
    rows = [
        # state, level, jobs_jun24, jobs_jun25, wages_2023_24, wages_2024_25
        ("NSW", "Commonwealth", 86.9, 91.6, 8938.0, 9726.1),
        ("NSW", "State", 557.3, 566.1, 52348.7, 55444.1),
        ("NSW", "Local", 63.4, 65.2, 5052.8, 5478.4),
        ("Vic", "Commonwealth", 62.9, 65.6, 6362.8, 6847.8),
        ("Vic", "State", 485.9, 493.2, 42980.4, 45733.2),
        ("Vic", "Local", 57.4, 58.1, 4028.2, 4209.2),
        ("Qld", "Commonwealth", 50.0, 52.9, 5004.7, 5485.3),
        ("Qld", "State", 406.2, 425.4, 39433.9, 42841.7),
        ("Qld", "Local", 48.1, 48.8, 4114.1, 4409.3),
        ("SA", "Commonwealth", 21.3, 23.2, 2151.3, 2433.8),
        ("SA", "State", 143.2, 149.3, 11951.9, 12703.3),
        ("SA", "Local", 11.6, 11.7, 958.8, 1014.4),
        ("WA", "Commonwealth", 19.0, 20.0, 1911.3, 2097.8),
        ("WA", "State", 219.8, 232.3, 19544.8, 21697.7),
        ("WA", "Local", 25.5, 26.5, 1775.7, 1927.3),
        ("Tas", "Commonwealth", 6.0, 5.8, 566.3, 586.9),
        ("Tas", "State", 54.8, 56.3, 4740.9, 5093.2),
        ("Tas", "Local", 4.6, 4.8, 323.4, 344.7),
        ("NT", "Commonwealth", 9.5, 9.7, 901.9, 951.8),
        ("NT", "State", 31.6, 32.4, 3290.4, 3475.8),
        ("NT", "Local", 3.0, 3.0, 192.6, 194.2),
        ("ACT", "Commonwealth", 109.8, 117.1, 11482.3, 12728.6),
        ("ACT", "State", 37.5, 38.2, 3741.5, 4088.7),
        # ACT has no separate local government line (combined into State)
    ]
    df = pd.DataFrame(rows, columns=[
        "state", "level_of_government", "employee_jobs_thousands_jun24",
        "employee_jobs_thousands_jun25", "cash_wages_millions_2023_24",
        "cash_wages_millions_2024_25"
    ])
    df.to_csv("data/public_sector_employment_by_state.csv", index=False)
    return df

def build_employment_by_level_national():
    # national totals by level of government, for the headline productivity
    # comparison against existing GFS employee-expense figures
    rows = [
        ("Commonwealth", 365.4, 385.9, 37318.6, 40858.0),
        ("State", 1936.4, 1993.4, 178032.5, 191077.5),
        ("Local", 213.5, 218.0, 16445.5, 17577.6),
        ("Total Public Sector", 2515.3, 2597.3, 231796.6, 249513.0),
    ]
    df = pd.DataFrame(rows, columns=[
        "level_of_government", "employee_jobs_thousands_jun24",
        "employee_jobs_thousands_jun25", "cash_wages_millions_2023_24",
        "cash_wages_millions_2024_25"
    ])
    df["jobs_growth_pct"] = (
        (df["employee_jobs_thousands_jun25"] - df["employee_jobs_thousands_jun24"])
        / df["employee_jobs_thousands_jun24"] * 100
    ).round(2)
    df["wages_growth_pct"] = (
        (df["cash_wages_millions_2024_25"] - df["cash_wages_millions_2023_24"])
        / df["cash_wages_millions_2023_24"] * 100
    ).round(2)
    df["avg_wage_per_job_2024_25_thousands"] = (
        df["cash_wages_millions_2024_25"] * 1000
        / (df["employee_jobs_thousands_jun25"] * 1000)
    ).round(1)
    df.to_csv("data/public_sector_employment_national.csv", index=False)
    return df

def build_employment_by_industry():
    rows = [
        ("Electricity, gas, water and waste services", 62.3, 66.4, 7771.7, 9144.3),
        ("Construction", 8.9, 9.2, 892.0, 993.3),
        ("Transport, postal and warehousing", 78.0, 79.3, 8478.9, 9062.7),
        ("Information media and telecommunications", 16.8, 16.5, 1936.5, 1945.2),
        ("Financial and insurance services", 18.4, 19.8, 2253.7, 2498.9),
        ("Rental, hiring and real estate services", 7.6, 7.7, 664.6, 704.5),
        ("Professional, scientific and technical services", 38.7, 39.6, 3803.1, 4149.3),
        ("Public administration and safety", 849.4, 880.6, 83444.4, 90195.8),
        ("Education and training", 753.9, 768.3, 57904.5, 61399.3),
        ("Health care and social assistance", 642.4, 668.7, 61684.5, 66169.2),
        ("Arts and recreation services", 22.8, 23.6, 1568.5, 1634.5),
        ("Other industries", 15.9, 17.6, 1394.2, 1616.1),
    ]
    df = pd.DataFrame(rows, columns=[
        "industry", "employee_jobs_thousands_jun24",
        "employee_jobs_thousands_jun25", "cash_wages_millions_2023_24",
        "cash_wages_millions_2024_25"
    ])
    df.to_csv("data/public_sector_employment_by_industry.csv", index=False)
    return df

def main():
    by_state = build_employment_by_state()
    national = build_employment_by_level_national()
    by_industry = build_employment_by_industry()

    print("Public sector employment by state/level built:")
    print(by_state.to_string(index=False))
    print("\nNational level-of-government summary:")
    print(national.to_string(index=False))
    print("\nBy industry (top 3 by 2024-25 wages):")
    print(by_industry.sort_values("cash_wages_millions_2024_25", ascending=False).head(3).to_string(index=False))

if __name__ == "__main__":
    main()
