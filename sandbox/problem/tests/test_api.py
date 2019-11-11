import pytest
from django.test import TestCase
from rest_framework import status
from utils.rest_framework import ViewsetTestMixin
from .utils import create_problem, create_submission
from ..serializers import SubmissionSerializer
from .. import models


class ProblemMixin:
    def create_problem(self, *args, **kwargs):
        return create_problem(*args, **kwargs)

    def create_submission(self, *args, **kwargs):
        return create_submission(*args, **kwargs)


'''
    Test Model
'''


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
        models.Problem.objects.all().delete()
        problem = self.create_problem()
        content = self.api_list().json
        self.assertEqual(len(content), 1, content)
        self.assertTrue(content[0]['id'], problem.pk)

    def test_retrieve(self):
        problem = self.create_problem()
        content = self.api_retrieve(pk=problem.pk).json
        self.assertEqual(content['id'], problem.pk)

        # test fields
        for name in ['id', 'title', 'description', 'output_type']:
            self.assertIn(name, content)

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
