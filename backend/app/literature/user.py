from sqlalchemy.orm import Session

from literature.crud import user_crud
from literature.models.user_model import UserModel

user_id: str = None


def set_global_user_id(db: Session, id: str):
    global user_id
    user_id = id

    if not db.query(UserModel).filter(UserModel.id == user_id).first():
        user_crud.create(db, user_id)


def get_global_user_id():
    return user_id
