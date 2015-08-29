# coding:utf-8

import pytest
from mapletree.exceptionhandler import (ExceptionHandler,
                                        NoExceptionHandler)


def test_basics():
    er = ExceptionHandler()

    @er.add(TypeError)
    def ehandler(e):
        pass

    assert er(TypeError()) == ehandler


def test_merge():
    er1, er2 = ExceptionHandler(), ExceptionHandler()

    @er1.add(TypeError)
    def ehandler1(e):
        pass

    @er2.add(ValueError)
    def ehandler2(e):
        pass

    er1.merge(er2)
    assert er1(TypeError()) == ehandler1
    assert er1(ValueError()) == ehandler2


def test_no_exc_handler():
    er = ExceptionHandler()
    pytest.raises(NoExceptionHandler, er, Exception())
