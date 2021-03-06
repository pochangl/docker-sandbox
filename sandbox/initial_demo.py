from problem.models import Problem


def initial_problem():
    # default problem - two sum
    Problem.objects.create(
        title='two sum',
        description='create a function named \'two_sum\' with two parameters (a, b) that adds up two numbers',
        image='python:3.7',
        run_script="{% import_main %}\nassert main.two_sum(1, 2) == 3, 'two_sum(1, 2) returns {}'.format(main.two_sum(1, 2))\nprint('two_sum(1, 2) = {}'.format(main.two_sum(1, 2)))",
        initial_code="def two_sum(a, b):",
    )

    # default problem - html dom
    Problem.objects.create(
        title='html tag',
        output_type='text/html',
        description='create a variable named \'html_tag\' that contains html tag',
        image='python:3.7',
        run_script='{% import_main %}\nprint(main.html_tag)',
        initial_code="html_tag = ",
    )


if not Problem.objects.count():
    initial_problem()
