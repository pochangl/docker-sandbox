from django.urls import path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'problem', views.ProblemViewSet, 'problem')
router.register(r'submission', views.SubmissionViewSet, 'submission')

urlpatterns = router.urls
