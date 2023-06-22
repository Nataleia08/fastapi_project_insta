from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
import cloudinary
import cloudinary.uploader

from src.database.models import Image, User
from src.database.db import get_db
from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File, Path
from sqlalchemy import and_
from src.schemas import ImageResponseCloudinaryModel

from src.conf.config import config_cloudinary
from src.services.auth import auth_service
from src.services.auth_decorators import has_role
from src.database.models import allowed_get_comments, allowed_post_comments, allowed_put_comments, \
    allowed_delete_comments

router = APIRouter(prefix='/cloudinary', tags=["cloudinary"])
security = HTTPBearer()


@router.patch('/{image_id}', response_model=ImageResponseCloudinaryModel)
# @has_role(allowed_get_comments)
async def cloudinary_set(image_id: int = Path(description="The ID of the image", ge=1), file: UploadFile = File(),
                         current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    config_cloudinary()

    new_image = db.query(Image).filter(and_(Image.id == image_id, Image.user_id == current_user.id)).first()
    # new_image = db.query(Image).filter((Image.id == image_id)).first()
    if new_image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    r = cloudinary.uploader.upload(file.file, public_id=f'UsersPhoto/{new_image.user_id}/{new_image.id}',
                                   overwrite=True)
    src_url = cloudinary.CloudinaryImage(f'UsersPhoto/{new_image.user_id}/{new_image.id}') \
        .build_url(width=250, height=250, crop='fill', version=r.get('version'))
    new_image.image = src_url
    db.commit()
    return new_image


@router.patch("/{image_id}/cropped", response_model=ImageResponseCloudinaryModel)
# @has_role(allowed_get_comments)
async def cloudinary_cropped(image_id: int = Path(description="The ID of the image", ge=1), height: int = 100,
                             width: int = 100, current_user: User = Depends(auth_service.get_current_user),
                             db: Session = Depends(get_db)):
    config_cloudinary()

    new_image = db.query(Image).filter(and_(Image.id == image_id, Image.user_id == current_user.id)).first()
    # new_image = db.query(Image).filter((Image.id == image_id)).first()
    if new_image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    try:
        new_url = cloudinary.CloudinaryImage(f'UsersPhoto/{new_image.user_id}/{new_image.id}').build_url(height=height,
                                                                                                         width=width,
                                                                                                         crop="fill")
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Attribute is not correctly!")
    new_image.image = new_url
    db.commit()
    return new_image


@router.patch("/{image_id}/scaled", response_model=ImageResponseCloudinaryModel)
# @has_role(allowed_get_comments)
async def cloudinary_scaled(image_id: int = Path(description="The ID of the image", ge=1), crop: str = "fill",
                            blur: int = 100, current_user: User = Depends(auth_service.get_current_user),
                            db: Session = Depends(get_db)):
    config_cloudinary()

    new_image = db.query(Image).filter(and_(Image.id == image_id, Image.user_id == current_user.id)).first()
    # new_image = db.query(Image).filter((Image.id == image_id)).first()
    if new_image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    try:
        new_url = cloudinary.CloudinaryImage(f'UsersPhoto/{new_image.user_id}/{new_image.id}').build_url(crop=crop,
                                                                                                         effect=f"blur:{blur}")
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Attribute is not correctly!")
    new_image.image = new_url
    db.commit()
    return new_image


@router.patch("/{image_id}/zoom", response_model=ImageResponseCloudinaryModel)
# @has_role(allowed_get_comments)
async def cloudinary_zoom(image_id: int = Path(description="The ID of the image", ge=1), zoom: float = 1.0,
                          current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    config_cloudinary()

    new_image = db.query(Image).filter(and_(Image.id == image_id, Image.user_id == current_user.id)).first()
    # new_image = db.query(Image).filter((Image.id == image_id)).first()
    if new_image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    try:
        new_url = cloudinary.CloudinaryImage(f'UsersPhoto/{new_image.user_id}/{new_image.id}').build_url(zoom=zoom)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Attribute is not correctly!")
    new_image.image = new_url
    db.commit()
    return new_image


@router.patch("/{image_id}/radius", response_model=ImageResponseCloudinaryModel)
# @has_role(allowed_get_comments)
async def cloudinary_radius(image_id: int = Path(description="The ID of the image", ge=1),
                            current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    config_cloudinary()

    new_image = db.query(Image).filter(and_(Image.id == image_id, Image.user_id == current_user.id)).first()
    # new_image = db.query(Image).filter((Image.id == image_id)).first()
    if new_image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    try:
        new_url = cloudinary.CloudinaryImage(f'UsersPhoto/{new_image.user_id}/{new_image.id}').build_url(radius="max")
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Attribute is not correctly!")
    new_image.image = new_url
    db.commit()
    return new_image


# shadow
@router.patch("/{image_id}/shadow", response_model=ImageResponseCloudinaryModel)
# @has_role(allowed_get_comments)
async def cloudinary_radius(image_id: int = Path(description="The ID of the image", ge=1), color: str = "black",
                            x: int = 10, y: int = 10, current_user: User = Depends(auth_service.get_current_user),
                            db: Session = Depends(get_db)):
    config_cloudinary()

    new_image = db.query(Image).filter(and_(Image.id == image_id, Image.user_id == current_user.id)).first()
    # new_image = db.query(Image).filter((Image.id == image_id)).first()
    if new_image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    try:
        new_url = cloudinary.CloudinaryImage(f'UsersPhoto/{new_image.user_id}/{new_image.id}').build_url(color=color,
                                                                                                         effect="shadow",
                                                                                                         x=x, y=y)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Attribute is not correctly!")
    new_image.image = new_url
    db.commit()
    return new_image
