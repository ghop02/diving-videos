

class Ripple(object):
    Config = None

    @staticmethod
    def init_config(env):
        if env == 'development':
            import development as env_config

        Ripple.Config = env_config.ApplicationConfig


def init_config(env=None):
    Ripple.init_config(env)
