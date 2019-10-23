from unittest import TestCase
from ..executor import run, ExecutionError


class TestPythonRun(TestCase):
    def run_python(self, text: str):
        return run('python', '3.7', text)

    def test_hello_world(self):
        stdout = self.run_python('print("hello world")')
        self.assertEqual(stdout, 'hello world\n')

    def test_exception(self):
        with self.assertRaisesRegex(ExecutionError, r'Exception: err\n$'):
            self.run_python('raise Exception("err")')
