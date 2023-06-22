from fastapi import HTTPException, status
from functools import wraps
from src.database.models import Image, Comment, User, UserRole

from src.database.models import allowed_get_comments, allowed_post_comments, allowed_put_comments, \
    allowed_delete_comments

from src.database.db import get_db


def has_role(role):
    def decorator(view_func):
        @wraps(view_func)
        async def wrapper(image_id=None, body=None, db=None, current_user=None):
            if not image_id:
                if current_user.role not in role:
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient privileges")
            else:
                image_user_id = db.query(Image).filter(Image.id == image_id).first().user_id
                if current_user.role not in role and image_user_id != current_user.id:
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                        detail="Insufficient privileges for current user")
            return await view_func(current_user)

        return wrapper

    return decorator
