import os

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


if __name__ == "__main__":

    if "{{ cookiecutter.preffered_requirements_tool }}" == "poetry":
        pass
    else:
        remove_file("pyproject.toml")
        remove_file("poetry.lock")
