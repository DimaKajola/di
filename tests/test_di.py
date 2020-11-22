from unittest import TestCase
from di.dependency_injector import DependenciesInjector


class SomeClass:
    pass


class TestDependenciesInjectorGetClass(TestCase):

    def test_import_from_the_same_file(self):
        # Trying to import some class located in the current file
        self.assertIs(DependenciesInjector._get_class('tests.test_di.SomeClass'), SomeClass)

    def test_from_other_file(self):
        # Trying to import some classes located in another file and that weren't imported before

        # Bar's reference added to tests.snippets.__init__.py
        class_obj = DependenciesInjector._get_class('tests.snippets.bar.Bar')

        from tests.snippets.bar import Bar
        self.assertIs(class_obj, Bar)

        # Foo's reference wasn't added to tests.snippets.__init__.py
        class_obj = DependenciesInjector._get_class('tests.snippets.foo.Foo')

        from tests.snippets.foo import Foo
        self.assertIs(class_obj, Foo)

    def test_relative_import(self):
        # trying to import some class in the global context
        self.assertRaises(ModuleNotFoundError, DependenciesInjector._get_class, 'SomeClass')

        # relative import won't work without specifying of correct module name
        self.assertRaises(TypeError, DependenciesInjector._get_class, '.SomeClass')
        self.assertRaises(AttributeError, DependenciesInjector._get_class, '.SomeClass', module_ref=__package__)

        self.assertIs(DependenciesInjector._get_class('.SomeClass', module_ref=__name__), SomeClass)
        self.assertIs(DependenciesInjector._get_class('SomeClass', module_ref=__name__), SomeClass)

    def test_bad_import(self):
        # Some others edge cases
        self.assertRaises(TypeError, DependenciesInjector._get_class, '.')
        self.assertRaises(ModuleNotFoundError, DependenciesInjector._get_class, ',,,,sdfg,dsfg,h54hh')
        self.assertRaises(ModuleNotFoundError, DependenciesInjector._get_class, 'not_existed_module.not_existed')
        self.assertRaises(ModuleNotFoundError, DependenciesInjector._get_class, '______')
        self.assertRaises(ModuleNotFoundError, DependenciesInjector._get_class, '12345')
        self.assertRaises(AttributeError, DependenciesInjector._get_class, 12345678)
        self.assertRaises(AttributeError, DependenciesInjector._get_class, None)
        self.assertRaises(AttributeError, DependenciesInjector._get_class, SomeClass)


class TestDependenciesInjectorGetValue(TestCase):

    def test_get_defaults(self):
        pass

