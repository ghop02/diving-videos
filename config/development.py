from config.application import (
    GlobalApplicationConfig,
    GlobalLogConfig
)
import logging


class ApplicationConfig(GlobalApplicationConfig):
    ENV = 'development'

    CASSANDRA_CLUSTER = ['127.0.0.1']
    CASSANDRA_KEYSPACE = 'ripple'
    CASSANDRA_REPLICATION = {
        'class': 'SimpleStrategy',
        'replication_factor': 1
    }


class LogConfig(GlobalLogConfig):
    LOG_TO_FILE = True
    LOG_TO_CONSOLE = True
    ROOT_LEVEL = logging.DEBUG
