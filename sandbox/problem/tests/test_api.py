import pytest
from django.test import TestCase
from rest_framework import status
from utils.rest_framework import ViewsetTestMixin
from ..serializers import SubmissionSerializer
from .utils import create_problem as base_create_problem, create_submission as base_create_submission


class ProblemMixin:
    def create_problem(self, *args, **kwargs):
        return base_create_problem(*args, **kwargs)

    def create_submission(self, *args, **kwargs):
        return base_create_submission(*args, **kwargs)


'''
    Test Model
'''


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_evaluate_pass():
    problem = base_create_problem(run_script='test()')
    submission = base_create_submission(
        problem=problem,
        code='def test(): print("stdout")')

    assert not submission.evaluated

    await submission.evaluate()

    assert submission.evaluated
    assert submission.has_passed
    assert submission.stdout == 'stdout\n'
    assert submission.stderr == ''


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_evaluate_fail():
    problem = base_create_problem(run_script='test()')
    code = (
        'def test():'
        '  print(1)'
        '  raise Exception()'
    )
    submission = base_create_submission(
        problem=problem,
        code=code)

    assert not submission.evaluated

    await submission.evaluate()

    assert not submission.has_passed
    assert submission.evaluated
    assert submission.stdout == ''
    assert 'raise Exception()' in submission.stderr


class TestSubmissionSerializer(ProblemMixin, TestCase):
    def test_create(self):
        problem = self.create_problem(run_script='test()')
        serializer = SubmissionSerializer(data=dict(
            problem=problem.id,
            code='def test(): pass'
        ))
        serializer.is_valid()
        submission = serializer.save()
        self.assertTrue(submission)

    def test_fields(self):
        problem = self.create_problem(run_script='test()')
        readonly_data = dict(
            evaluate=False,
            has_passed=0,
            stderr='err',
            stdout='out'
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

    def test_trim_space(self):
        'make sure code does not get trimmed'
        problem = self.create_problem(run_script='test()')
        code = '\n\n def test(): pass \n\n'
        data = dict(
            problem=problem.pk,
            code=code,
        )
        serializer = SubmissionSerializer(data=data)
        serializer.is_valid()
        submission = serializer.save()

        self.assertEqual(submission.code, code)


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

        response = self.api_create(data={})
        self.assertEqual(response.status_code, HTTP_405_METHOD_NOT_ALLOWED)
