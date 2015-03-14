# coding:utf-8

from .shared import mt

mt.config.load_package('test_config_pkg')
mt.scan('test_app_pkg.routes')
app = mt
