from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas


async def get_project(db: AsyncSession, project_id: int):
    result = await db.execute(
        select(models.Project).filter(models.Project.id == project_id)
    )
    return result.scalar_one_or_none()


async def get_projects(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Project).offset(skip).limit(limit))
    return result.scalars().all()


async def create_project(db: AsyncSession, project: schemas.ProjectCreate):
    db_project = models.Project(**project.model_dump())
    db.add(db_project)
    await db.commit()
    await db.refresh(db_project)
    return db_project


async def delete_project(db: AsyncSession, project_id: int):
    project = await get_project(db, project_id)
    if project:
        await db.delete(project)
        await db.commit()
        return project
    return None


async def get_contacts(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(models.Contact)
        .order_by(models.Contact.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def create_contact(db: AsyncSession, contact: schemas.ContactCreate):
    db_contact = models.Contact(**contact.model_dump())
    db.add(db_contact)
    await db.commit()
    await db.refresh(db_contact)
    return db_contact
