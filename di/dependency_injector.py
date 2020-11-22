import inspect
from typing import Union, Any


class DependenciesInjector:
    """

    """
    def __call__(self, class_obj: Union[str, type], **kwargs):
        """

        :param class_obj:
        :param kwargs:
        :return:
        """
        return self.load(class_obj, **kwargs)

    def load(self, class_obj: Union[str, type], **kwargs):
        """

        :param class_obj:
        :param kwargs:
        :return:
        """
        if type(class_obj) == str:
            class_obj = self.get_class(class_obj)

        # Please don't try to create any object based on built-in types
        # via DependenciesInjector - it might cause unpredictable behaviour.
        # That is why following row is added - it will raise TypeError for built-in types.
        inspect.getsource(class_obj)

        signature = inspect.signature(class_obj)

        return class_obj() \
            if signature is None \
            else class_obj(**self.get_initial_arguments(class_obj, signature, kwargs))

    def get_initial_arguments(self, class_obj: type, signature: inspect.Signature, user_values: dict):
        """

        :param class_obj:
        :param signature:
        :param user_values:
        :return:
        """
        return {key: self.get_value(parameter,  user_values.get(key, parameter.empty), class_obj)
                for key, parameter
                in signature.parameters.items()}

    def get_value(self, parameter, passed_value: Any, class_obj: type):
        """

        :param parameter:
        :param passed_value:
        :param class_obj:
        :return:
        """
        if parameter.annotation is parameter.empty:
            raise TypeError(f'Please hint the type of parameter "{parameter.name}" '
                            f'in {".".join([class_obj.__module__, class_obj.__name__])}.__init__')

        if passed_value is not parameter.empty:
            # to be able to overwrite the parameter on-the-fly
            return passed_value
        elif parameter.default is not parameter.empty:
            # to be able to pass default value
            return parameter.default
        else:
            # to auto generate arguments from annotations for user defined classes.
            # it will also generate objects for built-in types with default values
            # (e.g 0 for int, an empty string for str, etc.)
            return self.load(parameter.annotation)

    @staticmethod
    def get_class(class_obj: str) -> type:
        """

        :param class_obj:
        :return:
        """
        components = class_obj.split('.')
        class_obj = __import__(components[0])
        for comp in components[1:]:
            class_obj = getattr(class_obj, comp)
        return class_obj
