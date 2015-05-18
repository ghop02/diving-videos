from fabric.api import task, local, lcd
import db
import os
ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


@task
def update_env():
    """ Update current environment with latest python packages """

    with lcd(ROOT_PATH):
        # delete pyc files
        local("find . -name '*.pyc' -delete")
        local('pip install -r requirements.txt')
        local('pip install -r test_requirements.txt')

    # update cassandra keyspace
    db.create_keyspace()
    db.run_migrations()
