from cassandra.cqlengine import connection
from lib import Log


class Ripple(object):
    Config = None

    @staticmethod
    def init_config(env):
        if env == 'development':
            import development as env_config

        Ripple.Config = env_config.ApplicationConfig
        Ripple.LogConfig = env_config.LogConfig


def init_config(env=None):
    Ripple.init_config(env)
    Log.init(Ripple.LogConfig)


def init_cassandra(env):
    connection.setup(
        Ripple.Config.CASSANDRA_CLUSTER,
        Ripple.Config.CASSANDRA_KEYSPACE
    )
