from . import models
from .database import SessionLocal


def init_db():
    db = SessionLocal()

    # Проверяем, есть ли уже проекты
    if not db.query(models.Project).count():
        # Добавляем тестовые проекты
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
        db.commit()
        print("Добавлены тестовые проекты")

    db.close()


if __name__ == "__main__":
    init_db()
