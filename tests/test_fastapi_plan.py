import random
import string
from pathlib import Path

r"""
In the root folder

$ pytest tests --template fastapi_plan\template

Where `template` is path to folder with `cookiecutter.json` file
See https://github.com/hackebrot/pytest-cookies

Or example tests here 
https://github.com/audreyfeldroy/cookiecutter-pypackage/blob/master/tests/test_bake_project.py

# from py._path.local import LocalPath
"""


ROOT_FOLDER = Path(__file__).parent.parent
PROJECT_TEMPLATE = f"{ROOT_FOLDER}/fastapi_plan/template"


def random_lower_string(length=20) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=length))


def test_bake_project_poetry(cookies):
    project_name = random_lower_string()
    result = cookies.bake(
        template=PROJECT_TEMPLATE,
        extra_context={
            "project_name": project_name,
            "preffered_requirements_tool": "poetry",
        },
    )

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project.basename == project_name
    assert result.project.isdir()
    top_level = [f.basename for f in result.project.listdir()]
    assert "requirements.txt" not in top_level
    assert "poetry.lock" in top_level
    assert "pyproject.toml" in top_level

    # the rest
    assert ".dockerignore" in top_level
    assert ".env" in top_level
    assert "aerich.ini" in top_level
    assert "app" in top_level
    assert "config" in top_level
    assert "docker-compose.yml" in top_level
    assert "Dockerfile" in top_level
    assert "pytest.ini" in top_level
    assert ".gitignore" in top_level


def test_bake_project_requiremnts(cookies):
    project_name = random_lower_string()
    result = cookies.bake(
        template=PROJECT_TEMPLATE,
        extra_context={
            "project_name": project_name,
            "preffered_requirements_tool": "requirements.txt",
        },
    )

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project.basename == project_name
    assert result.project.isdir()
    top_level = [f.basename for f in result.project.listdir()]
    assert "requirements.txt" in top_level
    assert "poetry.lock" not in top_level
    assert "pyproject.toml" not in top_level

    # the rest
    assert ".dockerignore" in top_level
    assert ".env" in top_level
    assert "aerich.ini" in top_level
    assert "app" in top_level
    assert "config" in top_level
    assert "docker-compose.yml" in top_level
    assert "Dockerfile" in top_level
    assert "pytest.ini" in top_level
    assert ".gitignore" in top_level
