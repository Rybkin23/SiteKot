from datetime import datetime

import pytz
from sqlalchemy import Column, DateTime, Integer, String, Text

from .database import Base

SAMARA_TZ = pytz.timezone("Europe/Samara")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)
    description = Column(Text)
    image_url = Column(String(200))  # Путь к изображению относительно /static/


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100))
    message = Column(Text)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(SAMARA_TZ))
