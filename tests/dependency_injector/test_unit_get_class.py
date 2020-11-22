from unittest import TestCase, mock
from di import DependenciesInjector


class SomeClass:
    pass


class TestDependenciesInjectorGetClass(TestCase):

    def setUp(self) -> None:
        self.di = DependenciesInjector(mock.Mock())

    def test_import_from_the_same_file(self):
        # Trying to import some class located in the current file
        ref = 'tests.dependency_injector.test_unit_get_class.SomeClass'
        self.assertIs(self.di._get_class(ref), SomeClass)

    def test_from_other_file(self):
        # Trying to import some classes located in another files and that weren't imported before

        # A reference to Bar added to tests.snippets.__init__.py
        class_obj = self.di._get_class('tests.snippets.bar.Bar')

        from tests.snippets.bar import Bar
        self.assertIs(class_obj, Bar)

        # A reference to Foo wasn't added to tests.snippets.__init__.py
        class_obj = self.di._get_class('tests.snippets.foo.Foo')

        from tests.snippets.foo import Foo
        self.assertIs(class_obj, Foo)

    def test_relative_import(self):
        # trying to import some class in the global context
        self.assertRaises(ModuleNotFoundError, self.di._get_class, 'SomeClass')

        # relative import won't work without specifying of correct module name
        self.assertRaises(TypeError, self.di._get_class, '.SomeClass')
        self.assertRaises(AttributeError, self.di._get_class, '.SomeClass', module_ref=__package__)

        self.assertIs(self.di._get_class('.SomeClass', module_ref=__name__), SomeClass)
        self.assertIs(self.di._get_class('SomeClass', module_ref=__name__), SomeClass)

    def test_bad_import(self):
        # Some others edge cases
        self.assertRaises(TypeError, self.di._get_class, '.')
        self.assertRaises(AttributeError, self.di._get_class, 12345678)
        self.assertRaises(AttributeError, self.di._get_class, None)
        self.assertRaises(AttributeError, self.di._get_class, SomeClass)
        self.assertRaises(ModuleNotFoundError, self.di._get_class, ',,,,sdfg,dsfg,h54hh')
        self.assertRaises(ModuleNotFoundError, self.di._get_class, 'not_existed_module.not_existed_class')
        self.assertRaises(ModuleNotFoundError, self.di._get_class, '______')
        self.assertRaises(ModuleNotFoundError, self.di._get_class, '12345')
