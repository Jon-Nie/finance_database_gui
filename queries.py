from utils import db
import pandas as pd
import numpy as np

con = db.connection
cur = db.cursor

def get_stock_list():

    data = cur.execute("SELECT ticker, yahoo_name FROM securities WHERE id IN (SELECT security_id FROM companies)").fetchall()
    for index, item in enumerate(data):
        if item[1] is None:
            data[index] = (item[0], "None")

    return data

def get_security_id(ticker):
    security_id = cur.execute("SELECT id FROM securities WHERE ticker = ?", (ticker,)).fetchone()[0]

    return security_id

def get_price_data(ticker) -> pd.DataFrame:
    security_id = cur.execute("SELECT id FROM securities WHERE ticker = ?", (ticker,)).fetchone()[0]
    data = cur.execute(
        """
        SELECT ts, close, adj_close, simple_return, split_ratio, dividends FROM security_prices 
        WHERE security_id = ?
        """,
        (security_id, )
    ).fetchall()

    df = pd.DataFrame(
        data = data,
        columns = ["date", "close", "adj_close", "simple_return", "split", "dividends"]
    )

    df.set_index("date", drop=True, inplace=True)

    return df

def get_fundamental_variables(source) -> list:
    data = cur.execute(
        f"""
        SELECT fundamental_variables_{source}.name, financial_statement_types.name
        FROM fundamental_variables_{source} JOIN financial_statement_types
        ON fundamental_variables_{source}.statement_id = financial_statement_types.id
        """
    ).fetchall()

    data = {item[0]: item[1] for item in data}   

    return data

def get_fundamental_data(ticker, variable, source) -> list:
    security_id = cur.execute("SELECT id FROM securities WHERE ticker = ?", (ticker,)).fetchone()[0]
    variable_id = cur.execute(f"SELECT id FROM fundamental_variables_{source} WHERE name = ?", (variable,)).fetchone()[0]
    data = cur.execute(
        f"""
        SELECT ts, value FROM fundamental_data_{source}
        WHERE security_id = ?
        AND variable_id = ?
        AND quarter != 0
        """,
        (security_id, variable_id)
    ).fetchall()

    return data

def get_company_profile(ticker) -> dict:
    security_id = cur.execute("SELECT id FROM securities WHERE ticker = ?", (ticker,)).fetchone()[0]
    data = cur.execute(
        """
        SELECT
        securities.cik,
        securities.ticker,
        securities.isin,
        securities.yahoo_name AS name,
        securities.description,
        securities.logo,
        (SELECT currencies.abbr FROM currencies WHERE id = securities.currency_id) AS currency,
        DATE(securities.prices_updated, "unixepoch") as prices_updated,
        DATE(companies.macrotrends_fundamentals_updated, "unixepoch") as fundamentals_updated,
        (SELECT sic_industries.name FROM sic_industries WHERE id = companies.sic_industry_id) AS sic_industry,
        (SELECT sic_divisions.name FROM sic_divisions WHERE id = (
            SELECT sic_industries.division_id FROM sic_industries WHERE id = companies.sic_industry_id
        )
        ) AS sic_division,
        (SELECT gics_industries.name FROM gics_industries WHERE id = companies.gics_industry_id) AS gics_industry,
        (SELECT gics_sectors.name FROM gics_sectors WHERE id = (
            SELECT gics_industries.sector_id FROM gics_industries WHERE id = companies.gics_industry_id
        )
        ) AS gics_sector,
        companies.website,
        (SELECT countries.name FROM countries WHERE id = companies.country_id) AS country,
        (SELECT countries.flag_small FROM countries WHERE id = companies.country_id) AS country_flag,
        (SELECT cities.name FROM cities WHERE id = companies.city_id) AS city,
        companies.address1,
        companies.address2,
        companies.zip,
        companies.employees,
        companies.fiscal_year_end
        FROM 
        securities JOIN companies
        ON securities.id = companies.security_id
        WHERE
        companies.security_id = ?
        """,
        (security_id,)
    ).fetchall()[0]

    dct = {}

    for index, col in enumerate(cur.description):
        dct[col[0]] = data[index]

    return dct

