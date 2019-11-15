from ..models import Problem, Submission


def create_problem(run_script, **kwargs):
    data = dict(
        title='title',
        description='description',
        run_script=run_script,
        image='python:3.7'
    )
    data.update(kwargs)
    return Problem.objects.create(**data)


def create_submission(**kwargs):
    return Submission.objects.create(**kwargs)
