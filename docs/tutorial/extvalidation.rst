Validation & default values
===========================

The goal
--------

We have been working on validation feature in MapleTree using ``req.params.pint``. But positive integer is not the only validation rule we use. Plus, we have seen ``InsufficientError`` raise when the value is not provided in requests, but don't know how to set default values (the value that are used when the target value is not provided).

In this page, we see more usage of features for retrieving values in requests.

Use your validation functions
-----------------------------

You can use your function for validation.

.. sourcecode:: python

    @mt.req.get('/custom_validation')
    def _(req):

        def username_vldt(v): # `v` is always string, never becomes None
            if len(v) < 16:
                return v

            raise Exception('too long')

        username = req.params.take('username', username_vldt)
        return rsp().json(username=username)

In your validation function, you don't need to raise ``ValidationError``. MapleTree will convert any exception raised in validation function to ``ValidationError`` automatically.


If you want to use ``username_vldt`` rule in many endpoints, you can use it as if it were an initially defined method by doing like below.

.. sourcecode:: python

    from mapletree import Request


    @Request.validator
    def username(v):
        if len(v) < 16:
            return v

        raise Exception('too long')


    @mt.req.get('/username')
    def _(req):
        username = req.params.username('username')
        return rsp().json(username=username)


Default values
--------------

Some of arguments in requests are not required. For example, the default value for page is 1. The codes below shows how to set default values in MapleTree.

.. sourcecode:: python

    @mt.req.ge('/defaultvalue')
    def _(req):
        page = req.params.pint('page', 1)
        return rsp().json(page=page)

The default value is used only when ``page`` value is not provided in clients' requests. If the value of ``paga`` is given but not a positive integer, the line raises ``ValidationError``.

