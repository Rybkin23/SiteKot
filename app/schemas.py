from datetime import datetime

from pydantic import BaseModel


class ProjectBase(BaseModel):
    title: str
    description: str


class ProjectCreate(ProjectBase):
    image_url: str

    class Config:
        from_attributes = True


class Project(ProjectBase):
    id: int
    image_url: str

    class Config:
        from_attributes = True


class ContactBase(BaseModel):
    name: str
    email: str


class ContactCreate(ContactBase):
    message: str


class Contact(ContactBase):
    id: int
    message: str
    created_at: datetime

    class Config:
        from_attributes = True
