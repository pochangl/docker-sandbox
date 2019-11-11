from problem.models import Problem


def initial_problem():
    # default problem - two sum
    Problem.objects.create(
        title='two sum',
        description='create a function named \'two_sum\' with two parameters (a, b) that adds up two numbers',
        run_script="assert two_sum(1, 2) == 3, 'two_sum(1, 2) returns {}'.format(two_sum(1, 2))\nprint('two_sum(1, 2) = {}'.format(two_sum(1, 2)))"
    )

    # default problem - html dom
    Problem.objects.create(
        title='html tag',
        output_type='text/html',
        description='create a variable named \'html_tag\' that contains html tag',
        run_script='print(html_tag)',
    )


if not Problem.objects.count():
    initial_problem()
