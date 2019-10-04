from django.contrib import admin
from . import models


@admin.register(models.Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title')


@admin.register(models.Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('has_passed', 'time_created')
