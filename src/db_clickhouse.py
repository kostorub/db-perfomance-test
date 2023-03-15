from random import randint
from time import time

from sqlalchemy import Engine, create_engine, select
from sqlalchemy.orm import Session

from models.data import (Account, AccountBalance, Base, Protocol,
                         ProtocolToken, Token, TokenPrice, Tvl)
from utils import timeitit
from sql.clickhouse.db_init import create_tables_sql

import clickhouse_connect
from clickhouse_connect.driver.client import Client


client = clickhouse_connect.get_client()

TOKEN_NUMBER = 1000
ACCOUNT_NUMBER = 1000000


def check_content(client: Client) -> bool:
    result = client.query("""SELECT * FROM (
        SELECT * 
        FROM INFORMATION_SCHEMA.TABLES

        ) z_q WHERE table_name = 'account'""")
    if result.row_count:
        return True
    return False


def init_db(client: Client):
    for el in create_tables_sql:
        client.command(el)
    add_protocols_and_tokens(client)
    add_accounts_and_balances(client)


@timeitit
def add_protocols_and_tokens(client: Client) -> None:
    client.insert("protocol", [[1, "Uniswapv3"]])

    current_time = int(time())
    halfhour_time = current_time - 60 * 30
    hourhalf_time = current_time - 60 * 90
    twoday_time = current_time - 60 * 60 * 48

    token_price_id = 0

    for i in range(TOKEN_NUMBER):
        protocol_token = [i, i, 1]
        client.insert("protocol_token", [protocol_token])

        token = [i, f"{i}", f"{i}", f"{i}", 10]
        client.insert("token", [token])

        # current time
        add_history_data(client, token_price_id, i, current_time)
        token_price_id += 1
        # half an hour ago
        add_history_data(client, token_price_id, i, halfhour_time)
        token_price_id += 1
        # hour and half ago
        add_history_data(client, token_price_id, i, hourhalf_time)
        token_price_id += 1
        # two days ago
        add_history_data(client, token_price_id, i, twoday_time)
        token_price_id += 1


def add_history_data(client: Client, token_price_id: int, protocol_token_id: int, time_value: int):
    token_price = [token_price_id, 10, protocol_token_id, time_value]
    client.insert("token_price", [token_price])
    tvl = [token_price_id, protocol_token_id, 10, 100, time_value, 0]
    client.insert("tvl", [tvl])


@timeitit
def add_accounts_and_balances(client: Client) -> None:
    balances_count = 20
    for i in range(ACCOUNT_NUMBER):
        account = [i, f"{i}"]
        client.insert("account", [account])
        for j in range(balances_count):
            account_balance = [i*balances_count + j, randint(1, TOKEN_NUMBER), 10, i, 0]
            client.insert("account_balance", [account_balance])
