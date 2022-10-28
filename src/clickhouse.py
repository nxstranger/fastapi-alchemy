from .settings import settings

if settings.COLLECT_CLICKHOUSE_DATA:
    from clickhouse_driver import Client
    client = Client(host=settings.CLICKHOUSE_DB)

    REQUESTS_STATS_TABLE = 'request_stats'

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

    ADV_TABLE = settings.CLICKHOUSE_ADV_TABLE

