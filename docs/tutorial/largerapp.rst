Larger application
==================

The goal
--------

If you have been writing codes in ``application.py``, which created in the first tutorial, the number of lines became too large to understand things at sight. Even if not, we need to write a certain amount of codes when creating actual application.

You would have already know that writing everything in one file is not good idea, so let's split them into some files. The goal of this page is learning how to structure files in MapleTree.


Prepare
-------

Create directories and python files as shown below.

::

    largerapp
        |-- application.py
        |-- shared.py
        |-- routes
            |-- __init__.py
            |-- users.py
            |-- excs.py


Fundamental part
--------------------

First of all, we need an instance of MapleTree. Let's write the short codes below in ``shared.py`` (not in ``application.py``).

.. sourcecode:: python

    from mapletree import MapleTree

    mt = MapleTree()

Next, write some lines in ``application.py`` which starts MapleTree application.

.. sourcecode:: python

    from shared import mt

    if __name__ == '__main__':
        mt.run()

We got the fundamental part of  the application. You can run the app now, but nothing interesting happens yet.


Request routing
---------------

Write some codes in ``routes/users.py``. The codes below are just example, saving nothing about users, only saying like ``created!``. This page is for learning how to structure larger app, so write whatever you want other than ``from shared import mt``. this line is important.


.. sourcecode:: python

    from shared import mt
    from mapletree import rsp


    @mt.req.get('/users/:id')
    def _(req):
        uid = req.pathparams.pint('uid')
        return rsp().json(message='info of user {}'.format(uid))


    @mt.req.get('/users')
    def _(req):
        email = req.data.email_addr('email')
        name = req.data.take('name', None, 'Anonymous')

        fmt = 'created new user {}({})'
        return rsp().json(message=fmt.format(name, email))


    @mt.req.delete('/users/:id')
    def _(req):
        uid = req.pathparams.pint('uid')
        return rsp().json(message='deleted user {}'.format(uid))


Exception routing
-----------------

Write some codes in ``routes/excs.py`` to handle exceptions. Nothing new, but the line ``from shared import mt`` is also important in this file.

.. sourcecode:: python

    import traceback
    from shared import mt

    @mt.exc(Exception)
    def _(e):
        traceback.print_exc()

        msg = "I'm lazy so i just write basic exception handler"
        return rsp().code(500).json(message=msg)


Scan files
----------

We created ``routes/users.py`` and ``routes/excs.py`` with some contents, but the app still do not return meaningful responses. This is because they are not loaded at all, we have to load them to the application.

Actually the loading means ``import``-ing, so should we edit ``application.py`` like...

.. sourcecode:: python

    from shared import mt
    from routes import users, excs

    if __name__ == '__main__':
        mt.run()

This is not so bad if we only have two routing files. But it is kind of repeating to type names of the files you created in directory ``routes``.

MapleTree liberates you from this repeating with ``scan``. With this, you can write like below.

.. sourcecode:: python

    from shared import mt
    
    mt.scan('routes')

    if __name__ == '__main__':
        mt.run()

``scan`` imports all modules in the target package recursively, so you can move, rename, remove files without editing ``application.py``.

Now you would get meaningful responses from your app.


Why 'shared.py'
---------------

Why we cannot write the codes for creating instance of MapleTree in ``application.py``? The reason is that, if ``mt`` is created in ``application.py``, each route file (``routes/users.py``, ``routes/excs.py``) needs to import ``application.py``. However ``application.py`` also needs route files so there is an import loop.

``shared.py`` seems a wasteful file. But in actual application building, you will write codes for ``mt.config`` and ``mt.thread``  (See :ref:`utility_tutorial_index`) in ``shared.py`` and it's going to contain more meaningful lines.
