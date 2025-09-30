import os
import secrets
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

load_dotenv()

security = HTTPBasic()


def get_current_admin(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    correct_username = os.getenv("ADMIN_USERNAME", "admin")
    correct_password = os.getenv("ADMIN_PASSWORD", "admin")

    username_correct = secrets.compare_digest(credentials.username, correct_username)
    password_correct = secrets.compare_digest(credentials.password, correct_password)

    if not (username_correct and password_correct):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверные учетные данные",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
