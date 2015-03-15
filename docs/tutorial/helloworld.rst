"Hello World!" with MapleTree
=============================

The goal
--------

The goal of this page is creating an application that actually responds to http requests.

The specs of the app we work on are...

- return plain text ``Hello World!`` for ``http://localhost:5000``
- return json response ``{"message": "Hello World!"}`` for ``http://localhost:5000/json``
- return html response ``<html><body>Hellow World!</body></html>`` for ``http://localhost:5000/html``


Prepare dirs & files
--------------------

Create a directory named ``mt-tutorial`` at wherever you want. Then create a python file named ``application.py`` in ``mt-tutorial``.


Write application codes
-----------------------

Write the code below in ``application.py`` and save it!

.. sourcecode:: python

    from mapletree import MapleTree, rsp

    mt = MapleTree()


    @mt.req.get('/')
    def _(req):
        """ plain text response """
        return rsp().body('Hello World!')


    @mt.req.get('/json')
    def _(req):
        """ json response """
        return rsp().json(message='Hello World!')


    @mt.req.get('/html')
    def _(req):
        """ html response """
        return rsp().html('<html><body>Hello World!</body></html>')


    if __name__ == '__main__':
        mt.run()


Test the app
---------------
Now you can run your first mapletree app with command ``python application.py``!
Running this command should print lines below in your terminal.

::

    : starting driver
    : starting stub

This is showing that mapletree is serving requests.

Check it's running as you expected by accessing ``http://localhost:5000`, `http://localhost:5000/json`` and ``http://localhost:5000/html``!
