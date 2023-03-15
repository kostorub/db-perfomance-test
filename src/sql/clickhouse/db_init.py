create_tables_sql = [
"""
-- `default`.account definition

CREATE TABLE default.account
(
    `id` Int32,
    `wallet_address` String
)
ENGINE = MergeTree
ORDER BY id
SETTINGS index_granularity = 8192;
""",
"""
-- `default`.account_balance definition

CREATE TABLE default.account_balance
(
    `id` Int32,
    `protocol_token_id` Int32,
    `amount` Int32,
    `account_id` Int32,
    `created_at_block` Int32
)
ENGINE = MergeTree
ORDER BY id
SETTINGS index_granularity = 8192;
""",
"""
-- `default`.protocol definition

CREATE TABLE default.protocol
(
    `id` Int32,
    `name` String
)
ENGINE = MergeTree
ORDER BY id
SETTINGS index_granularity = 8192;
""",
"""
-- `default`.protocol_token definition

CREATE TABLE default.protocol_token
(
    `id` Int32,
    `token_id` Int32,
    `protocol_id` Int32
)
ENGINE = MergeTree
ORDER BY id
SETTINGS index_granularity = 8192;
""",
"""
-- `default`.token definition

CREATE TABLE default.token
(
    `id` Int32,
    `address` Int32,
    `name` Int32,
    `symbol` Int32,
    `decimals` Int32
)
ENGINE = MergeTree
ORDER BY id
SETTINGS index_granularity = 8192;
""",
"""
-- `default`.token_price definition

CREATE TABLE default.token_price
(
    `id` Int32,
    `protocol_token_id` Int32,
    `usd_price` Int32,
    `created_at` Int32
)
ENGINE = MergeTree
ORDER BY id
SETTINGS index_granularity = 8192;
""",
"""
-- `default`.tvl definition

CREATE TABLE default.tvl
(
    `id` Int32,
    `protocol_token_id` Int32,
    `amount` Int32,
    `amount_usd` Int32,
    `created_at` Int32,
    `created_at_block` Int32
)
ENGINE = MergeTree
ORDER BY id
SETTINGS index_granularity = 8192;
"""
]