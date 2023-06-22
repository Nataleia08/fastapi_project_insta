import cloudinary.uploader
from typing import List

from fastapi import APIRouter, HTTPException, Depends, Query, UploadFile, File
from sqlalchemy import func
from sqlalchemy.orm import Session
from starlette import status

from src.schemas import ImageResponse, ImageUpdateDescriptionRequest, ImageUpdateTagsRequest
from src.conf.config import settings, config_cloudinary
from src.database.db import get_db
from src.database.models import Image, Tag, User, Rating
from src.services.auth import auth_service
from src.services.auth_decorators import has_role
from src.database.models import allowed_get_comments, allowed_post_comments, allowed_put_comments, \
    allowed_delete_comments


router = APIRouter(prefix="/images", tags=["images"])


@router.post("/", response_model=ImageResponse)
# @has_role(allowed_get_comments)
async def create_image(image: UploadFile = File(...), description: str = None, tags: List[str] = [],
                       db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    try:
        config_cloudinary()

        uploaded_image = cloudinary.uploader.upload(image.file)

        image_url = uploaded_image['secure_url']

        image = Image(image=image_url, description=description, user_id=current_user.id)

        for tag_data in tags:
            tag = db.query(Tag).filter_by(name=tag_data).first()
            if not tag:
                tag = Tag(name=tag_data)
                db.add(tag)
            image.tags.append(tag)

        db.add(image)
        db.commit()
        db.refresh(image)

        return ImageResponse(
            id=image.id,
            image=image.image,
            description=image.description,
            tags=tags
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{image_id}")
# @has_role(allowed_delete_comments)
async def delete_image(image_id: int, db: Session = Depends(get_db)):
    try:
        image = db.query(Image).filter(Image.id == image_id).first()
        if not image:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

        db.delete(image)
        db.commit()
        return {"message": "Image deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/{image_id}/update-image", response_model=ImageResponse)
# @has_role(allowed_get_comments)
async def update_image_image(image_id: int, image_data: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        config_cloudinary()

        image = db.query(Image).filter(Image.id == image_id).first()
        if not image:
            raise HTTPException(status_code=404, detail="Image not found")

        public_id = f"UsersPhoto/{image.id}"
        cloudinary.uploader.destroy(public_id)

        uploaded_image = cloudinary.uploader.upload(image_data.file, public_id=public_id)

        image_url = uploaded_image['secure_url']

        image.image = image_url

        db.commit()
        rating = db.query(func.avg(Rating.numbers_rating)).filter(Rating.image_id == image.id).scalar()
        return ImageResponse(
            id=image.id,
            image=image.image,
            description=image.description,
            tags=[tag.name for tag in image.tags],
            rating=rating
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{image_id}/update-tags", response_model=ImageResponse)
# @has_role(allowed_get_comments)
async def update_image_tags(
        image_id: int,
        tags: List[str] = Query(..., description="List of tags to update for the image"),
        db: Session = Depends(get_db)):
    try:
        image = db.query(Image).filter(Image.id == image_id).first()
        if not image:
            raise HTTPException(status_code=404, detail="Image not found")

        image.tags.clear()

        for tag_data in tags:
            tag = db.query(Tag).filter_by(name=tag_data).first()
            if not tag:
                tag = Tag(name=tag_data)
                db.add(tag)
            image.tags.append(tag)

        db.commit()
        db.refresh(image)
        rating = db.query(func.avg(Rating.numbers_rating)).filter(Rating.image_id == image.id).scalar()
        return ImageResponse(
            id=image.id,
            image=image.image,
            description=image.description,
            tags=[tag.name for tag in image.tags],
            rating=rating
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{image_id}/update-description", response_model=ImageResponse)
# @has_role(allowed_get_comments)
async def update_image_description(image_id: int, description: ImageUpdateDescriptionRequest,
                                   db: Session = Depends(get_db)):
    try:
        image = db.query(Image).filter(Image.id == image_id).first()
        if not image:
            raise HTTPException(status_code=404, detail="Image not found")

        image.description = description.description
        db.commit()
        db.refresh(image)
        rating = db.query(func.avg(Rating.numbers_rating)).filter(Rating.image_id == image.id).scalar()
        return ImageResponse(
            id=image.id,
            image=image.image,
            description=image.description,
            tags=[tag.name for tag in image.tags],
            rating=rating
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{image_id}", response_model=ImageResponse)
# @has_role(allowed_get_comments)
async def get_image(image_id: int, db: Session = Depends(get_db)):
    try:
        image = db.query(Image).filter(Image.id == image_id).first()
        if not image:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
        rating = db.query(func.avg(Rating.numbers_rating)).filter(Rating.image_id == image.id).scalar()
        return ImageResponse(
            id=image.id,
            image=image.image,
            description=image.description,
            tags=[tag.name for tag in image.tags],
            rating=rating
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/", response_model=List[ImageResponse])
# @has_role(allowed_get_comments)
async def get_images_by_tags(tags: List[str] = Query(...), db: Session = Depends(get_db)):
    try:
        images = db.query(Image).join(Image.tags).filter(Tag.name.in_(tags)).all()

        filtered_images = [image for image in images if set(tags).issubset({tag.name for tag in image.tags})]

        image_responses = []
        for image in filtered_images:
            rating = db.query(func.avg(Rating.numbers_rating)).filter(Rating.image_id == image.id).scalar()
            image_responses.append(ImageResponse(
                id=image.id,
                image=image.image,
                description=image.description,
                tags=[tag.name for tag in image.tags],
                rating=rating
            ))

        return image_responses
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
