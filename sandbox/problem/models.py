from django.db import models
from utils import docker
from utils import executor


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


class Submission(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.PROTECT)
    code = models.TextField()
    evaluated = models.BooleanField(default=False)
    error = models.TextField(default='')
    time_created = models.DateTimeField(auto_now_add=True)

    @property
    def has_passed(self):
        return self.error == ''

    def evaluate(self):
        '''
            evaluate result
        '''
        try:
            return self.problem.run(self.code)
        except docker.ExecutionError as error:
            self.error = str(error)
        finally:
            self.evaluated = True