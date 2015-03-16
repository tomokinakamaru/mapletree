Reuse your endpoints
====================

The goal
--------

This is the last page for tutorial. In this page, we work on reusing endpoints. Reusability make your work a lot easier. Nobody wants to write the same code again.

Reuse exception routing
-----------------------

To reuse endpoints, you can use ``RequestTree`` for request routing and ``ExceptionTree`` for exception routing. The example below is using ``ExceptionTree``.

.. sourcecode:: python

    from mapletree.routetree import ExceptionTree
    from mapletree.exceptions import (ValidationError,
                                      InsufficientError,
                                      NotFound,
                                      MethodNotAllowed)

    et = ExceptionTree()


    @et(Exception)
    def _(e):
        return rsp().code(500).json(message='unknown error occurred')


    @et(NotFound)
    def _(e):
        return rsp().code(404).json(message='not found')


    @et(MethodNotAllowed)
    def _(e):
        return rsp().code(405).json(message='method not allowed')

    @et(ValidationError)
    def _(e):
        return rsp().code(400).json(message='invalid parameter')


    @et(InsufficientError)
    def _(e):
        return rsp().code(400).json(message='insufficient parameters')


Almost same as we've seen, the only difference is using ``ExceptionTree`` instead of ``MapleTree.exc``. (Actually an instance of MapleTree has ``ExceptionTree`` internally.)


Merge
-----

This is how to use your reusable route tree.

.. sourcecode:: python

    from shared import mt
    from myreusable import et as myexctree

    mt.exc.merge(myexctree)

This is all you need, merging ``myexctree`` with the exception tree in an instance of MapleTree. In the same way, you can reuse your request routing codes!
