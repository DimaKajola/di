import inspect


class DependenciesInjector:

    def __call__(self, class_name, **kwargs):

        if type(class_name) == str:
            class_name = self.import_class(class_name)

        signature = self.get_signatures(class_name)

        if signature is None:
            return class_name()

        return class_name(**{key: self.get_value(parameter, kwargs.get(key, parameter.empty), class_name)
                             for key, parameter in signature.parameters.items()})

    @staticmethod
    def get_signatures(class_name):
        try:
            return inspect.signature(class_name)
        except ValueError:
            # no signature found for builtin type
            return None

    @staticmethod
    def get_value(parameter, passed_value, class_name):
        if parameter.annotation is parameter.empty:
            raise TypeError(f'Please hint the type of parameter "{parameter.name}" '
                            f'in {".".join([class_name.__module__, class_name.__name__])}.__init__')

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
            return di(parameter.annotation)

    @staticmethod
    def import_class(class_name):
        components = class_name.split('.')
        class_name = __import__(components[0])
        for comp in components[1:]:
            class_name = getattr(class_name, comp)
        return class_name


di = DependenciesInjector()
