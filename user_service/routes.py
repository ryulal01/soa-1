from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User
from auth import hash_password, verify_password, create_jwt_token, get_current_user
from schemas import UserCreate, UserUpdate, UserAuth, UserResponse

router = APIRouter()

@router.post("/register/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login/")
def login(user: UserAuth, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    token = create_jwt_token({"sub": user.username})
    return {"access_token": token}

@router.put("/update/", response_model=UserResponse)
def update_profile(update_data: UserUpdate, db: Session = Depends(get_db), username: str = Depends(get_current_user)):
    db_user = db.query(User).filter(User.username == username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    update_dict = update_data.dict(exclude_unset=True)
    if "username" in update_dict or "password" in update_dict:
        raise HTTPException(status_code=400, detail="Cannot update username or password")

    for key, value in update_dict.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/profile/", response_model=UserResponse)
def get_profile(db: Session = Depends(get_db), username: str = Depends(get_current_user)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

