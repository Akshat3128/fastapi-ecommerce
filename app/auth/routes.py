from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from . import schemas, models, utils
from .schemas import UserSignin, TokenOut
from app.auth.models import User
from app.auth.utils import verify_password, create_access_token
from app.auth.utils import get_current_user
from fastapi.security import HTTPAuthorizationCredentials
from jose import jwt
from app.core.config import settings
from .schemas import ForgotPasswordRequest, ResetPasswordRequest
from .utils import create_reset_token, verify_reset_token
from app.auth.utils import send_reset_email
from app.core.logger import logger


router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup", response_model=schemas.UserOut)
def signup(user_data: schemas.UserSignup, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if existing_user:
        logger.info(f"User Already Exists During Signup: {user_data.email}")
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = utils.hash_password(user_data.password)
    new_user = models.User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed_password,
        role=user_data.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logger.info(f"New signup: {user_data.email}")
    return new_user

@router.post("/signin", response_model=TokenOut)
def signin(user_cred: UserSignin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_cred.email).first()

    if not user or not verify_password(user_cred.password, user.hashed_password):
        logger.warning(f"Failed login attempt for {user_cred.email}")
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(data={"sub": user.email, "role": user.role})
    logger.info(f"User logged in: {user.email}")
    return {"access_token": token, "token_type": "bearer"}

@router.get("/profile")
def get_my_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role
    }

@router.get("/me")
def read_profile(token: HTTPAuthorizationCredentials = Depends(utils.oauth2_scheme)):
    print("Token from Swagger:", token.credentials)
    payload = jwt.decode(token.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    print("Payload:", payload)
    return payload


# //reset routes
@router.post("/forgot-password")
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = create_reset_token(user.email)
    send_reset_email(user.email, token)
    logger.info(f"Password reset requested for {request.email}")
    return {"message": "Reset email sent"}


@router.post("/reset-password")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    email = verify_reset_token(request.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.hashed_password = utils.hash_password(request.new_password)
    db.commit()
    logger.info(f"Password reset completed for {email}")
    return {"message": "Password reset successful"}
