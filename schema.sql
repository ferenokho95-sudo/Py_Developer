PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS vendor (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE COLLATE NOCASE
);

CREATE TABLE IF NOT EXISTS product (
    id INTEGER PRIMARY KEY,
    vendor_id INTEGER NOT NULL REFERENCES vendor(id),
    name TEXT NOT NULL COLLATE NOCASE,
    UNIQUE (vendor_id, name)
);

CREATE TABLE IF NOT EXISTS product_version (
    id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES product(id),
    version TEXT NOT NULL,
    UNIQUE (product_id, version)
);

CREATE TABLE IF NOT EXISTS advisory (
    id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES product(id),
    article_id TEXT NOT NULL,
    description TEXT,
    published TEXT,
    UNIQUE (product_id, article_id)
);

CREATE TABLE IF NOT EXISTS advisory_range (
    id INTEGER PRIMARY KEY,
    advisory_id INTEGER NOT NULL REFERENCES advisory(id) ON DELETE CASCADE,
    first_vulnerable TEXT NOT NULL,
    first_fixed TEXT,
    UNIQUE (advisory_id, first_vulnerable, first_fixed)
);

CREATE INDEX IF NOT EXISTS idx_product_name ON product(name);
CREATE INDEX IF NOT EXISTS idx_advisory_prod ON advisory(product_id);
CREATE INDEX IF NOT EXISTS idx_range_adv ON advisory_range(advisory_id);
