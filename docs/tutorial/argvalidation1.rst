Validating arguments
====================

The goal
--------

In the previous page, you've just seen how to retrieve arguments in clients' requests.

However using raw values in requests is often dangerous. Almost always, we have to validate given values before using them. The goal of this page is learning the way mapletree provides for arg validation.


Do it normally
--------------

Assume that you want to return a text response like ``content of page N`` according to the value of ``page`` parameter in clients' requests. In this case, the value of ``page`` should be a positive integer.

From what you've learned, you can write endpoint codes like below.

.. sourcecode:: python

    @mt.req.get('/content/normalway')
    def _(req):
        page = req.params['page']

        if page.isdigit() and 0 < int(page):
            return rsp().body('content of page {}'.format(page))

        else:
            return rsp().body('bad page no!')

Not so complex, but we want them shorter if we can.


Do it with MapleTree
--------------------

MapleTree give you a easy way to validate arguments.

.. sourcecode:: python

    @mt.req.get('/content/mapletree')
    def _(req):
        page = req.params.int_positive('page')
        return rsp().body('content of page {}'.format(page))


This is much shorter! ``req.params`` is a dictionary which is extended. You can do validating and retrieving at the same time (in one line). In the codes just above, variant ``page`` is always a positive integer.

But what if ``page`` value given in clients' request is not a positive integer? First example (normal way) returns a response with error message but second one (mapletree way)  does not.

Before seeing how to handle situations like this, we have to know how to handle exception in mapletree.
