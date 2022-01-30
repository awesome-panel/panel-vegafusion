"""Module of Invoke build tasks to be invoked from the command line. Try

invoke --list=build

from the command line for a list of all available commands.
"""

from invoke import task


@task(aliases=["js"])
def javascript(command):
    """Builds the panel-vegafusion Javascript package

    """
    print(
        """Builds the panel-vegafusion Javascript package

=================================================
"""
    )
    with command.cd("src-js"):
        command.run("npm run build", echo=True)

@task(aliases=["package"])
def python_package(command):
    """Builds the panel-vegafusion Python package

    Remember to update the version number
    """
    print(
        """Builds the panel-vegafusion Python package

Remember to update the version number
=================================================
"""
    )
    command.run("python setup.py sdist bdist_wheel", echo=True)
