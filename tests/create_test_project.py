"""
Creates template project in current folder with default values
"""
from pathlib import Path
from re import TEMPLATE
from cookiecutter.main import cookiecutter

ROOT_FOLDER = Path(__file__).parent.parent
TEMPLATE = f"{ROOT_FOLDER}/fastapi_plan/template"


def main():
    cookiecutter(
        template=TEMPLATE,
        no_input=True,
        extra_context={
            "project_name": "test_project",
            "preffered_requirements_tool": "poetry",
        },
    )


if __name__ == "__main__":
    main()
