from utils import db
import pandas as pd
import numpy as np

con = db.connection
cur = db.cursor

def get_stock_list() -> list:
    data = cur.execute(
        "SELECT ticker, yahoo_name FROM securities WHERE id IN (SELECT security_id FROM companies)"
    ).fetchall()
    data_filtered = []
    for index, item in enumerate(data):
        if item[1] is None:
            continue
        data_filtered.append((item[0], item[1], "Stock"))
    return data_filtered


def get_company_profile(ticker) -> dict:
    security_id = cur.execute("SELECT id FROM securities WHERE ticker = ?", (ticker,)).fetchone()[0]
    data = cur.execute(
        """
        SELECT
        securities.ticker,
        securities.yahoo_name AS name,
        securities.isin,
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

    return list(data)