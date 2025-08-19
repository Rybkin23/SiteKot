from urllib.parse import unquote


def urldecode_filter(s):
    """Фильтр для декодирования URL-encoded строк в шаблонах Jinja2"""
    return unquote(s if s else "")


def add_template_filters(app):
    """Регистрирует все кастомные фильтры в приложении"""
    app.env.filters["urldecode"] = urldecode_filter
