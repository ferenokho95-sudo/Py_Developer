import os
import sqlite3
import sys

CONFIG_PATH = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DB = os.path.join(CONFIG_PATH, "base.db")


def connect(path):
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    return con


def get_product(con, vendor, product):
    con.execute("INSERT OR IGNORE INTO vendor(name) VALUES (?)", (vendor,))
    sql = "SELECT id FROM vendor WHERE name=?"
    r = con.execute(sql, (vendor,)).fetchone()
    vid = r["id"]
    con.execute("INSERT OR IGNORE INTO product(vendor_id,name) VALUES (?,?)", (vid, product))
    sql = "SELECT id FROM product WHERE vendor_id=? AND name=?"
    r = con.execute(sql, (vid, product)).fetchone()
    return r["id"]


def need_db(path):
    if not os.path.exists(path):
        sys.exit("Нет базы. Запустите python importer.py")
    return connect(path)


def find_products(con, name):
    sql = (
        "SELECT p.id, p.name, v.name AS vendor "
        "FROM product p JOIN vendor v ON v.id=p.vendor_id "
        "WHERE p.name=? ORDER BY p.name"
    )
    rows = con.execute(sql, (name,)).fetchall()
    if rows:
        return rows

    print("Продукт не найден:", name)
    sys.exit(1)


def load_advisories(con, pid):
    advisories = []
    sql = "SELECT * FROM advisory WHERE product_id=? ORDER BY published, article_id"
    rows = con.execute(sql, (pid,)).fetchall()
    for advisory in rows:
        sql = (
            "SELECT first_vulnerable, first_fixed "
            "FROM advisory_range WHERE advisory_id=?"
        )
        ranges = con.execute(sql, (advisory["id"],)).fetchall()
        advisories.append((advisory, ranges))
    return advisories
