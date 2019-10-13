from django.test import TestCase
from rest_framework import status
from utils.rest_framework import ViewsetTestMixin
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

    def test_fields(self):
        problem = self.create_problem(run_script='test()')
        readonly_data = dict(
            evaluate=False,
            has_passed=0,
            stderr='err'
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


class TestProblemViewset(ViewsetTestMixin, ProblemMixin, TestCase):
    view_name = 'problem:problem'

    def create_problem(self):
        return super().create_problem('')

    def test_list(self):
        problem = self.create_problem()
        content = self.api_list().json
        self.assertEqual(len(content), 1, content)
        self.assertEqual(content[0]['id'], problem.pk)

    def test_retrieve(self):
        problem = self.create_problem()
        content = self.api_retrieve(pk=problem.pk).json
        self.assertEqual(content['id'], problem.pk)

    def test_invalid_methods(self):
        HTTP_405_METHOD_NOT_ALLOWED = status.HTTP_405_METHOD_NOT_ALLOWED

        response = self.api_update(pk=1, data={})
        self.assertEqual(response.status_code, HTTP_405_METHOD_NOT_ALLOWED)

        response = self.api_delete(pk=1)
        self.assertEqual(response.status_code, HTTP_405_METHOD_NOT_ALLOWED)

        response = self.api_create(data={})
        self.assertEqual(response.status_code, HTTP_405_METHOD_NOT_ALLOWED)


class TestSubmissionViewset(ViewsetTestMixin, ProblemMixin, TestCase):
    view_name = 'problem:submission'

    def test_create(self):
        problem = self.create_problem('test()')
        data = dict(
            problem=problem.pk,
            code='def test(): pass',
        )
        content = self.api_create(data=data).json

        self.assertDictContainsSubset(dict(
            problem=problem.pk,
            has_passed=True,
            stderr='',
            evaluated=True,
        ), content)

    def test_list(self):
        content = self.api_list().json
        self.assertEqual(content, [])

    def test_retrieve(self):
        problem = self.create_problem('test()')
        submission = self.create_submission(
            problem=problem,
            code='def test(): pass')
        content = self.api_retrieve(pk=submission.pk).json
        self.assertEqual(content['id'], submission.pk)

    def test_invalid_methods(self):
        HTTP_405_METHOD_NOT_ALLOWED = status.HTTP_405_METHOD_NOT_ALLOWED

        response = self.api_update(pk=1, data={})
        self.assertEqual(response.status_code, HTTP_405_METHOD_NOT_ALLOWED)

        response = self.api_delete(pk=1)
        self.assertEqual(response.status_code, HTTP_405_METHOD_NOT_ALLOWED)
