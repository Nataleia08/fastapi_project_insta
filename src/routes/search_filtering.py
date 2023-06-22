from fastapi import APIRouter, Query, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List

from src.database.db import get_db
from src.database.models import Image, Tag, Rating
from src.schemas import ImageResponse, ImageWithCreatedAtResponse

router = APIRouter(prefix="/search_filtering", tags=["search_filtering"])


@router.get("/", response_model=List[ImageResponse])
async def search_images_by_tags(tags: List[str] = Query(...), db: Session = Depends(get_db)):
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


@router.get("/by_description", response_model=List[ImageResponse])
async def search_images_by_description(description: str = Query(...), db: Session = Depends(get_db)):
    try:
        images = db.query(Image).filter(Image.description.ilike(f"%{description}%")).all()

        image_responses = []
        for image in images:
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


# ___________________________________________________________

@router.post("/sorted-by-rating", response_model=List[ImageResponse])
def get_images_sorted_by_rating(
        images: List[ImageResponse],
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100)
):
    sorted_images = sorted(
        images,
        key=lambda img: img.rating if img.rating is not None else float('-inf'),
        reverse=True
    )
    return sorted_images[skip: skip + limit]


@router.post("/sorted-by-date", response_model=List[ImageWithCreatedAtResponse])
def get_images_sorted_by_date(
        images: List[ImageResponse],
        db: Session = Depends(get_db),
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100)
):
    image_ids = [image.id for image in images]
    db_images = db.query(Image).filter(Image.id.in_(image_ids)).all()
    image_map = {image.id: image for image in db_images}

    sorted_with_created_at = [
        ImageWithCreatedAtResponse(
            id=image.id,
            image=image.image,
            description=image.description,
            tags=image.tags,
            rating=image.rating,
            created_at=image_map[image.id].created_at.strftime("%Y-%m-%d %H:%M") if image.id in image_map else None
        )
        for image in images
    ]

    sorted_with_created_at = [
        img for img in sorted_with_created_at if img.created_at is not None
    ]

    sorted_with_created_at.sort(key=lambda img: img.created_at, reverse=True)

    return sorted_with_created_at[skip: skip + limit]
