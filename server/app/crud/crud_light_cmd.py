
   
from typing import Any, Dict, Optional, Union
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.schemas.light_cmd import LightCommand, LightCommandCreate, LightCommandUpdate
from app.models.light_cmd import LightCommand as LightCommandModel

class CRUDLightCmd(CRUDBase[LightCommand, LightCommandCreate, LightCommandUpdate]):
    def update(
        self,
        db: Session,
        *,
        db_obj: LightCommandModel,
        obj_in: LightCommandUpdate,
    ) -> LightCommand:
        db_obj = super().update(db, db_obj=db_obj, obj_in=obj_in)
        return db_obj

light_cmd = CRUDLightCmd(LightCommandModel)