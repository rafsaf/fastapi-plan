import logging
from pathlib import Path

from cookiecutter.exceptions import OutputDirExistsException
from cookiecutter.main import cookiecutter

TEMPLATE_DIR = Path(__file__).parent

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s -   %(message)s")

logger = logging.getLogger(
    name="fastapi-plan",
)

# print() below for newlines


def main():
    try:
        print()
        logger.warning("Enter fiew basic information about project")
        print()
        cookiecutter(template=f"{TEMPLATE_DIR}/template")
    except OutputDirExistsException:
        print()
        logger.error("FAILED")
        logger.error("Directory with such a name already exists!")
    except Exception as exc:
        print()
        logger.error("FAILED")
        logger.error(f"{exc}")
    else:
        print()
        logger.info("SUCCESS")
        logger.info("Project successfully generated.")


if __name__ == "__main__":
    main()
