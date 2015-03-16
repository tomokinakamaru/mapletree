Handling exceptions
===================

The goal
--------

The goal of this page is learning the way to handle exceptions.

Prepare
-------

Add new codes below just like we've been doing in tutorials.

.. sourcecode:: python

    @mt.req.get('/handle_exception')
    def _(req):
        return rsp().json(message='tutorial for exception handling!')

Test
----

Try accessing ``http://localhost:5000/handle_exception`` with GET method. As you guess, you will get a json response. But what happens if you access with POST method to ``http://localhost:5000/handle_exception``? 

Maybe you've got response with an error message like ``A server error occurred.  Please contact the administrator.`` and terminal message ``NoExceptionHandler: <class 'mapletree.exceptions.MethodNotAllowed'>``. This is not acceptable behavior, we want the app to return a response with status code 405 (Method Not Allowed).

You would get almost same messages if you try accessing ``http://localhost:5000/abcdefghijk`` with GET, which is not defined in your app. In this case, you get ``NoExceptionHandler: <class 'mapletree.exceptions.NotFound'>`` in terminal, but what we want is a response with status code 404 (Not Found)!

Handle exceptions
-----------------

The codes below are the solution. Add these to your app codes!

.. sourcecode:: python

    # at the top of `application.py`
    from mapletree.exceptions import MethodNotAllowed, NotFound


    # just before `if __name__ == '__main__'`
    @mt.exc(NotFound)
    def _(e):
        return rsp().code(404).json(message='Not Found')


    @mt.exc(MethodNotAllowed)
    def _(e):
        return rsp().code(405).body('Method Not Allowed')


Then try again, this time you would get things you expected.


Handle more
-----------

To see more of what happens on exceptions, let's try another example.

.. sourcecode:: python

    @mt.req.get('/zerodivision')
    def _(req):
        return rsp().body('1/0 is {}'.format(1/0))

This obviously raises exception ``ZeroDivisionError`` and you would get an error response. You need an exception handler shown below.


.. sourcecode:: python

    @mt.exc(ZeroDivisionError)
    def _(e):
        return rsp()code(500).body('cannot divide a number by 0')

Now you get a response with status code 500, saying ``cannot divide a number by 0``.


How it works
------------

In the example above, We wrote exception handlers for each type of exceptions. However it's not easy to list up all the exception that happens in your application.

The exception routing to handlers in MapleTree has a flexible feature for this reason. See table below to understand the exception routing in MapleTree. Assume that you write exception handlers for ``Exception``, ``ArithemeticError`` and ``ZeroDivisionError``, each named ``exc_handler``, ``arithmetic_exchandler`` and ``zerodivision_exchandler``.


===================== ================================= =======================
raised exception type the ancestors of raised exception invoking handler
===================== ================================= =======================
ZeroDivisionError     ArithemeticError,                 zerodivision_exchandler
                      StandardError,
                      Exception
OverflowError         ArithemeticError,                 arithmetic_exc_handler
                      StandardError,
                      Exception
TypeError             StandardError,                    exc_handler
                      Exception
===================== ================================= =======================

When an exception raise, MapleTree tries finding handler for the type of the exception. If no handler is found for it, tries finding the handler for the super class of the raised exception. If not found again, tries with the super of the super of the raised exception.
