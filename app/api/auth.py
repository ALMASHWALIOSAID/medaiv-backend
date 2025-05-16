from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.core.auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
    get_active_user,
    oauth2_scheme
)
from app.core.config import get_settings
from app.core.db import get_session
from app.core.security import hash_password
from app.models.schemas import Token, UserCreate
from app.models.user import User

router = APIRouter(prefix="/api")

settings = get_settings()

@router.post("/signup", response_model=User, status_code=status.HTTP_201_CREATED, tags=["auth"])
def signup(
    user_in: UserCreate,
    session: Session = Depends(get_session)
):
    # Prevent duplicate usernames
    existing = session.exec(select(User).where(User.username == user_in.username)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already registered")
    # Hash password and create user
    user = User(
        username=user_in.username,
        hashed_password=hash_password(user_in.password),
        disabled=False
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.post("/token", response_model=Token, tags=["auth"])
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=User, tags=["auth"])
async def read_users_me(current_user=Depends(get_active_user)):
    return current_user