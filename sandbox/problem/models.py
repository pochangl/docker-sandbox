from django.db import models
from worker import executor


class Problem(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    run_script = models.TextField()

    def run(self, code):
        '''
            merge code with run_script
            then execute the merged code
        '''
        merged_code = '{}\n{}'.format(code, self.run_script)
        return executor.run('python', '3.7', merged_code)

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

    def evaluate(self):
        '''
            evaluate result
        '''
        try:
            self.stdout = self.problem.run(self.code)
        except executor.ExecutionError as error:
            self.stderr = str(error)
        finally:
            self.evaluated = True
