from utils import db
import pandas as pd
import numpy as np

con = db.connection
cur = db.cursor

def get_stock_list() -> list:
    data = cur.execute(
        "SELECT ticker, yahoo_name FROM securities WHERE id IN (SELECT DISTINCT security_id FROM companies)"
    ).fetchall()
    data_filtered = []
    for index, item in enumerate(data):
        if item[1] is None:
            continue
        data_filtered.append((item[0], item[1], "Stock"))
    return data_filtered

def get_company_profile(ticker) -> list:
    security_id = cur.execute("SELECT id FROM securities WHERE ticker = ?", (ticker,)).fetchone()[0]
    data = cur.execute(
        """
        SELECT
        securities.logo,
        securities.yahoo_name as name,
        securities.ticker,
        securities.isin,
        (SELECT countries.flag_small FROM countries WHERE id = companies.country_id) AS country_flag,
        (SELECT countries.name FROM countries WHERE id = companies.country_id) AS country,
        (companies.zip || ", " || (SELECT cities.name FROM cities WHERE id = companies.city_id)) AS city,
        companies.address1,
        companies.website,
        companies.employees,
        (SELECT gics_sectors.name FROM gics_sectors WHERE id = (
            SELECT gics_industries.sector_id FROM gics_industries WHERE id = companies.gics_industry_id
        )
        ) AS gics_sector,
        (SELECT gics_industries.name FROM gics_industries WHERE id = companies.gics_industry_id) AS gics_industry,
        (SELECT sic_divisions.name FROM sic_divisions WHERE id = (
            SELECT sic_industries.division_id FROM sic_industries WHERE id = companies.sic_industry_id
        )
        ) AS sic_division,
        (SELECT sic_industries.name FROM sic_industries WHERE id = companies.sic_industry_id) AS sic_industry,
        securities.description,
        DATE(securities.prices_updated, "unixepoch") as prices_updated,
        DATE(companies.macrotrends_fundamentals_updated, "unixepoch") as fundamentals_updated
        FROM 
        securities JOIN companies
        ON securities.id = companies.security_id
        WHERE
        companies.security_id = ?
        """,
        (security_id,)
    ).fetchall()[0]

    return list(data)

def get_news(ticker):
    security_id = cur.execute("SELECT id FROM securities WHERE ticker = ?", (ticker,)).fetchone()[0]
    data = cur.execute(
        """
        SELECT
        security_news.ts,
        news_source.name,
        security_news.header,
        security_news.url
        FROM security_news JOIN security_news_match JOIN news_source JOIN news_type
        ON
        security_news.id = security_news_match.news_id
        AND security_news.source_id = news_source.id
        AND security_news.type_id = (SELECT id FROM news_type WHERE name = "news")
        WHERE security_news_match.security_id = ?
        ORDER BY ts DESC
        """,
        (security_id,)
    ).fetchall()

    return data

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

def get_time_series_data(ticker=None, isin=None) -> pd.DataFrame:
    if isin and not ticker:
        ticker = cur.execute("SELECT ticker FROM securities WHERE isin = ?", (isin,)).fetchone()[0]
    
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
        if len(fundamentals) > 12:
            fundamentals[f"revenue growth{scope}"]  = (fundamentals[f"revenue{scope}"] / fundamentals[f"revenue{scope}"].shift(12)) ** (1/3) - 1
            fundamentals[f"operating income growth{scope}"] = (fundamentals[f"operating income{scope}"] / fundamentals[f"operating income{scope}"].shift(12)) ** (1/3) - 1
            fundamentals[f"net income growth{scope}"] = (fundamentals[f"net income{scope}"] / fundamentals[f"net income{scope}"].shift(12)) ** (1/3) - 1
            fundamentals[f"eps growth{scope}"] = (fundamentals[f"diluted eps{scope}"] / fundamentals[f"diluted eps{scope}"].shift(12)) ** (1/3) - 1
        fundamentals[f"gross margin{scope}"] = fundamentals[f"gross profit{scope}"] / fundamentals[f"revenue{scope}"]
        fundamentals[f"operating margin{scope}"] = fundamentals[f"operating income{scope}"] / fundamentals[f"revenue{scope}"]
        fundamentals[f"net margin{scope}"] = fundamentals[f"net income{scope}"] / fundamentals[f"revenue{scope}"]
        fundamentals[f"roa{scope}"] = fundamentals[f"net income{scope}"] / fundamentals[f"total assets{scope}"]
        fundamentals[f"roe{scope}"] = fundamentals[f"net income{scope}"] / fundamentals[f"total shareholders equity{scope}"]
        fundamentals[f"reinvestment rate{scope}"] = 1+(fundamentals[f"total dividends paid{scope}"].replace(np.NaN, 0)+fundamentals[f"total stock issued/repurchased{scope}"].replace(np.NaN, 0))  / fundamentals[f"net income{scope}"]

    df = pd.concat([prices, fundamentals], axis=1)
    df.index = pd.to_datetime(df.index, unit="s")
    df = df.sort_index()

    df["split"] = df["split"].fillna(0)
    df["dividends"] = df["dividends"].fillna(0)

    for col in df.columns:
        if col in ("close", "adj_close", "split", "simple_return", "dividends"):
            continue
        df[col] = df[col].ffill()
    
    df = df.copy()
    df["market_cap"] = df["close"] * df["diluted shares outstanding"]
    df["e/p"] = df["income from continuous operations ttm"] / df["market_cap"]
    df["cf/p"] = df["cashflow from operating activities ttm"] / df["market_cap"]
    df["b/m"] = df["total shareholders equity ttm"] / df["market_cap"]
    df["s/p"] = df["revenue ttm"] / df["market_cap"]
    df["payout_yield"] = -(df["total dividends paid ttm"].fillna(0) + df["common stock issued/repurchased ttm"].fillna(0)) / df["market_cap"]
    
    df = df[df["close"].notna()]
    
    return df

def get_stock_data(ticker) -> list:
    data = get_company_profile(ticker)
    news = get_news(ticker)
    time_series = get_time_series_data(ticker)
    index = time_series.index
    data.insert(4, f"${time_series.loc[index[-1], 'adj_close']:.2f}")
    market_cap = time_series.loc[index[-1], "market_cap"]
    if market_cap >= 1_000_000_000_000:
        market_cap /= 1_000_000_000_000
        digit = "T"
    elif market_cap >= 1_000_000_000:
        market_cap /= 1_000_000_000
        digit = "B"
    else:
        market_cap /= 1_000_000
        digit = "M"
    data.insert(5, f"${market_cap:.2f}{digit}")
    data.insert(6, f"{1/time_series.loc[index[-1], 'e/p']:.2f}")
    data.insert(7, f"{time_series.loc[index[-1], 'payout_yield']:.2%}")
    data.insert(19, news)
    
    if data[13] is None:
        data[13] = ""
    else:
        data[13] = f"{data[13]:,d} Employees".replace(",", ".")
    
    data.insert(20, time_series)

    return data