# coding:utf-8

from dictree import Dictree, WILDCARD


class RequestHandler(object):
    def __init__(self):
        self._tree = Dictree()

    @property
    def tree(self):
        return self._tree

    @staticmethod
    def parse_path(path):
        ls = path.lstrip('/').split('/')
        key = [WILDCARD if e.startswith(':') else e for e in ls]
        labels = [e[1:] if e.startswith(':') else None for e in ls]
        return key, labels

    @staticmethod
    def build_path(key, labels):
        ls = [k if l is None else ':' + l for k, l in zip(key, labels)]
        return '/' + '/'.join(ls)

    def __call__(self, environ):
        path = environ['PATH_INFO'] or '/'
        key, _ = self.parse_path(path)

        try:
            (labels, funcs), trace = self.tree.find(key, True)

        except KeyError:
            raise NotFound(path)

        else:
            method = environ['REQUEST_METHOD']
            if method not in funcs:
                raise MethodNotAllowed(method, path)

            extra = dict(zip([l for l in labels if l is not None],
                             [k for k, b in zip(key, trace) if b]))
            return funcs[method], extra

    def add(self, method, path):
        def _(f):
            key, labels = self.parse_path(path)
            self.tree.setdefault(key, [(), {}])
            self.tree[key][0] = labels
            self.tree[key][1][method.upper()] = f

            return f
        return _

    def get(self, path):
        return self.add('get', path)

    def post(self, path):
        return self.add('post', path)

    def put(self, path):
        return self.add('put', path)

    def delete(self, path):
        return self.add('delete', path)

    def head(self, path):
        return self.add('head', path)

    def options(self, path):
        return self.add('options', path)

    def patch(self, path):
        return self.add('patch', path)

    def merge(self, handler, prefix=''):
        for key, (labels, funcs) in handler.tree.items():
            fullkey = prefix + self.build_path(key, labels)
            for method, f in funcs.items():
                self.add(method, fullkey)(f)


class NotFound(Exception):
    pass


class MethodNotAllowed(Exception):
    pass
