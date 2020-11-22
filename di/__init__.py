from di.di_registry import DIRegistry, DIRegistryItem
from typing import Union, Any
import importlib
import inspect


class DependenciesInjector:
    """

    """
    def __init__(self, registry: DIRegistry) -> None:
        self._registry = registry

    def __call__(self, class_obj: Union[str, type], module_ref: str = None, **kwargs):
        """

        :param class_obj:
        :param package:
        :param kwargs:
        :return:
        """

        return self.load(class_obj, module_ref, **kwargs)

    def load(self, class_obj: Union[str, type], module_ref: str = None, **kwargs):
        """

        :param class_obj:
        :param module_ref:
        :param kwargs:
        :return:
        """
        if type(class_obj) == str:
            class_obj = self._get_class(class_obj, module_ref)

        # Please don't try to create any object based on built-in types
        # via DependenciesInjector - it might cause unpredictable behaviour.
        # That is why following row is added - it will raise TypeError for built-in types.
        inspect.getsource(class_obj)

        signature = inspect.signature(class_obj)

        if signature is None:
            return class_obj()

        user_values = {**self._registry.get(class_obj), **kwargs}
        return class_obj(**self._get_init_args(class_obj, signature, user_values))

    def to(self, class_obj: Union[str, type], module_ref: str = None) -> DIRegistryItem:
        if type(class_obj) == str:
            class_obj = self._get_class(class_obj, module_ref)
        return self._registry.add(class_obj)

    def _get_init_args(self, class_obj: type, signature: inspect.Signature, user_values: dict):
        """

        :param class_obj:
        :param signature:
        :param user_values:
        :return:
        """
        return {key: self._get_value(parameter, user_values.get(key, parameter.empty), class_obj)
                for key, parameter
                in signature.parameters.items()}

    def _get_value(self, parameter: inspect.Parameter, passed_value: Any, class_obj: type):
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
            return self.load(passed_value) \
                if inspect.isclass(passed_value) \
                else passed_value
        elif parameter.default is not parameter.empty:
            # to be able to pass default value
            return parameter.default

        # to auto generate arguments from annotations for user defined classes.
        # it will also generate objects for built-in types with default values
        # (e.g 0 for int, an empty string for str, etc.)
        return self.load(parameter.annotation)

    @staticmethod
    def _get_class(class_ref: str, module_ref: str = None) -> Any:
        """

        :param class_ref:
        :param module_ref:
        :return:
        """

        try:
            return importlib.import_module(class_ref, package=module_ref)
        except ModuleNotFoundError:
            pass

        ref = class_ref if module_ref is None else f"{module_ref}.{class_ref.strip('.')}"
        components = ref.split('.')
        class_obj = __import__(components[0])
        for comp in components[1:]:
            class_obj = getattr(class_obj, comp)
        return class_obj


di = DependenciesInjector(DIRegistry())
