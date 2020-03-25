"""Configuration"""

import os


class ConfigGetter(dict):
    """Default Getter/Setter"""

    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError as ke:
            raise AttributeError('Config has no {key}'.format(key=ke.args[0]))

    def __setattr__(self, attr, value):
        self[attr] = value


class AppConfig(ConfigGetter):
    """Web Config"""

    def __init__(self):
        super().__init__({})


class DatabaseConfig(ConfigGetter):
    """Database config"""

    def __init__(self):
        super().__init__({})

        self.host = os.environ['POSTGRES_HOST']
        self.port = int(os.environ['POSTGRES_PORT'])
        self.db_name = os.environ['POSTGRES_DB']
        self.user = os.environ['POSTGRES_USER']
        self.password = os.environ['POSTGRES_PASSWORD']
        self.schema = os.environ['POSTGRES_SCHEMA']


class ApplicationConfig(ConfigGetter):
    """Main configuration class"""

    def __init__(self):
        super().__init__({})
        self.app = AppConfig()
        self.database = DatabaseConfig()
