from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schema.users import (
    UserResponse,
    Token,
    RefreshTokenRequest
)
from app.crud.user import get_user_by_email, create_user
from app.core.auth import (
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_refresh_token
)


router = APIRouter(
    prefix="/auth",
    tags=["Signup"]
)


class LoginForm:
    def __init__(
        self,
        username: str = Form(...),
        password: str = Form(...)
    ):
        self.username = username
        self.password = password


class RegisterForm:
    def __init__(
        self,
        name: str = Form(...),
        email: str = Form(...),
        password: str = Form(...),
        role: str = Form("student")
    ):
        self.name = name
        self.email = email
        self.password = password
        self.role = role


@router.post("/register", response_model=UserResponse)
def register_user(
    user: RegisterForm = Depends(),
    db: Session = Depends(get_db)
):
    existing_user = get_user_by_email(db, user.email)

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    return create_user(db, user)


@router.post("/login", response_model=Token)
def login_user(
    form_data: LoginForm = Depends(),
    db: Session = Depends(get_db)
):
    db_user = get_user_by_email(db, form_data.username)

    if db_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        form_data.password,
        db_user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={
            "sub": db_user.email,
            "role": db_user.role
        }
    )

    refresh_token = create_refresh_token(
        data={
            "sub": db_user.email,
            "role": db_user.role
        }
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh")
def refresh_access_token(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    payload = verify_refresh_token(
        request.refresh_token
    )

    email = payload.get("sub")

    user = get_user_by_email(
        db,
        email
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    access_token = create_access_token(
        data={
            "sub": user.email,
            "role": user.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }