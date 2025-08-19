from datetime import datetime
from urllib.parse import unquote

from fastapi.templating import Jinja2Templates


def setup_templates():
    templates = Jinja2Templates(directory="app/templates")

    # Регистрация фильтров
    filters = {
        "urldecode": lambda s: unquote(s if s else ""),
        "format_date": lambda dt: dt.strftime("%d.%m.%Y %H:%M") if dt else "",
    }

    templates.env.filters.update(filters)

    # Глобальные переменные шаблонов
    templates.env.globals.update({"current_year": datetime.now().year})

    return templates
