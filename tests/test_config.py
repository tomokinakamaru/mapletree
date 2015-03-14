# coding:utf-8

from mapletree.config import Config


class ConfigTest(object):
    def __init__(self):
        self.config = Config()


def test_config():
    ct = ConfigTest()

    ct.config.load_package('test_config_pkg')
    ct.config.stage = 'development'
    assert ct.config.value == 100

    ct.config.stage = 'production'
    assert ct.config.value == 200
