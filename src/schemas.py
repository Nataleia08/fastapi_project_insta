from typing import Optional

from src.database.models import UserRole, User
from datetime import datetime, date
from pydantic import BaseModel, Field, constr, EmailStr

from typing import List, Optional
from fastapi import UploadFile
from pydantic.types import conlist


# class OwnerModel(BaseModel):
#     email: EmailStr
#
#
# class OwnerResponse(BaseModel):
#     id: int = 1
#     email: EmailStr
#
#     class Config:
#         orm_mode = True
#
class ImageCreateRequest(BaseModel):
    image: str
    description: str = None
    tags: conlist(constr(max_length=50), min_items=1, max_items=5) = []


class ImageUpdateRequest(BaseModel):
    description: str
    tags: conlist(constr(max_length=50), min_items=1, max_items=5) = []


class ImageResponse(BaseModel):
    id: int
    image: str
    description: str
    tags: conlist(constr(max_length=50), min_items=1, max_items=5) = []
    rating: Optional[int]

    # возможно стоит тут добавить поле rating если да то и в search_filtering тоже
    class Config:
        orm_mode = True


class ImageUpdateImageRequest(BaseModel):
    image: UploadFile


class ImageUpdateTagsRequest(BaseModel):
    tags: conlist(constr(max_length=50), min_items=1, max_items=5) = []


class ImageUpdateDescriptionRequest(BaseModel):
    description: str


# class CatModel(BaseModel):
#     nick: str = Field('Barsik', min_length=3, max_length=16)
#     age: int = Field(1, ge=1, le=30)
#     vaccinated: Optional[bool] = False
#     description: str
#     owner_id: int = Field(1, gt=0)  # ge >=  gt >
#
#
# class CatVaccinatedModel(BaseModel):
#     vaccinated: bool = False
#
#
# class CatResponse(BaseModel):
#     id: int = 1
#     nick: str = 'Barsik'
#     age: int = 12
#     vaccinated: bool = False
#     description: str
#     owner: OwnerResponse
#
#     class Config:
#         orm_mode = True
#
#
# class UserModel(BaseModel):
#     username: str = Field(min_length=5, max_length=12)
#     email: EmailStr
#     password: str = Field(min_length=6, max_length=8)
#
#
# class UserResponse(BaseModel):
#     id: int
#     username: str
#     email: EmailStr
#     avatar: str
#     role: Role
#
#     class Config:
#         orm_mode = True
#
class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: EmailStr
    password: str = Field(min_length=6, max_length=10)


class UserResponse(BaseModel):
    id: int = 1
    username: str = "username"
    email: EmailStr = "useruser@example.com"
    avatar: str
    role: UserRole = UserRole.user
    detail: str = "User successfully created"

    class Config:
        orm_mode = True


# class UserDb(BaseModel):                   #     где используется?????????????
#     id: int
#     username: str
#     email: str
#     created_at: datetime
#     role: UserRole = UserRole.USER
#     avatar: str
#
#     class Config:
#         orm_mode = True


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class BlacklistTokenCreate(BaseModel):
    token: str


class UserProfileCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    date_of_birth: date


class UserProfileResponse(BaseModel):
    id: int
    user_id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    date_of_birth: date

    class Config:
        orm_mode = True


class ImageResponseCloudinaryModel(BaseModel):
    id: int
    image: str
    is_active: bool

    # created_at: datetime
    # update_at: datetime
    # user_id: int

    class Config():
        orm_mode = True


class RatingRequestModel(BaseModel):
    numbers_rating: int
    text_rating: str
    # user_id: int = Field(1, gt=0)
    # image_id: int = Field(1, gt=0)


class RatingResponseModel(BaseModel):
    id: int
    numbers_rating: int
    text_rating: str
    user_id: int
    image_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class CommentBase(BaseModel):
    text: str = Field(max_length=500)


class CommentModel(CommentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    user_id: int
    image_id: int
    update_status: bool = False

    class Config:
        orm_mode = True


class CommentUpdate(CommentModel):
    update_status: bool = True
    updated_at = datetime

    class Config:
        orm_mode = True


class ImageWithCreatedAtResponse(BaseModel):
    id: int
    image: str
    description: str
    tags: conlist(constr(max_length=50), min_items=1, max_items=5) = []
    rating: Optional[int]
    created_at: datetime


# class CommentModel(BaseModel):
#     id: int
#     comment: str = Field(max_length=512)
#     # created_at: datetime                                  это в моделях
#     # updated_at: Optional[datetime]
#     user_id: int
#     image_id: int
#     update_status: bool = False
#
# class CommentUpdate(BaseModel):
#     update_status: bool = True
#     updated_at = datetime
#
#     class Config:
#         orm_mode = True


#
# class TokenModel(BaseModel):
#     access_token: str
#     refresh_token: str
#     token_type: str = "bearer"
#
#
# class RequestEmail(BaseModel):
#     email: EmailStr
#
#
# class TestForm(BaseModel):
#     email: EmailStr
#     text: str
