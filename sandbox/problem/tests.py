from django.test import TestCase
from .models import Problem, Submission


class TestModel(TestCase):
    def create_problem(self, run_script):
        return Problem.objects.create(
            title='title',
            description='description',
            run_script=run_script
        )

    def create_submission(self, **kwargs):
        return Submission.objects.create(**kwargs)

    def test_evaluate_pass(self):
        problem = self.create_problem(run_script='test()')
        submission = self.create_submission(
            problem=problem,
            code='def test(): pass')

        self.assertFalse(submission.evaluated)

        submission.evaluate()

        self.assertTrue(submission.evaluated)
        self.assertTrue(submission.has_passed)

    def test_evaluate_fail(self):
        problem = self.create_problem(run_script='test()')
        submission = self.create_submission(
            problem=problem,
            code='def test(): raise Exception()')

        self.assertFalse(submission.evaluated)

        submission.evaluate()

        self.assertFalse(submission.has_passed)
        self.assertTrue(submission.evaluated)
