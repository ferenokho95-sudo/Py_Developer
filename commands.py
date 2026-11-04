from database import find_products, load_advisories, need_db
from versions import advisory_hit, vkey

def cmd_safe(args):
    con = need_db(args.db)
    for product in find_products(con, args.product):
        sql = "SELECT version FROM product_version WHERE product_id=?"
        rows = con.execute(sql, (product["id"],)).fetchall()
        advisories = load_advisories(con, product["id"])
        safe = None
        for r in rows:
            version = r[0]
            found = False
            for advisory, ranges in advisories:
                if advisory_hit(version, ranges) is not None:
                    found = True
                    break
            if not found:
                if safe is None or vkey(version) >= vkey(safe):
                    safe = version
        print(product["vendor"], product["name"])
        if not rows:
            print("Нет версий в базе")
        elif safe is None:
            print("В базе нет версий без известных уязвимостей")
        else:
            print("Последняя версия без известных уязвимостей:", safe)
    con.close()


def cmd_check(args):
    con = need_db(args.db)
    for product in find_products(con, args.product):
        print(product["vendor"], product["name"], args.version)
        found = False
        for advisory, ranges in load_advisories(con, product["id"]):
            fixed = advisory_hit(args.version, ranges)
            if fixed is None:
                continue
            found = True
            print(advisory["article_id"], advisory["published"])
            print(advisory["description"])
            if fixed:
                print("Исправлено в версии:", fixed)
            else:
                print("Исправления пока нет")
        if not found:
            print("Известных уязвимостей не найдено")
    con.close()
