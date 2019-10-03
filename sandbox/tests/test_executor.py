from unittest import TestCase
from ..executor import run


class TestPythonRun(TestCase):
    def run_python(self, text: str):
        return run('python', '3.7', text)

    def test_hello_world(self):
        out, err = self.run_python('print("hello world")')
        self.assertEqual(err, '')
        self.assertEqual(out, b'hello world\n')
