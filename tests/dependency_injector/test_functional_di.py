from unittest import TestCase
from di import di, DependenciesInjector
from tests.snippets.foo import Foo
from tests.snippets.bar import Bar
from tests.snippets.baz import Baz


class Parent(object):

    def __init__(self, foo: Foo):
        self.foo = foo


class Child(Parent):
    pass


class ChildBar(Bar):
    pass


class ChildBaz(Baz):
    pass


class ChildBar2(Bar):
    pass


class ChildBaz2(Baz):
    pass


class TestDI(TestCase):

    def test_bootstrap(self):
        self.assertIsInstance(di, DependenciesInjector)

    def test_di(self):
        foo = di('tests.snippets.foo.Foo', test_int=5)
        self.assertIsInstance(foo, Foo)
        self.assertIsInstance(foo.bar, Bar)
        self.assertIsInstance(foo.baz, Baz)
        self.assertEqual(foo.test_int, 5)
        self.assertEqual(foo.test_str, 'default string')

        child = di(Child)
        self.assertIsInstance(child.foo, Foo)
        self.assertIsInstance(child.foo.bar, Bar)
        self.assertIsInstance(child.foo.baz, Baz)

        try:
            foo.bar.test()
            foo.baz.test()
            _ = foo.bar.test_var
            _ = foo.baz.test_var

            child.foo.bar.test()
            child.foo.baz.test()
            _ = child.foo.bar.test_var
            _ = child.foo.baz.test_var

            di('tests.dependency_injector.test_functional_di.Parent')
            di('tests.dependency_injector.test_functional_di.Child')
            di('Parent', module_ref=__name__)
            di('Child', module_ref=__name__)
        except Exception as e:
            self.fail(f"DI failed: {e}")

    def test_di_binding(self):
        res1 = di(Foo)

        self.assertNotIsInstance(res1.bar, ChildBar)
        self.assertNotIsInstance(res1.baz, ChildBaz)

        di.to(Foo).bind(bar=di(ChildBar), baz=di(ChildBaz))

        res2 = di(Foo)

        self.assertIsInstance(res2.bar, ChildBar)
        self.assertIsInstance(res2.baz, ChildBaz)

        di.to(Foo).bind(bar=ChildBar2, baz=ChildBaz2)

        res2 = di(Foo)

        self.assertIsInstance(res2.bar, ChildBar2)
        self.assertIsInstance(res2.baz, ChildBaz2)