def get_sic_division_companies(division) -> list:
    data = cur.execute(
        """
        SELECT *
        FROM
        securities JOIN companies
        ON securities.id = companies.security_id
        WHERE companies.sic_industry_id IN (
            SELECT id FROM sic_industries WHERE division_id IN (
                SELECT id FROM sic_divisions WHERE name = ?
            )
        )
        """,
        (division,)

    ).fetchall()

    return data

def get_sic_industry_companies(industry) -> list:
    data = cur.execute(
        """
        SELECT *
        FROM
        securities JOIN companies
        ON securities.id = companies.security_id
        WHERE companies.sic_industry_id = (
            SELECT id FROM sic_industries WHERE name = ?
        )
        """,
        (industry, )
    ).fetchall()

    return data

def get_gics_sector_companies(sector) -> list:
    data = cur.execute(
        """
        SELECT *
        FROM
        securities JOIN companies
        ON securities.id = companies.security_id
        WHERE companies.gics_industry_id IN (
            SELECT id FROM gics_industries WHERE sector_id IN (
                SELECT id FROM gics_sectors WHERE name = ?
            )
        )
        """,
        (sector, )
    ).fetchall()

    return data

def get_gics_industry_companies(industry) -> list:
    data = cur.execute(
        """
        SELECT *
        FROM
        securities JOIN companies
        ON securities.id = companies.security_id
        WHERE companies.gics_industry_id = (
            SELECT id FROM gics_industries WHERE name = ?
        )
        """,
        (industry, )
    ).fetchall()

    return data

def get_executives(ticker) -> list:
    security_id = cur.execute("SELECT id FROM securities WHERE ticker = ?", (ticker, )).fetchone()[0]
    data = cur.execute(
        """
        SELECT 
        executives.name as name,
        executives.age as age,
        executives.born as born,
        executive_positions.name as position,
        company_executive_match.salary as salary
        FROM 
        executives JOIN company_executive_match JOIN executive_positions
        ON 
        executives.id = company_executive_match.executive_id
        AND company_executive_match.position_id = executive_positions.id
        WHERE security_id = ?
        """,
        (security_id,)
    ).fetchall()

    return data

def get_analyst_recommendations(ticker) -> list:
    data = cur.execute(
        """
        SELECT a.name, DATE(ar.ts, "unixepoch") date, r1.name old, r2.name new, r3.name change 
        FROM 
        analysts a JOIN analyst_recommendations ar JOIN ratings r1 JOIN ratings r2 JOIN ratings r3
        ON 
        a.id = ar.analyst_id
        AND r1.id = ar.old
        AND r2.id = ar.new
        AND r3.id = ar.change
        WHERE 
        ar.security_id = (
        SELECT id FROM securities WHERE ticker = ?
        )
        """,
        (ticker,)
    ).fetchall()

    return data

def get_recommendation_trend(ticker) -> pd.DataFrame:
    security_id = cur.execute("SELECT id FROM securities WHERE ticker = ?", (ticker,)).fetchone()[0]
    data = cur.execute(
        """
        SELECT DATE(month, "unixepoch"), number, average, strong_buy, buy, hold, sell, strong_sell
        FROM recommendation_trend
        WHERE security_id = ?
        ORDER BY ts DESC
        """,
        (security_id,)
    ).fetchall()

    df = pd.DataFrame(
        data = data,
        columns = ["date", "number", "average", "strong_buy", "buy", "hold", "sell", "strong_sell"]
    )
    df.set_index("date", drop=True, inplace=True)
    df.index = pd.to_datetime(df.index)
    df.sort_index(inplace=True)

    return df

