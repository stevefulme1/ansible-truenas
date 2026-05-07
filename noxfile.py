import nox
import os
import shutil

nox.options.sessions = ["lint", "sanity"]

COLLECTION_PATH = os.path.join(
    os.path.expanduser("~"),
    ".ansible", "collections", "ansible_collections", "truenas", "storage",
)


def _install_collection(session):
    if os.path.exists(COLLECTION_PATH):
        shutil.rmtree(COLLECTION_PATH)
    shutil.copytree(
        ".",
        COLLECTION_PATH,
        ignore=shutil.ignore_patterns(".nox", "__pycache__", "*.egg-info"),
    )


@nox.session(python=["3.12", "3.13"])
def lint(session):
    session.install("ansible-lint")
    session.run("ansible-lint", ".")


@nox.session(python=["3.12", "3.13"])
def sanity(session):
    session.install("ansible-core>=2.16")
    _install_collection(session)
    session.chdir(COLLECTION_PATH)
    session.run(
        "ansible-test", "sanity", "--local", "-v", "--color",
        "--python", "default",
    )


@nox.session(python=["3.12", "3.13"])
def security(session):
    session.install("bandit")
    session.run("bandit", "-r", "plugins/", "-ll", "-ii")
