from unittest import TestCase
from di import DependenciesInjector, DIRegistry
from tests.snippets.foo import Foo
import inspect


class TestDependenciesInjectorGetInitArgs(TestCase):

    def setUp(self) -> None:
        self.di = DependenciesInjector(DIRegistry())

    def test_get_init_args(self):
        signature = inspect.signature(Foo)

        res = self.di._get_init_args(Foo, signature, {})

        self.assertIsInstance(res, dict)
        self.assertEqual(signature.parameters.keys(), res.keys())
