from collections import defaultdict
from enum import Enum
from time import time
from typing import List

from sqlalchemy import Engine, func, select
from sqlalchemy.orm import Session

from db import check_content, engine, init_db
from models.data import ProtocolToken, Token, Tvl
from utils import timeitit


class Period(Enum):
    HOUR = 1
    DAY = 2
    MONTH = 3


@timeitit
def get_protocol_tokens(engine: Engine) -> List[Token]:
    with Session(engine) as session:
        query = select(Token).join(ProtocolToken).where(ProtocolToken.protocol_id == 1)
        return list(session.scalars(query))


@timeitit
def get_protocol_estimation(engine: Engine) -> float:
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
            .where(ProtocolToken.protocol_id == 1)
        )
        query = select(func.sum(sub_query.c.amount_usd)).where(sub_query.c.row_number == 1)
        result = sum(list(session.scalars(query)))
        return result


@timeitit
def get_portfolio_timeline(engine: Engine, period: Period):
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
            .where(ProtocolToken.protocol_id == 1)
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


if __name__ == "__main__":
    if not check_content(engine):
        init_db(engine)

    print("get_protocol_tokens", get_protocol_tokens(engine))
    print("get_protocol_estimation", get_protocol_estimation(engine))
    print("Period.HOUR", get_portfolio_timeline(engine, Period.HOUR))
    print("Period.DAY", get_portfolio_timeline(engine, Period.DAY))
    print("Period.MONTH", get_portfolio_timeline(engine, Period.MONTH))
