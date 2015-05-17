from fabric.api import task, local, lcd
import os
ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


@task
def update_env():
    """ Update current environment with latest python packages """

    # delete pyc files
    with lcd(ROOT_PATH):
        local("find . -name '*.pyc' -delete")
        local('pip install -r requirements.txt')
