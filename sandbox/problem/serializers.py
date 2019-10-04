from rest_framework import serializers
from . import models


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Problem
        fields = ('id', 'title', 'description')


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Submission
        fields = ('id', 'problem', 'code', 'error', 'evaluated', 'has_passed')
        read_only_fields = ('error', 'evaluated', 'has_passed')

    def create(self, *args, **kwargs):
        submission = super().create(*args, **kwargs)
        submission.evaluate()
        submission.save()
        return submission
