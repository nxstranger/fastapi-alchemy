from .settings import settings

REQUESTS_STATS_TABLE = 'request_stats'

if settings.COLLECT_CLICKHOUSE_DATA:
    from clickhouse_driver import Client
    client = Client(host=settings.CLICKHOUSE_DB)

    client.execute(
            'CREATE TABLE IF NOT EXISTS {0} ({1} String, {2} String, {3} String, {4} String, {5} DateTime) ENGINE = Memory'.format(
                REQUESTS_STATS_TABLE,
                'agent',
                'client',
                'path',
                'method',
                'stamp',

            )
        )

