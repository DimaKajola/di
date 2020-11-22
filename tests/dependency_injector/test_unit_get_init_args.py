from unittest import TestCase
from di import di
from tests.snippets.foo import Foo
import inspect


class TestDependenciesInjectorGetInitArgs(TestCase):

    def test_get_init_args(self):
        signature = inspect.signature(Foo)

        res = di._get_init_args(Foo, signature, {})

        self.assertIsInstance(res, dict)
        self.assertEqual(signature.parameters.keys(), res.keys())
