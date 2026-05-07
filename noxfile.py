import nox
import os
import shutil
import sys

nox.options.sessions = ["lint", "sanity"]

_python = os.environ.get("NOX_PYTHON", f"{sys.version_info.major}.{sys.version_info.minor}")

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


@nox.session(python=_python)
def lint(session):
    session.install("ansible-lint")
    session.run("ansible-lint", ".")


@nox.session(python=_python)
def sanity(session):
    session.install("ansible-core>=2.16")
    _install_collection(session)
    session.chdir(COLLECTION_PATH)
    session.run(
        "ansible-test", "sanity", "--local", "-v", "--color",
        "--python", "default",
    )


@nox.session(python=_python)
def security(session):
    session.install("bandit")
    session.run("bandit", "-r", "plugins/", "-ll", "-ii")
