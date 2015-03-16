# coding:utf-8


class RouteTree(object):
    _WILDCARD = object()

    def __init__(self):
        self._item = None
        self._subtrees = {}

    def find(self, path, strict):
        item, pathinfo = self._find(path, strict)

        if item is None:
            if strict:
                return None, pathinfo

            else:
                return self._item, pathinfo

        else:
            return item, pathinfo

    def _find(self, path, strict):
        if len(path) == 0:
            return self._item, {}

        else:
            head, tail = path[0], path[1:]

            if head in self._subtrees:
                return self._subtrees[head].find(tail, strict)

            elif self._WILDCARD in self._subtrees:
                label, rtree = self._subtrees[self._WILDCARD]
                item, pathinfo = rtree.find(tail, strict)
                pathinfo[label] = head
                return item, pathinfo

            else:
                return None, {}

    def update(self, path, item, replace):
        if len(path) == 0:
            if self._item is None or replace:
                self._item = item

            return self._item

        else:
            head, tail = path[0], path[1:]

            if head.startswith(':'):
                default = (head[1:], self.__class__())
                _, rtree = self._subtrees.setdefault(self._WILDCARD, default)
                return rtree.update(tail, item, replace)

            else:
                rtree = self._subtrees.setdefault(head, self.__class__())
                return rtree.update(tail, item, replace)

    def items(self):
        if self._item is not None:
            yield [], self._item

        for k1, item1 in self._subtrees.items():
            if k1 is self._WILDCARD:
                label, subtree = item1
                for k2, item2 in subtree.items():
                    yield [':{}'.format(label)] + k2, item2

            else:
                for k2, item2 in item1.items():
                    yield [k1] + k2, item2


class RequestTree(RouteTree):
    def __call__(self, method, pathexpr):
        def _(f):
            self.update(self.create_path(pathexpr), {}, False)[method] = f
            return f
        return _

    def match(self, pathexpr):
        return self.find(self.create_path(pathexpr), True)

    def merge(self, tree):
        for path, item in tree.items():
            self.update(path, {}, False).update(item)

    def create_path(self, pathexpr):
        return pathexpr.lstrip('/').split('/')

    def get(self, pathexpr):
        return self('get', pathexpr)

    def post(self, pathexpr):
        return self('post', pathexpr)

    def put(self, pathexpr):
        return self('put', pathexpr)

    def delete(self, pathexpr):
        return self('delete', pathexpr)

    def options(self, pathexpr):
        return self('options', pathexpr)

    def head(self, pathexpr):
        return self('head', pathexpr)

    def patch(self, pathexpr):
        return self('patch', pathexpr)


class ExceptionTree(RouteTree):
    def __call__(self, exc_cls):
        def _(f):
            self.update(self.create_path(exc_cls), f, True)
            return f
        return _

    def match(self, exc_cls):
        return self.find(self.create_path(exc_cls), False)[0]

    def merge(self, tree):
        for path, item in tree.items():
            self.update(path, item, True)

    def create_path(self, exc_cls):
        return '/' + '/'.join(self._create_path(exc_cls))

    def _create_path(self, exc_cls):
        if exc_cls is Exception:
            return []

        else:
            super_cls = exc_cls.__bases__[0]
            return self._create_path(super_cls) + [exc_cls.__name__]
