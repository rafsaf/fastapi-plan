import logging
from pathlib import Path

from cookiecutter.exceptions import FailedHookException, OutputDirExistsException
from cookiecutter.main import cookiecutter

__version__ = "0.1.0"
TEMPLATE_DIR = Path(__file__).parent
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(name="fastapi-plan")


def main():
    try:
        cookiecutter(template=f"{TEMPLATE_DIR}/template")
    except (FailedHookException, OutputDirExistsException) as exc:
        if isinstance(exc, OutputDirExistsException):
            logger.error("Directory with such a name already exists!")
        return
    else:
        logger.info("Project successfully generated.")


if __name__ == "__main__":
    main()
