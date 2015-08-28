# coding:utf-8

from mapletree import MapleTree, rsp

mt = MapleTree()


@mt.req.get('/')
def _(req):
    return rsp().json(message='GET OK')


@mt.req.post('/')
def _(req):
    print req.data
    return rsp().json(message='POST OK')


@mt.exc.route(Exception)
def _(e):
    print e
    return rsp().code(400)


if __name__ == '__main__':
    mt.run()
