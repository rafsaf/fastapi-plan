import logging

from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed
from tortoise import Tortoise, run_async

try:
    import app
except ModuleNotFoundError:
    import os
    import pathlib
    import sys

    app = pathlib.Path(os.path.dirname(__file__)).parent
    sys.path.append(str(app))
    from app import crud, schemas
    from app.core.config import TORTOISE_ORM, settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@retry(
    wait=wait_fixed(1),
    stop=stop_after_attempt(30),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
async def initial():
    try:
        await Tortoise.init(config=TORTOISE_ORM)
        user = await crud.user.get_by_email(email=settings.FIRST_SUPERUSER_EMAIL)
        if not user:
            user_data = schemas.UserCreateBySuperuser(
                email=settings.FIRST_SUPERUSER_EMAIL,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                is_superuser=True,
            )
            await crud.user.create_by_superuser(user_data)
    except Exception as e:
        logger.error(e)
        raise Exception(e)


async def main() -> None:
    logger.info("Creating initial data")
    await initial()
    logger.info("Initial data created")


if __name__ == "__main__":
    run_async(main())
