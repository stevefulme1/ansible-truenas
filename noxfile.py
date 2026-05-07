import nox

nox.options.sessions = ["lint", "sanity"]


@nox.session(python=["3.12", "3.13"])
def lint(session):
    session.install("ansible-lint")
    session.run("ansible-lint", ".")


@nox.session(python=["3.12", "3.13"])
def sanity(session):
    session.install("ansible-core>=2.16")
    session.run(
        "ansible-test", "sanity", "--local", "-v", "--color",
        "--python", f"{session.python}",
    )


@nox.session(python=["3.12", "3.13"])
def security(session):
    session.install("bandit")
    session.run("bandit", "-r", "plugins/", "-ll", "-ii")
