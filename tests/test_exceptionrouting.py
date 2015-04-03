# coding:utf-8

import pytest
from mapletree.defaults.routings.exceptionrouting import (
        ExceptionRouting,
        NoExceptionHandler)


def test_basics():
    er = ExceptionRouting()

    @er.route(TypeError)
    def ehandler(e):
        pass

    assert er(TypeError()) == ehandler


def test_merge():
    er1, er2 = ExceptionRouting(), ExceptionRouting()

    @er1.route(TypeError)
    def ehandler1(e):
        pass

    @er2.route(ValueError)
    def ehandler2(e):
        pass

    er1.merge(er2)
    assert er1(TypeError()) == ehandler1
    assert er1(ValueError()) == ehandler2


def test_no_exc_handler():
    er = ExceptionRouting()
    pytest.raises(NoExceptionHandler, er, Exception())
