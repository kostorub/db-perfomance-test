from collections import defaultdict
from enum import Enum
from time import time
from typing import Dict, List, Tuple

from sqlalchemy import Engine, and_, desc, func, select, text
from sqlalchemy.orm import Session

from models.data import AccountBalance, ProtocolToken, Token, TokenPrice, Tvl
from utils import timeitit


class Period(Enum):
    HOUR = 1
    DAY = 2
    MONTH = 3


@timeitit
def get_protocol_tokens(engine: Engine, protocol_id: int) -> List[Token]:
    with Session(engine) as session:
        query = select(Token).join(ProtocolToken).where(ProtocolToken.protocol_id == protocol_id)
        return list(session.scalars(query))


@timeitit
def get_protocol_estimation(engine: Engine, protocol_id: int) -> int:
    with Session(engine) as session:
        sub_query = (
            select(
                Tvl.amount_usd,
                Tvl.created_at,
                func.row_number()
                .over(partition_by=ProtocolToken.token_id, order_by=Tvl.created_at.desc())
                .label("row_number"),
            )
            .join(ProtocolToken)
            .where(ProtocolToken.protocol_id == protocol_id)
        )
        query = select(func.sum(sub_query.c.amount_usd)).where(sub_query.c.row_number == 1)
        result = sum(list(session.scalars(query)))
        return result


@timeitit
def get_portfolio_timeline(engine: Engine, protocol_id: int, period: Period) -> Dict[int, int]:
    """
    Return a dict where key is a timestamp and a value is an amount_usd sum
    {1678147200: Decimal('10000'), 1678233600: 0, 1678320000: Decimal('10000')}
    """
    time_to = int(time()) // 60 * 60
    # time_to = 1678384923
    if period == Period.HOUR:
        time_from = time_to - 60 * 60
        divider = 60
    elif period == Period.DAY:
        time_from = time_to - 60 * 60 * 24
        divider = 60 * 15
    elif period == Period.MONTH:
        time_from = time_to - 60 * 60 * 24 * 30
        divider = 60 * 60 * 24

    with Session(engine) as session:
        query = (
            select(ProtocolToken.token_id, Tvl.amount_usd, Tvl.created_at)
            .join(ProtocolToken)
            .where(ProtocolToken.protocol_id == protocol_id)
            .where(Tvl.created_at >= time_from)
        )
        db_result = session.execute(query)

    t_result = defaultdict(dict)

    for token_id, amount_usd, created_at in db_result:
        key = created_at // divider
        if token_id not in t_result[key]:
            t_result[key][token_id] = []
        t_result[key][token_id].append((amount_usd, created_at))

    result = dict()
    for key in range(time_from // divider, time_to // divider + 1):
        result[key * divider] = 0

    for key, tokens in t_result.items():
        for values in tokens.values():
            result[key * divider] += max(values, key=lambda x: x[1])[0]

    return result


@timeitit
def get_top_accounts(engine: Engine, protocol_id: int) -> List[Tuple[int, int]]:
    """Return [(1, Decimal('2900')), (3, Decimal('2000')), (64, Decimal('2000'))]"""
    with Session(engine) as session:
        subquery_1 = (
            select(TokenPrice.protocol_token_id, func.max(TokenPrice.created_at).label("max_created_at"))
            .group_by(TokenPrice.protocol_token_id)
            .subquery()
        )

        subquery_2 = (
            select(ProtocolToken.id, TokenPrice.protocol_token_id, TokenPrice.usd_price)
            .join(
                subquery_1,
                and_(
                    TokenPrice.protocol_token_id == subquery_1.c.protocol_token_id,
                    TokenPrice.created_at == subquery_1.c.max_created_at,
                ),
            )
            .join(ProtocolToken)
            .where(ProtocolToken.protocol_id == protocol_id)
            .subquery()
        )

        subquery_3 = (
            select(
                AccountBalance.account_id,
                AccountBalance.protocol_token_id,
                func.max(AccountBalance.created_at_block).label("max_created_at_block"),
            )
            .group_by(AccountBalance.account_id, AccountBalance.protocol_token_id)
            .subquery()
        )

        subquery_4 = (
            select(AccountBalance.account_id, AccountBalance.protocol_token_id, AccountBalance.amount)
            .join(
                subquery_3,
                and_(
                    AccountBalance.account_id == subquery_3.c.account_id,
                    AccountBalance.protocol_token_id == subquery_3.c.protocol_token_id,
                    AccountBalance.created_at_block == subquery_3.c.max_created_at_block,
                ),
            )
            .subquery()
        )

        query = (
            select(subquery_4.c.account_id, func.sum(subquery_4.c.amount * subquery_2.c.usd_price).label("amount_top"))
            .join(subquery_2, subquery_4.c.protocol_token_id == subquery_2.c.protocol_token_id)
            .group_by(subquery_4.c.account_id)
            .order_by(desc("amount_top"))
            .limit(100)
        )

        db_result = session.execute(query)

    return list(db_result)


@timeitit
def get_top_accounts_view(engine: Engine, protocol_id: int) -> Dict[str, int]:
    """Experimental"""
    with Session(engine) as session:
        query = text("SELECT * FROM top_100 LIMIT 100;")
        db_result = session.execute(query)

    return list(db_result)
