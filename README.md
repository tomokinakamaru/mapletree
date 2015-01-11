MapleTree
==========

## MapleTree

MapleTree is a WSGI application framework.

## "Hello World!" in MapleTree

```python

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
	return rsp().html('<h1>Hello World!</h1>')


application = mt.wsgiapp()  # creating wsgi application

if __name__ == '__main__':
	import wsgidriver  # just a driving server for wsgi (https://github.com/tomokinakamaru/wsgidriver)
	wsgidriver.run(application)  # start serving

```


## Basic usages

### Request routing

+ Static routing

```python
@mt.get('/')  # for method GET, routing path must start with '/'
def _(req):
	return rsp()  # '200 OK' with empty response body


@mt.post('/')  # for method POST
def _(req):
	return rsp()


@mt.put('/test/path')  # for PUT @http://example.com/test/path
def _(req):
	return rsp()

```

+ Dynamic routing

```python

@mt.get('/*(label)')
def _(req):
	""" This function will be called when request path is '/' or '/xxx', etc.
	This will never be called for '/xxx/yyy' nor '/xxx/'. """

	return rsp().body(req.pathparams['label'])


@mt.get('/foo')
def _(req):
	""" Static routing like '/foo' has priority over dynamic routing.
	This function will be called when request path is '/foo'
	even if you defined '/*(name)' before. """

	return rsp().body('This is static route!')


@mt.get('/*(model_name)/*(model_id)')
def _(req):
	""" Routing path can contain more than one wildcard
	and you can label them as you want. """

	fmt = 'getting data of {} (ID={})'
	mname, mid = req.pathparams['model_name'], req.pathparams['model_id']

	return rsp().body(fmt.format(mname, mid))

```


### Exception routing

```python

""" Request routing """
@mt.get('/test1')
def _(req):
	a = 1/0  # ZeroDivisionError
	return rsp().body(a)


@mt.get('/test2')
def _(req):
	raise OverflowError()  # subclass of ArithmeticError


@mt.get('/test3')
def _(req):
	i = int('abcd')  # ValueError (subclass of StandardError(Exception))
	return rsp().body(i)


@mt.get('/test4')
def _(req):
	i = int(None)  # TypeError (subclass of StandardError(Exception))
	return rsp().body(i)


""" Exception routing """
@mt.exception(Exception)
def _(e):
	return rsp().code(500).body('Unknown error')


@mt.exception(ArithmeticError)  # subclass of StandardError(Exception)
def _(e):
	return rsp().code(500).body('Arithmetic error occurred')


@mt.exception(ZeroDivisionError)  # subclass of ArithmeticError
def _(e):
	return rsp().code(500).body('Cannot deveide number by 0')


@mt.exception(ValueError)
def _(e):
	return rsp().code(400).body('Bad value')


""" Internally, this code above constructs routing-tree below.

Exception  (<- '/test4')
	|- StandardError
		|- ValueError  (<- '/test3')
		|- ArithmeticError  (<- '/test2')
			|- ZeroDivisionError  (<- '/test1')

And each exception class in '/test1' - '/test4' is expressed as a path below.

/test1 (ZeroDivisionError):
	/Exception/StandardError/ArithmeticError/ZeroDivisionError

/test2 (OverflowError):
	/Exception/StandardError/ArithmeticError/OverflowError

/test3 (ValueError):
	/Exception/StandardError/ValueError

/test4 (TypeError):
	/Exception/StandardError/TypeError

Unlike in the case of request routing, finding a matching endpoint in
exception routing is not strict, which means a node return its own function
if the node cannot find any matching function in its subnodes.

"""

```
