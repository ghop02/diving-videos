from config.application import (
    GlobalApplicationConfig
)


class ApplicationConfig(GlobalApplicationConfig):
    ENV = 'development'

    CASSANDRA_CLUSTER = ['127.0.0.1']
    CASSANDRA_KEYSPACE = 'ripple'
    CASSANDRA_REPLICATION = {
        'class': 'SimpleStrategy',
        'replication_factor': 1
    }
