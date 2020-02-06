from typing import List

from invoke import Result, UnexpectedExit, task

PACKAGE = 'temapi'


def check_all(results: List[Result]):
    try:
        result = next(result for result in results if result.exited != 0)
    except StopIteration:
        pass
    else:
        raise UnexpectedExit(result)


@task
def format(c):
    c.run(f'black -q {PACKAGE}')
    c.run(f'black -q tasks.py')
    c.run(f'isort -rc -y -q {PACKAGE}')
    c.run(f'isort -rc -y -q tasks.py')


@task
def lint(c):
    c.run(f'pylint --rcfile=pylintrc {PACKAGE}', warn=True),


@task
def format_check(c):
    check_all(
        [
            c.run(f'black --check -q {PACKAGE}', warn=True),
            c.run(f'black --check -q tasks.py', warn=True),
            c.run(f'isort -rc -c -q {PACKAGE}', warn=True),
            c.run(f'isort -rc -c -q tasks.py', warn=True),
        ]
    )