def get_sic_divisions() -> list:
    data = cur.execute(
        """
        SELECT * FROM sic_divisions
        """
    ).fetchall()

    return data

def get_sic_industries() -> list:
    data = cur.execute(
        """
        SELECT * FROM sic_industries
        """
    ).fetchall()

    return data

def get_gics_sectors() -> list:
    data = cur.execute(
        """
        SELECT * FROM gics_sectors
        """
    ).fetchall()

    return data

def get_gics_industries() -> list:
    data = cur.execute(
        """
        SELECT * FROM gics_industries
        """
    ).fetchall()

    return data

def get_sic_industry_competitors(ticker) -> list:
    security_id = cur.execute("SELECT id FROM securities WHERE ticker = ?", (ticker, )).fetchone()[0]
    data = cur.execute(
        """
        SELECT
        securities.ticker as ticker,
        securities.yahoo_name as name,
        countries.name as country
        FROM 
        securities JOIN companies JOIN countries
        ON
        securities.id = companies.security_id
        AND companies.country_id = countries.id
        WHERE sic_industry_id = (
            SELECT sic_industry_id FROM companies WHERE security_id = ?
        )
        """,
        (security_id,)
    ).fetchall()

    return data

def get_gics_industry_competitors(ticker) -> list:
    security_id = cur.execute("SELECT id FROM securities WHERE ticker = ?", (ticker, )).fetchone()[0]
    data = cur.execute(
        """
        SELECT
        securities.ticker as ticker,
        securities.yahoo_name as name,
        countries.name as country
        FROM 
        securities JOIN companies JOIN countries
        ON
        securities.id = companies.security_id
        AND companies.country_id = countries.id
        WHERE gics_industry_id = (
            SELECT gics_industry_id FROM companies WHERE security_id = ?
        )
        AND securities.id != ?
        ORDER BY securities.ticker
        """,
        (security_id, security_id)
    ).fetchall()

    return data

def get_executives(ticker) -> list:
    security_id = cur.execute("SELECT id FROM securities WHERE ticker = ?", (ticker, )).fetchone()[0]
    data = cur.execute(
        """
        SELECT 
        executives.name as name,
        executives.age as age,
        executives.born as born,
        executive_positions.name as position,
        company_executive_match.salary as salary
        FROM 
        executives JOIN company_executive_match JOIN executive_positions
        ON 
        executives.id = company_executive_match.executive_id
        AND company_executive_match.position_id = executive_positions.id
        WHERE security_id = ?
        """,
        (security_id,)
    ).fetchall()

    return data

def get_major_holders() -> list:
    return


