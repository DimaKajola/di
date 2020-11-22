from unittest import TestCase
from di.dependency_injector import DependenciesInjector
from tests.snippets.foo import Foo
import inspect


class TestDependenciesInjectorGetInitArgs(TestCase):

    def test_get_init_args(self):
        di = DependenciesInjector()
        signature = inspect.signature(Foo)

        res = di._get_init_args(Foo, signature, {})

        self.assertIsInstance(res, dict)
        self.assertEqual(signature.parameters.keys(), res.keys())
