import platform
from random import randint
from time import time

from sqlalchemy import Engine, create_engine, select
from sqlalchemy.orm import Session

from models.data import Account, AccountBalance, Base, Protocol, ProtocolToken, Token, TokenPrice, Tvl
from utils import timeitit

if platform.python_implementation() == "CPython":
    db_connector_prefix = "postgresql+psycopg2"
else:
    db_connector_prefix = "postgresql+pg8000"

engine = create_engine(f"{db_connector_prefix}://postgres:example@localhost/postgres", echo=False)

Base.metadata.create_all(bind=engine)

TOKEN_NUMBER = 1000
ACCOUNT_NUMBER = 1000000


def check_content(engine: Engine) -> bool:
    with Session(engine) as session:
        if session.scalar(select(Protocol)):
            return True
    return False


def init_db(engine: Engine):
    with Session(engine) as session:
        add_protocols_and_tokens(session)
    with Session(engine) as session:
        add_accounts_and_balances(session)


@timeitit
def add_protocols_and_tokens(session: Session) -> None:
    protocol = Protocol(name="Uniswapv3")
    current_time = int(time())
    halfhour_time = current_time - 60 * 30
    hourhalf_time = current_time - 60 * 90
    twoday_time = current_time - 60 * 60 * 48
    tokens = []
    for i in range(TOKEN_NUMBER):
        protocol_token = ProtocolToken()

        token = Token(address=f"{i}", name=f"{i}", symbol=f"{i}", decimals=10)
        protocol_token.token = token
        # current time
        add_history_data(protocol_token, current_time)
        # half an hour ago
        add_history_data(protocol_token, halfhour_time)
        # hour and half ago
        add_history_data(protocol_token, hourhalf_time)
        # two days ago
        add_history_data(protocol_token, twoday_time)

        protocol.tokens.append(protocol_token)
    session.add(protocol)
    session.commit()


def add_history_data(protocol_token: ProtocolToken, time_value: int):
    token_price = TokenPrice(usd_price=10, created_at=time_value)
    protocol_token.token_prices.append(token_price)

    tvl = Tvl(amount=1, amount_usd=10, created_at=time_value, created_at_block=0)
    protocol_token.tvls.append(tvl)


@timeitit
def add_accounts_and_balances(session: Session) -> None:
    accounts = []
    for i in range(ACCOUNT_NUMBER):
        account = Account(wallet_address=f"{i}")
        for j in range(20):
            account.account_balances.append(
                AccountBalance(protocol_token_id=randint(1, TOKEN_NUMBER), amount=10, created_at_block=0)
            )
        accounts.append(account)
        if len(accounts) >= 1000:
            session.add_all(accounts)
            session.commit()
            accounts.clear()
    session.add_all(accounts)
    session.commit()
