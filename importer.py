import json
import os

from database import CONFIG_PATH, DEFAULT_DB, connect, get_product

def load_json(path):
    with open(path, encoding="utf-8-sig") as json_file:
        data = json.load(json_file)
    return data


def cmd_import(db=DEFAULT_DB):
    con = connect(db)
    schema_path = os.path.join(CONFIG_PATH, "schema.sql")
    with open(schema_path, encoding="utf-8") as schema_file:
        schema = schema_file.read()
    con.executescript(schema)

    path = os.path.join(CONFIG_PATH, "data", "vulnerabilities.json")
    for record in load_json(path):
        for field in ('vendor', 'product', 'KLA_id', 
                      'description', 'publish_date', 
                      'start_vuln_version', 'fixed_version'):
            
            value = record.get(field)

            if value is not None:
                value = str(value).strip()

            if value == "":
                value = None
            record[field] = value

        vendor = record.get("vendor")
        product = record.get("product")
        article_id = record.get("KLA_id")

        if not (vendor and product and article_id):
            continue

        pid = get_product(con, vendor, product)
        description = record.get("description")
        published = record.get("publish_date")

        sql = (
            "INSERT OR IGNORE INTO advisory "
            "(product_id, article_id, description, published) VALUES (?, ?, ?, ?)"
        )

        params = (pid, article_id, description, published)
        con.execute(sql, params)
        sql = "SELECT id FROM advisory WHERE product_id=? AND article_id=?"
        r = con.execute(sql, (pid, article_id)).fetchone()
        first_vulnerable = record.get("start_vuln_version")

        if not first_vulnerable:
            first_vulnerable = "0"
        first_fixed = record.get("fixed_version")
        sql = (
            "INSERT OR IGNORE INTO advisory_range "
            "(advisory_id, first_vulnerable, first_fixed) VALUES (?, ?, ?)"
        )
        params = (r["id"], first_vulnerable, first_fixed)
        con.execute(sql, params)


    path = os.path.join(CONFIG_PATH, "data", "versions.json")
    for record in load_json(path):
        for field in ('vendor', 'product', 'version'):
            value = record.get(field)
            if value is not None:
                value = str(value).strip()
            if value == "":
                value = None
            record[field] = value
        vendor = record.get("vendor")
        product = record.get("product")
        version = record.get("version")

        if not (vendor and product and version):
            continue
        pid = get_product(con, vendor, product)
        sql = "INSERT OR IGNORE INTO product_version(product_id,version) VALUES (?,?)"
        con.execute(sql, (pid, version))

    con.commit()
    con.close()


if __name__ == "__main__":
    cmd_import()
