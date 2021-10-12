from crud.base import CRUDBase
from schemas.users import UserCreate, UserUpdate
from database.models import User


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    pass


crud_users = CRUDUser(User)
