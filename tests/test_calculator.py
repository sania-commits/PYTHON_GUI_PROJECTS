"""Exercise calculator callbacks without starting a desktop window."""
import ast
from pathlib import Path
import unittest


class LabelStub(dict):
    def config(self, **kwargs):
        self.update(kwargs)


class CalculatorTests(unittest.TestCase):
    def setUp(self):
        source = Path(__file__).resolve().parents[1] / 'Wallpapers/calculator.py'
        tree = ast.parse(source.read_text())
        callbacks = ast.Module(body=[n for n in tree.body if isinstance(n, ast.FunctionDef)], type_ignores=[])
        self.scope = {'result_label': LabelStub(text=''), 'history_label': LabelStub(text=''), 'first_number': None, 'second_number': None, 'operator': None}
        exec(compile(callbacks, str(source), 'exec'), self.scope)

    def calculate(self, left, op, right):
        self.scope['result_label']['text'] = left
        self.scope['get_operator'](op)
        self.scope['result_label']['text'] = right
        self.scope['get_result']()
        return self.scope['result_label']['text']

    def test_operations(self):
        for left, op, right, result in [('12', '+', '8', '20'), ('12', '-', '8', '4'), ('12', '*', '8', '96'), ('9', '/', '2', '4.5')]:
            with self.subTest(op=op):
                self.assertEqual(self.calculate(left, op, right), result)

    def test_divide_by_zero_and_recovery(self):
        self.assertEqual(self.calculate('9', '/', '0'), 'Error')
        self.scope['get_digit'](7)
        self.assertEqual(self.scope['result_label']['text'], '7')

    def test_incomplete_input(self):
        self.scope['get_operator']('+')
        self.assertEqual(self.scope['result_label']['text'], 'Error')
        self.scope['clear']()
        self.scope['get_result']()
        self.assertEqual(self.scope['result_label']['text'], 'Error')

    def test_chained_fraction_and_clear(self):
        self.assertEqual(self.calculate('9', '/', '2'), '4.5')
        self.assertEqual(self.calculate('4.5', '+', '2'), '6.5')
        self.scope['clear']()
        self.assertIsNone(self.scope['operator'])
        self.assertEqual(self.scope['history_label']['text'], '')


if __name__ == '__main__':
    unittest.main()
