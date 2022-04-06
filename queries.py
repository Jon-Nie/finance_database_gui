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