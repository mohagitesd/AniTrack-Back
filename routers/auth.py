from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models.user import User
from core.database import get_session
from core.security import hash_password,verify_password, create_access_token
from schemas.user import UserCreate ,UserLogin
from core.security import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=User)
def register(user_data: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.exec(select(User).where(User.email == user_data.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")

    hashed_pw = hash_password(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_pw
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@router.post("/login")
def login(data: UserLogin, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == data.email)).first()

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Identifiants invalides")

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me")
def read_current_user(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email
    }