def get_stock_data(ticker=None, isin=None):
    if isin and not ticker:
        ticker = cur.execute("SELECT ticker FROM securities WHERE isin = ?", (isin,)).fetchone()[0]
    profile = get_company_profile(ticker)
    profile = {k: (v if v != None else "") for k, v in profile.items()}
    if isinstance(profile['employees'], int):
        profile['employees'] = f"{profile['employees']:,}".replace(",", ".")

    executives = get_executives(ticker)
    recommendation_trend = get_recommendation_trend(ticker)
    prices = get_price_data(ticker)

    macrotrends_variables = get_fundamental_variables("macrotrends")
    series_list = []
    for variable in macrotrends_variables.keys():
        series = get_fundamental_data(ticker, variable, "macrotrends")
        if len(series) == 0:
            series = pd.Series(dtype = "float64")
        else:
            series = list(zip(*series))
            series = pd.Series(index = series[0], data = series[1])
        series.name = variable
        series_list.append(series)

    fundamentals = pd.concat(series_list, axis=1)
    fundamentals = fundamentals.sort_index()
    for variable in fundamentals.columns:
        if macrotrends_variables[variable] == "balance sheet":
            fundamentals[f"{variable} ttm"] = fundamentals[variable].rolling(4, min_periods=4).mean()
        else:
            fundamentals[f"{variable} ttm"] = fundamentals[variable].rolling(4, min_periods=4).sum()
    
    for scope in ("", " ttm"):
        fundamentals[f"revenue growth{scope}"]  = (fundamentals[f"revenue{scope}"].iloc[-1] / fundamentals[f"revenue{scope}"].iloc[-12]) ** (1/3) - 1
        fundamentals[f"operating income growth{scope}"] = (fundamentals[f"operating income{scope}"].iloc[-1] / fundamentals[f"operating income{scope}"].iloc[-12]) ** (1/3) - 1
        fundamentals[f"net income growth{scope}"] = (fundamentals[f"net income{scope}"].iloc[-1] / fundamentals[f"net income{scope}"].iloc[-12]) ** (1/3) - 1
        fundamentals[f"eps growth{scope}"] = (fundamentals[f"diluted eps{scope}"].iloc[-1] / fundamentals[f"diluted eps{scope}"].iloc[-12]) ** (1/3) - 1
        fundamentals[f"gross margin{scope}"] = fundamentals[f"gross profit{scope}"] / fundamentals[f"revenue{scope}"]
        fundamentals[f"operating margin{scope}"] = fundamentals[f"operating income{scope}"] / fundamentals[f"revenue{scope}"]
        fundamentals[f"net margin{scope}"] = fundamentals[f"net income{scope}"] / fundamentals[f"revenue{scope}"]
        fundamentals[f"roa{scope}"] = fundamentals[f"net income{scope}"] / fundamentals[f"total assets{scope}"]
        fundamentals[f"roe{scope}"] = fundamentals[f"net income{scope}"] / fundamentals[f"total shareholders equity{scope}"]
        fundamentals[f"reinvestment rate{scope}"] = 1+(fundamentals[f"total dividends paid{scope}"].replace(np.NaN, 0)+fundamentals[f"total stock issued/repurchased{scope}"].replace(np.NaN, 0))  / fundamentals[f"net income{scope}"]
        fundamentals[f"equity share{scope}"] = fundamentals[f"total shareholders equity{scope}"] / fundamentals[f"total assets{scope}"]
        fundamentals[f"debt/fcf{scope}"] = ((fundamentals[f"total current liabilities{scope}"] + fundamentals[f"non-current debt{scope}"]) / 
                                            (fundamentals[f"net income{scope}"] +
                                            fundamentals[f"depreciation and amortization{scope}"] +
                                            fundamentals[f"total change in assets/liabilities{scope}"] +
                                            fundamentals[f"capital expenditures{scope}"]))
        fundamentals[f"interest coverage{scope}"] = (fundamentals[f"operating income{scope}"]+fundamentals[f"depreciation and amortization{scope}"]) / fundamentals[f"non-operating income/expenses{scope}"]

    time_series = pd.concat([prices, fundamentals], axis=1)

    time_series.index = pd.to_datetime(time_series.index, unit="s")
    time_series = time_series.sort_index()

    time_series["split"] = time_series["split"].fillna(0)
    time_series["dividends"] = time_series["dividends"].fillna(0)

    for col in time_series.columns:
        if col in ("close", "adj_close", "split", "simple_return", "dividends"):
            continue
        time_series[col] = time_series[col].ffill()

    for variable in macrotrends_variables:
        time_series[variable] = time_series[variable].fillna(0)

    time_series["market_cap"] = time_series["close"] * time_series["diluted shares outstanding"]
    time_series["p/e"] = time_series["market_cap"] / time_series["net income ttm"]
    time_series["p/cf"] = time_series["market_cap"] / time_series["cashflow from operating activities ttm"]
    time_series["p/b"] = time_series["market_cap"] / time_series["total shareholders equity ttm"]
    time_series["p/s"] = time_series["market_cap"] / time_series["revenue ttm"]

    return {
        "profile": profile,
        "executives": executives,
        "recommendation_trend": recommendation_trend,
        "fundamentals": fundamentals,
        "time_series": time_series,
        "news": None
    }
