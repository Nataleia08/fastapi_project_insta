from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from src.database.models import User, Rating, Image, RatingImage
from src.database.db import get_db
from src.conf.config import settings
from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File, Path
from sqlalchemy import and_
from src.schemas import RatingResponseModel, RatingRequestModel
from typing import List
from src.repository.rating import calculate_total_rating
from src.services.auth import auth_service
from src.services.auth_decorators import has_role
from src.database.models import allowed_get_comments, allowed_post_comments, allowed_put_comments, \
    allowed_delete_comments

router = APIRouter(prefix='/rating', tags=["rating"])


@router.post("/", response_model=RatingResponseModel)
# @has_role(allowed_get_comments)
async def create_rating(body: RatingRequestModel, image_id: int, db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):
    new_rating = db.query(Rating).filter(and_(Rating.image_id == image_id, Rating.user_id == current_user.id)).first()
    if new_rating:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This rating is exists!")
    image_r = db.query(Image).filter(Image.id == image_id).first()
    if image_r is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Image not found!')
    if image_r.user_id == current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can't complete this action!!")
    new_rating = Rating(**body.dict(), user_id=current_user.id, image_id=image_id)
    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)
    await calculate_total_rating(image_id=image_id, db=db, user_id=current_user.id)
    return new_rating


@router.get("/{image_id}", response_model=List[RatingResponseModel])
# @has_role(allowed_put_comments)
async def get_image_rating(image_id: int, db: Session = Depends(get_db)):
    image_r = db.query(Image).filter(Image.id == image_id).first()
    if image_r is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Image not found!')
    list_rating = db.query(Rating).filter(Rating.image_id == image_id).all()
    return list_rating


@router.get("/users/{user_id}", response_model=List[RatingResponseModel])
# @has_role(allowed_put_comments)
async def get_user_rating(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found!')
    list_rating_users = db.query(Rating).filter(Rating.user_id == user_id).all()
    return list_rating_users


@router.delete("/{rating_id}")
# @has_role(allowed_put_comments)
async def delete_rating(image_id: int, user_id: int, db: Session = Depends(get_db)):
    new_rating = db.query(Rating).filter(and_(Rating.image_id == image_id, Rating.user_id == user_id)).first()
    if new_rating is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Rating not found!')
    db.delete(new_rating)
    db.commit()
