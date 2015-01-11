# coding:utf-8


class BaseRoute(object):
    WILDCARD = object()

    def __init__(self):
        self._item = None
        self._subroutes = {}

    @property
    def item(self):
        return self._item

    @property
    def subroutes(self):
        return self._subroutes

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

            if head in self._subroutes:
                return self._subroutes[head].find(tail, strict)

            elif self.WILDCARD in self._subroutes:
                label, route = self._subroutes[self.WILDCARD]
                item, pathinfo = route.find(tail, strict)
                pathinfo[label] = head
                return item, pathinfo

            else:
                return None, {}

    def update(self, path, item, replace=False):
        if len(path) == 0:
            if self._item is None or replace:
                self._item = item

            return self._item

        else:
            head, tail = path[0], path[1:]

            if isinstance(head, WildcardLabel):
                default = (head.label, BaseRoute())
                _, route = self._subroutes.setdefault(self.WILDCARD, default)
                return route.update(tail, item, replace)

            else:
                route = self._subroutes.setdefault(head, BaseRoute())
                return route.update(tail, item, replace)

    def get(self, pathexpr, strict=True):
        return self.find(self.create_path(pathexpr), strict)

    def set(self, pathexpr, item):
        return self.update(self.create_path(pathexpr), item, True)

    def setdefault(self, pathexpr, item):
        return self.update(self.create_path(pathexpr), item, False)

    def create_path(self, pathexpr):
        raise Exception()


class WildcardLabel(object):
    def __init__(self, label):
        self._label = label

    @property
    def label(self):
        return self._label
