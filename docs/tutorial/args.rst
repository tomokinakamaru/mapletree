Getting args in requests
========================

The goal
--------

In the previous page, you just made simple application that returns static contents. But actually, almost all app have to handle request parameters to change contents dynamically. So we need to know how to retrieve request parameters.

The goal of this page is creating an application that echos back parameters in clients' requests.

Add some codes
--------------

Add lines below just before ``if __name__ == '__main__'`` in ``application.py``, which you've created in last section.

.. sourcecode:: python

    @mt.req.get('/params')
    def _(req):
        return rsp().json(message='what you gave me',
                          params=req.params,
                          data=req.data)


    @mt.req.post('/data')
    def _(req):
        return rsp().json(message='what you gave me',
                          params=req.params,
                          data=req.data)


These are basically not different from codes you wrote in the previous page.

As you imagine, ``req.params`` is a dictionary containing the values in query string (GET parameters) and ``req.data`` is one containig the values in request body (POST arguments).


Test the updated app
--------------------

--------------
Before testing
--------------

Start server with ``python application.py`` if not yet started. If it's already running (you maybe started during reading in the previous page.), don't worry about restarting. MapleTree automatically restarts app when it detected changes of source codes.


----------------
Sending requests
----------------

Send GET request to ``http://localhost:5000/prams`` and  POST one to ``http://localhost:5000/data`` with whatever args you want. You will see the server echos back your parameters!
