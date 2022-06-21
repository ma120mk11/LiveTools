from app.crud.base import CRUDBase

from app.models.footswitch import Footswitch as FootswitchModel, Button as ButtonModel
from app.schemas.footswitch import Button, ButtonCreate, ButtonUpdate, Footswitch, FootswitchBase, FootswitchUpdate

class CRUDFootswitch(CRUDBase[Footswitch, FootswitchBase, FootswitchUpdate]):
    ...

class CRUDFsButton(CRUDBase[Button, ButtonCreate, ButtonUpdate]):
    ...

footswitch = CRUDFootswitch(FootswitchModel)
fs_button = CRUDFsButton(ButtonModel)