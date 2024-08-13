from invoke import task

SRC_ROOT = "src/"
TEST_ROOT = "src/test/"


@task
def test(c):
    print("Running unit tests...")
    c.run("python -m unittest discover -v")


@task
def mypy(c):
    print("Running mypy...")
    c.run(f"mypy {SRC_ROOT}")

@task
def formatter(c):
    print("Running black formatter...")
    c.run(f"python -m black {SRC_ROOT}")


@task
def linter(c):
    print("Running flake8...")
    # E501 is turned off - ignore long lines and whitespaces
    c.run(f"flake8 --extend-ignore=E501,W291,W293 {SRC_ROOT}")


@task
def bandit(c):
    print("Running bandit security checks...")
    c.run(f"bandit -r {SRC_ROOT} --skip B101,B301,B403")
    c.run(f"bandit -r {TEST_ROOT } --skip B101,B301,B403")


@task
def isort(c):
    print("Running isort...")
    c.run(f"isort --atomic .")


@task
def checks(c):
    print("Running all checks...")
    isort(c)
    mypy(c)
    formatter(c)
    linter(c)
    bandit(c)
    test(c)


