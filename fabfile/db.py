from fabric.api import task
import os
import sys
_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(_root)


@task
def run_migrations():
    from cdeploy.migrator import Migrator, load_config
    from cassandra.cluster import Cluster

    env = os.environ.get('RIPPLEENV')
    if not env:
        print "please set RIPPLEENV environment var"
        sys.exit(1)

    migrations_path = os.path.join(_root, 'migrations/')
    config = load_config(migrations_path, env)
    cluster = Cluster(config['hosts'])
    try:
        session = cluster.connect()
        session.default_timeout = None  # None disables timeout
        session.set_keyspace(config['keyspace'])
        Migrator(migrations_path, session).run_migrations()
    finally:
        cluster.shutdown()


@task
def create_keyspace():
    env = os.environ.get('RIPPLEENV')
    if not env:
        print "please set RIPPLEENV environment var"
        sys.exit(1)

    from config import Ripple
    from config.app_config import init_config
    init_config(env)

    from cassandra.cluster import Cluster
    cluster = Cluster(Ripple.Config.CASSANDRA_CLUSTER)
    session = cluster.connect()
    query = """
    CREATE KEYSPACE IF NOT EXISTS %(keyspace)s
    WITH replication = %(replication)s
    """
    args = {
        'keyspace': Ripple.Config.CASSANDRA_KEYSPACE,
        'replication': Ripple.Config.CASSANDRA_REPLICATION
    }
    print query % args
    session.execute(query % args)
