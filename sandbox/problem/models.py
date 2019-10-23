from django.db import models
from worker import dispatcher


class Problem(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    run_script = models.TextField()

    async def run(self, code):
        '''
            merge code with run_script
            then execute the merged code
        '''
        merged_code = '{}\n{}'.format(code, self.run_script)
        return await dispatcher.run('python', '3.7', merged_code)

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

    async def evaluate(self):
        '''
            evaluate result
        '''
        result = await self.problem.run(self.code)
        self.stdout = result.stdout
        self.stderr = result.stderr
        self.evaluated = True
