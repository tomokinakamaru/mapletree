# coding:utf-8

from mapletree.config import Config


class ConfigTest(object):
    def __init__(self):
        self.config = Config()


def test_config():
    config = Config()

    @config
    def value():
        return {'development': 100,
                'production': 200}

    config.stage = 'development'
    assert config.value == 100

    config.stage = 'production'
    assert config.value == 200
