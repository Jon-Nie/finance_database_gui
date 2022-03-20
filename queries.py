from utils import db
import pandas as pd
import numpy as np

con = db.connection
cur = db.cursor

def get_stock_list() -> list:
    data = cur.execute(
        "SELECT ticker, yahoo_name FROM securities WHERE id IN (SELECT security_id FROM companies)"
    ).fetchall()
    for index, item in enumerate(data):
        if item[1] is None:
            data[index] = (item[0], "None")
    return data

def get_security_id(ticker) -> int:
    security_id = cur.execute("SELECT id FROM securities WHERE ticker = ?", (ticker,)).fetchone()[0]
    return security_id

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