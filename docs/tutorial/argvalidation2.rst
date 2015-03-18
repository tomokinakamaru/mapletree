Validating arguments again
==========================

The goal
--------

We worked on argument validations 2 pages before but left a problem about invalid arguments.

The goal of this page is to solve the problem and make a complete endpoint implementation for the paging application.

ValidationError
---------------

The codes we wrote were ...

.. sourcecode:: python

    @mt.req.get('/content/normalway')
    def _(req):
        page = req.params['page']

        if page.isdigit() and 0 < int(page):
            return rsp().body('content of page {}'.format(page))

        else:
            return rsp().body('bad page no!')


    @mt.req.get('/content/mapletree')
    def _(req):
        page = req.params.int_positive('page')
        return rsp().body('content of page {}'.format(page))


``req.params.int_positive('page')`` raises ``ValidationError`` or ``InsufficientError`` if the value given as ``page`` is not a positive integer or does not provided. Let's add new lines to handle exceptions for this like below.

.. sourcecode:: python

    # at the top of application.py
    from mapletree.exceptions import ValidationError, InsufficientError


    # wherever you want
    @mt.exc(ValidationError)
    def _(e):
        key, val, err = e
        msg = '`{}` is invalid for {} ({})'.format(val, key, err)
        return rsp().code(400).json(message=msg)


    @mt.exc(InsufficientError)
    def _(e):
        return rsp().code(400).json(message='lacking parameter `{}`'.format(e))

This seems much longer than normal way in the end.

However the lines you just added catches all ``ValidationError`` or ``InsufficientError`` that raise in your entire application, so not longer overall. Moreover, the behavior to exceptions will become more consistent.
