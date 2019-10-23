from ..models import Problem, Submission


def create_problem(run_script):
    return Problem.objects.create(
        title='title',
        description='description',
        run_script=run_script
    )


def create_submission(**kwargs):
    return Submission.objects.create(**kwargs)
