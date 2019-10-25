from django.db import models
from worker import dispatcher


class Problem(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    run_script = models.TextField()

    def __str__(self):
        return self.title


class Submission(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.PROTECT)
    code = models.TextField()
    evaluated = models.BooleanField(default=False)
    stderr = models.TextField(default='')
    stdout = models.TextField(default='')
    time_created = models.DateTimeField(auto_now_add=True)

    @property
    def has_passed(self):
        return self.stderr == ''

    def process_evaluation(self, result):
        self.stdout = result['stdout']
        self.stderr = result['stderr']
        self.evaluated = True
        self.save()

    @property
    def run_params(self):
        merged_code = '{}\n{}'.format(self.code, self.problem.run_script)
        return dict(image='python', tag='3.7', text=merged_code)
