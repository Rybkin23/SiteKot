import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

from fastapi import Depends, FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud, schemas
from .auth import get_current_admin
from .config.logging_config import configure_logging
from .config.template_config import setup_templates
from .database import get_db
from .initial_data import init_db

app = FastAPI()

templates = setup_templates()
configure_logging()

BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


@app.on_event("startup")
async def startup_event():
    await init_db()
    logging.info("Приложение запущено, база данных инициализирована")


@app.post("/admin/projects")
async def create_project(
    title: str = Form(...),
    description: str = Form(...),
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    try:
        file_path = f"uploads/{image.filename}"
        static_path = f"app/static/{file_path}"

        os.makedirs(os.path.dirname(static_path), exist_ok=True)
        file_content = await image.read()

        with open(static_path, "wb") as buffer:
            buffer.write(file_content)

        project_data = schemas.ProjectCreate(
            title=title, description=description, image_url=file_path
        )

        await crud.create_project(db, project_data)
        logging.info(f"Проект {title} создан")
        return RedirectResponse(url="/admin", status_code=303)

    except Exception as e:
        logging.error(f"Ошибка при создании проекта: {e}")
        import traceback

        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/admin/delete_project/{project_id}", response_class=RedirectResponse)
async def delete_project(
    project_id: int,
    admin: str = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    await crud.delete_project(db, project_id)
    logging.info(f"Проект id={project_id} удалён")
    response = RedirectResponse(url="/admin", status_code=303)
    response.set_cookie(
        key="flash_message", value=quote("Проект успешно удален"), max_age=2
    )
    return response


@app.get("/admin", response_class=HTMLResponse)
async def admin_panel(
    request: Request,
    admin: str = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    projects = await crud.get_projects(db)
    contacts = await crud.get_contacts(db)
    return templates.TemplateResponse(
        "admin.html",
        {
            "request": request,
            "projects": projects,
            "contacts": contacts,
            "admin": True,
        },
    )


@app.post("/submit_contact", response_class=RedirectResponse)
async def create_contact(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    try:
        contact_data = schemas.ContactCreate(
            name=name,
            email=email,
            message=message,
            created_at=datetime.now(timezone.utc),
        )
        await crud.create_contact(db, contact_data)
        logging.info(f"Сообщение от {name} email {email} отправлено")

        response = RedirectResponse(url="/", status_code=303)
        response.set_cookie(
            key="flash_message",
            value=quote("Сообщение успешно отправлено!"),
            max_age=2,
            httponly=True,
            samesite="lax",
        )
        return response

    except Exception as e:
        logging.error(f"Error creating contact: {e}")
        response = RedirectResponse(url="/", status_code=303)
        response.set_cookie(
            key="flash_message",
            value=quote("Ошибка при отправке сообщения"),
            max_age=2,
        )
        response.set_cookie(key="flash_type", value="error", max_age=2)
        return response


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: AsyncSession = Depends(get_db)):
    projects = await crud.get_projects(db)
    return templates.TemplateResponse(
        "index.html", {"request": request, "projects": projects}
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
