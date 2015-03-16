Parameters in path
==================

The goal
--------

By accessing to ``req.params`` or ``req.data``, you can get values in requests. For the next, let's try getting values in path.


Endpoint definition
-------------------

All you need to do is just write ``:`` in the path. Here is the sample codes.

.. sourcecode:: python

    @mt.get('/users/:id')
    def _(req):
        """ Endpoint for /users/1, /users/abc, /users/ etc.
            Not for /users """
        user_id = req.pathparams.pint('id')
        return rsp().json(message='user id is {}'.format(user_id))


    @mt.req.get('/user/:uid/articles/:aid')
    def _(req):
        uid = req.pathparams.pint('uid')
        aid = req.pathparams.pint('aid')

        fmt = 'the content of airticle {} (owned by user {})'
        return rsp().body(fmt.format(uid, aid))


No diffrence from ``req.params`` etc., you can also use any validation function for ``pathparams``.
