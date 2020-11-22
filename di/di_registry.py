class DIRegistryItem(dict):
    """

    """
    def bind(self, **kwargs) -> None:
        """

        :param kwargs:
        :return:
        """
        self.update(kwargs)


class DIRegistry:
    """

    """
    def __init__(self) -> None:
        self._pool = {}

    def add(self, class_obj: type) -> DIRegistryItem:
        """

        :param class_obj:
        :return:
        """
        try:
            registry_item = self._pool[class_obj]
        except KeyError:
            registry_item = DIRegistryItem()
            self._pool[class_obj] = registry_item

        return registry_item

    def get(self, class_obj: type):
        return self._pool.get(class_obj, {})
