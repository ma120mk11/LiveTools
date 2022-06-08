from app.crud.base import CRUDBase

from app.models.user import User
from app.schemas.user import User, UserCreate, UserUpdate

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    ...


user = CRUDUser(User)