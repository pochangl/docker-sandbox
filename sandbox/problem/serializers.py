from rest_framework import serializers
from . import models


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Problem
        fields = ('id', 'title', 'description')


class SubmissionSerializer(serializers.ModelSerializer):

    # trimming is unexpected and biased
    code = serializers.CharField(trim_whitespace=False, max_length=10240)

    class Meta:
        model = models.Submission
        fields = ('id', 'problem', 'code', 'stdout', 'stderr', 'evaluated', 'has_passed')
        read_only_fields = ('id', 'stderr', 'stdout', 'evaluated', 'has_passed')
