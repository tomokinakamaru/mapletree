# coding:utf-8


class RouteTree(object):
    _WILDCARD = object()

    def __init__(self):
        self._item = None
        self._subtrees = {}

    def __iter__(self):
        if self._item is not None:
            yield [], self._item

        for k1, item1 in self._subtrees.items():
            if k1 is self._WILDCARD:
                label, subtree = item1
                for k2, item2 in subtree:
                    yield [':{}'.format(label)] + k2, item2

            else:
                for k2, item2 in item1:
                    yield [k1] + k2, item2

    def get(self, path, strict):
        """ Gets the item for `path`. If `strict` is true, this method
        returns `None` when matching path is not found.
        Otherwise, this returns the result item of prefix searching.

        :param path: Path to get
        :param strict: Searching mode
        :type path: list
        :type strict: bool
        """
        item, pathinfo = self._get(path, strict)

        if item is None:
            if strict:
                return None, pathinfo

            else:
                return self._item, pathinfo

        else:
            return item, pathinfo

    def set(self, path, item, replace):
        """ Sets item for `path` and returns the item.
        Replaces existing item with `item` when `replace` is true

        :param path: Path for item
        :param item: New item
        :param replace: Updating mode
        :type path: list
        :type item: object
        :type replace: bool
        """
        if len(path) == 0:
            if self._item is None or replace:
                self._item = item

            return self._item

        else:
            head, tail = path[0], path[1:]

            if head.startswith(':'):
                default = (head[1:], self.__class__())
                _, rtree = self._subtrees.setdefault(self._WILDCARD, default)
                return rtree.set(tail, item, replace)

            else:
                rtree = self._subtrees.setdefault(head, self.__class__())
                return rtree.set(tail, item, replace)

    def _get(self, path, strict):
        if len(path) == 0:
            return self._item, {}

        else:
            head, tail = path[0], path[1:]

            if head in self._subtrees:
                return self._subtrees[head].get(tail, strict)

            elif self._WILDCARD in self._subtrees:
                label, rtree = self._subtrees[self._WILDCARD]
                item, pathinfo = rtree.get(tail, strict)
                pathinfo[label] = head
                return item, pathinfo

            else:
                return None, {}
