import asyncio
import logging

from sqlalchemy import select

from . import models
from .config.logging_config import configure_logging
from .database import AsyncSessionLocal, Base, engine

configure_logging()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        result = await db.execute(select(models.Project))
        existing_projects = result.scalars().all()

        if not existing_projects:
            projects = [
                models.Project(
                    title="Брендинг для кафе",
                    description="Логотип и фирменный стиль",
                    image_url="uploads/project1.jpg",
                ),
                models.Project(
                    title="Корпоративный сайт",
                    description="Веб-дизайн и разработка",
                    image_url="uploads/project2.jpg",
                ),
                models.Project(
                    title="Мобильное приложение",
                    description="UI/UX дизайн",
                    image_url="uploads/project3.jpg",
                ),
            ]

            db.add_all(projects)
            await db.commit()
            logging.info("Добавлены тестовые проекты")
        else:
            logging.info(f"В базе уже есть {len(existing_projects)} проектов")


async def main():
    await init_db()


if __name__ == "__main__":
    asyncio.run(main())
