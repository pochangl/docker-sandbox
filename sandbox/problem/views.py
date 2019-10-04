from rest_framework import viewsets, permissions, mixins
from . import models, serializers


class ProblemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Problem.objects.all()
    serializer_class = serializers.ProblemSerializer


class SubmissionViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    queryset = models.Submission.objects.all()
    serializer_class = serializers.SubmissionSerializer
