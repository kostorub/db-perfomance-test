# Install

Clone the repository

    git clone git@github.com:kostorub/db-perfomance-test.git
    cd db-perfomance-test

Start a docker container for the Postgresql service

    docker-compose -f docker-compose/postgresql.yaml up

Use either CPython interpreter or PyPy for the best perfomance

    python3 -m venv .venv_cpython
    . ./.venv_cpython/bin/activate
    pip install pip-tools
    pip-compile
    pip-sync

For basic benchmarks use

    python3 ./src/api.py

On my machine I have

    Timeitit <get_protocol_estimation>: 0.01793503761291504 sec
    Timeitit <get_portfolio_timeline>: 0.06346869468688965 sec # Period.HOUR
    Timeitit <get_portfolio_timeline>: 0.07407307624816895 sec # Period.DAY
    Timeitit <get_portfolio_timeline>: 0.04651594161987305 sec # Period.MONTH
    Timeitit <get_top_accounts>: 254.63567757606506 sec

[Explain of get_top_accounts](https://explain.tensor.ru/archive/explain/36aff347c9c4f5c98c32ebe2051a8c85:0:2023-03-10#explain "Explain of get_top_accounts")

# Architecture 

## Current view

![Alt text](https://github.com/kostorub/db-perfomance-test/blob/main/img/Screenshot%202023-03-10%20203127.png "Current structure")

## Alternative view

![Alt text](https://github.com/kostorub/db-perfomance-test/blob/main/img/Screenshot%202023-03-10%20204201.png "Alternative structure")

Suggestions  
- To store the latest actual data in separate tables to improve the performance of top 100 accounts calculation
- To store an amount_usd in the AccountBalance current table and update it periodically
- Not to store all of the 1kk+ accounts in one table, probably separate them onto different DB
