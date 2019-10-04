from django.test import TestCase
from .models import Problem, Submission
from .serializers import SubmissionSerializer


class ProblemMixin:
    def create_problem(self, run_script):
        return Problem.objects.create(
            title='title',
            description='description',
            run_script=run_script
        )

    def create_submission(self, **kwargs):
        return Submission.objects.create(**kwargs)


class TestModel(ProblemMixin, TestCase):
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


class TestSubmissionSerializer(ProblemMixin, TestCase):
    def test_create(self):
        problem = self.create_problem(run_script='test()')
        serializer = SubmissionSerializer(data=dict(
            problem=problem.id,
            code='def test(): pass'
        ))
        serializer.is_valid()
        submission = serializer.save()
        self.assertTrue(submission.evaluated)

    def test_read_only_field(self):
        problem = self.create_problem(run_script='test()')
        readonly_data = dict(
            evaluate=False,
            has_passed=0,
            error='err'
        )
        data = dict(
            problem=problem.pk,
            code='def test(): pass',
        )
        serializer = SubmissionSerializer(data=dict(**data, **readonly_data))
        serializer.is_valid()
        submission = serializer.save()

        # writable fields
        self.assertEqual(data, dict(
            problem=submission.problem.pk,
            code=submission.code,
        ))

        # readonly fields
        for key in readonly_data.keys():
            self.assertNotEqual(
                getattr(submission, key),
                readonly_data[key]
            )
