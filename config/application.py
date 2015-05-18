import logging


class GlobalApplicationConfig(object):
    pass


class GlobalLogConfig(object):

    FORMAT = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    ROOT_LEVEL = logging.DEBUG
    LOG_TO_CONSOLE = True
    CONSOLE_LEVEL = logging.DEBUG
    LOG_TO_FILE = False
    FILE_BASE = '/var/log/ripple/'
    FILE_LEVEL = logging.DEBUG
