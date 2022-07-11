import logging
from typing import List, Optional
from app import crud
from app.crud.base import CRUDBase
from sqlalchemy.orm import Session
from app.constants import speech

from fastapi.encoders import jsonable_encoder

from app.models.setlist import Setlist as SetlistModel
from app.schemas.setlist import Setlist, SetlistCreate, SetlistFull, SetlistUpdate
from app.schemas.song import SongAction

logger = logging.getLogger(__name__)


class CRUDUser(CRUDBase[Setlist, SetlistCreate, SetlistUpdate]):
    def get(self, db: Session, id: int) -> Optional[SetlistFull]:
        set_db = super().get(db=db, id=id)
        return self._transform_set(set_db=set_db, db=db)

    def get_multi(self, db: Session, skip: int = 0, limit: int = 5000) -> List[SetlistFull]:
        setlists_db = super().get_multi(db, skip=skip, limit=limit)
        sets_full: List[SetlistFull] = []
        
        for set in setlists_db:
            sets_full.append(self._transform_set(set, db=db))
        return sets_full
    
    def _transform_set(self, set_db: Setlist, db: Session) -> SetlistFull:
        set = jsonable_encoder(set_db)

        for index, action_id in enumerate(set['actions']):

            #Speech
            if set['actions'][index] == 1000:
                set['actions'][index] = speech.speech
            else:
                song_action: SongAction = SongAction(**jsonable_encoder(crud.song.get_song(db=db, song_id=action_id, include_lyrics=False)))
                set['actions'][index] = jsonable_encoder(song_action)

        set_full: SetlistFull = SetlistFull(**set)
        # logger.info(set_full)
        return set_full

setlist = CRUDUser(SetlistModel)