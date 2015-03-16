.. image:: https://travis-ci.org/tomokinakamaru/mapletree.svg?branch=master
    :target: https://travis-ci.org/tomokinakamaru/mapletree
    :alt: MapleTree Build

=========
MapleTree
=========

About
=====

MapleTree is a WSGI application framework. Python2.7, 3.3, and 3.4 are supported.

"Hello World!" in MapleTree
===========================

.. sourcecode:: python

    from mapletree import MapleTree, rsp  # rsp stands for response

    mt = MapleTree()


    @mt.get('/')
    def _(req):
        """ Plain text response """
        return rsp().body('Hello World!')


    @mt.get('/json')
    def _(req):
        """ JSON response ({"message": "Hello World!"})"""
        return rsp().json(message='Hello World!')


    @mt.get('/html')
    def _(req):
        """ HTML response """
        return rsp().html('<html><body><h1>Hello World!</h1></body></html>')



    if __name__ == '__main__':
        mt.run()


Documentation
=============

Tutorial and documentations are available at `here <https://tomokinakamaru.github.io/mapletree>`
