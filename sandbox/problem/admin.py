from django.contrib import admin
from . import models


@admin.register(models.Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'image', 'output_type')


@admin.register(models.Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'problem', 'has_passed', 'time_created')
    readonly_fields = ('problem', 'code', 'evaluated', 'stderr', 'stdout')
