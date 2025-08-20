import shutil
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

from fastapi import Depends, FastAPI, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .auth import get_current_admin
from .config.template_config import setup_templates
from .database import SessionLocal, engine

# Создание приложения
app = FastAPI()

# Настройка базы данных
models.Base.metadata.create_all(bind=engine)

# Настройка шаблонов
templates = setup_templates()

# Настройка статических файлов
BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


# Зависимость для БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Роут для создания проектов
@app.post("/admin/projects")
async def create_project(
    title: str = Form(...),
    description: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # Сохранение изображения
    file_path = f"uploads/{image.filename}"
    with open(f"app/static/{file_path}", "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    # Создание проекта в БД
    project = schemas.ProjectCreate(
        title=title, description=description, image_url=file_path
    )
    crud.create_project(db, project)
    return RedirectResponse(url="/admin", status_code=303)


# Роут для удаления проектов
@app.get("/admin/delete_project/{project_id}", response_class=RedirectResponse)
async def delete_project(
    project_id: int,
    admin: str = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    crud.delete_project(db, project_id)
    response = RedirectResponse(url="/admin", status_code=303)
    response.set_cookie(
        key="flash_message", value=quote("Проект успешно удален"), max_age=3
    )
    return response


# Роут админки
@app.get("/admin", response_class=HTMLResponse)
async def admin_panel(
    request: Request,
    admin: str = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    projects = crud.get_projects(db)
    contacts = crud.get_contacts(db)
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
    db: Session = Depends(get_db),
):
    try:
        # Создаем контакт
        contact = schemas.ContactCreate(
            name=name,
            email=email,
            message=message,
            created_at=datetime.now(timezone.utc),
        )
        crud.create_contact(db, contact)

        # Устанавливаем flash-сообщение
        response = RedirectResponse(url="/", status_code=303)
        response.set_cookie(
            key="flash_message",
            value=quote("Сообщение успешно отправлено!"),
            max_age=3,
            httponly=True,
            samesite="lax",
        )
        return response

    except Exception:
        response = RedirectResponse(url="/", status_code=303)
        response.set_cookie(
            key="flash_message",  # Первый cookie
            value=quote("Ошибка при отправке сообщения"),
            max_age=5,
        )
        response.set_cookie(  # Второй отдельный cookie
            key="flash_type", value="error", max_age=5
        )
        return response


# Роут фронтенда
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: Session = Depends(get_db)):
    projects = crud.get_projects(db)
    return templates.TemplateResponse(
        "index.html", {"request": request, "projects": projects}
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
