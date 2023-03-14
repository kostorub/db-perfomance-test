from api import Period, get_portfolio_timeline, get_protocol_estimation, get_protocol_tokens, get_top_accounts
from db import check_content, init_db, engine


if __name__ == "__main__":
    if not check_content(engine):
        init_db(engine)

    result_1 = get_protocol_tokens(engine, 1)
    result_2 = get_protocol_estimation(engine, 1)
    result_3 = get_portfolio_timeline(engine, 1, Period.HOUR)
    result_4 = get_portfolio_timeline(engine, 1, Period.DAY)
    result_5 = get_portfolio_timeline(engine, 1, Period.MONTH)
    result_6 = get_top_accounts(engine, 1)
    # result_7 = get_top_accounts_view(engine, 1)

    print("get_protocol_tokens", result_1)
    print("get_protocol_estimation", result_2)
    print("Period.HOUR", result_3)
    print("Period.DAY", result_4)
    print("Period.MONTH", result_5)
    print("get_top_accounts", result_6)
    # print("get_top_accounts_view", result_7)

    # result_1 = get_protocol_tokens(engine, 1)
    # result_2 = get_protocol_estimation(engine, 1)
    # result_3 = get_portfolio_timeline(engine, 1, Period.HOUR)
    # result_4 = get_portfolio_timeline(engine, 1, Period.DAY)
    # result_5 = get_portfolio_timeline(engine, 1, Period.MONTH)
    # result_6 = get_top_accounts(engine, 1)