import enum

from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime, func, Boolean, Text, Date, Float, Enum

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class UserRole(str, enum.Enum):
    admin: str = 'admin'
    moderator: str = 'moderator'
    user: str = 'user'


    # class UserRole(str, Enum):
    #     USER = "user"
    #     MODERATOR = "moderator"
    #     ADMIN = "admin"

allowed_get_comments = [UserRole.user]
allowed_post_comments = [UserRole.admin, UserRole.moderator, UserRole.user]
allowed_put_comments = [UserRole.admin, UserRole.moderator]
allowed_delete_comments = [UserRole.admin]

#
# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True)
#     username = Column(String(50))
#     email = Column(String(250), nullable=False, unique=True)
#     password = Column(String(255), nullable=False)
#     avatar = Column(String(255), nullable=True)
#     refresh_token = Column(String(255), nullable=True)
#     role = Column('role', Enum(Role), default=Role.user)
#     confirmed = Column(Boolean, default=False)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column('crated_at', DateTime, default=func.now())
    username = Column(String(50))
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)

    role = Column('role', Enum(UserRole), default=UserRole.user)
    # role = Column(String(20), default=UserRole.USER)

    confirmed = Column(Boolean, default=False)   # ------------------------------  False


class BlacklistToken(Base):
    __tablename__ = 'blacklist_tokens'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    token = Column(String(255), nullable=False)


class UserProfile(Base):
    __tablename__ = 'users_profiles'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(50))
    phone = Column(String(50))
    # date_of_birth = Column(Date)
    date_of_birth = Column(String(50))
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)
    user = relationship('User', backref='user_profiles')




# class Owner(Base):
#     __tablename__ = "owners"
#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, unique=True, index=True)
#     created_at = Column(DateTime, default=func.now())
#     updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
#
#
# class Cat(Base):
#     __tablename__ = "cats"
#
#     id = Column(Integer, primary_key=True, index=True)
#     nick = Column(String, index=True)
#     age = Column(Integer)
#     vaccinated = Column(Boolean, default=False)
#     description = Column(String)
#     owner_id = Column(Integer, ForeignKey("owners.id"), nullable=True)
#     owner = relationship("Owner", backref="cats")
#     created_at = Column(DateTime, default=func.now())
#     updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class Qr(Base):
    __tablename__ = "qrs"
    id = Column(Integer, primary_key=True, index=True)
    image_id = Column('image_id', ForeignKey('images.id', ondelete='CASCADE'), default=None)
    image = relationship('Image', backref="qrs")
    qr_code_url = Column(Text)


class Rating(Base):
    __tablename__ = "ratings"
    id = Column(Integer, primary_key=True, autoincrement=True)
    numbers_rating = Column(Integer)
    text_rating = Column(String(255))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    image_id = Column('image_id', ForeignKey('images.id', ondelete='CASCADE'), default=None)
    user = relationship('User', backref="ratings")
    image = relationship('Image', backref="ratings")


class RatingImage(Base):
    __tablename__ = "ratings_images"
    id = Column(Integer, primary_key=True, autoincrement=True)
    now_number_rating = Column(Float)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    image_id = Column('image_id', ForeignKey('images.id', ondelete='CASCADE'), default=None)
    image = relationship('Image', backref="ratings_images")






class Image(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    image = Column(String, nullable=False)
    description = Column(String)
    tags = relationship('Tag', secondary='image_tag')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    is_active = Column(Boolean, default=True)

    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    user = relationship('User', backref="users")

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    images = relationship('Image', secondary='image_tag')


image_tag = Table(
    'image_tag',
    Base.metadata,
    Column('image_id', Integer, ForeignKey('images.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)





class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    update_status = Column(Boolean, default=False)

    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    user = relationship('User', backref="comments")
    image_id = Column('image_id', ForeignKey('images.id', ondelete='CASCADE'), default=None)
    image = relationship('Image', backref="comments")




