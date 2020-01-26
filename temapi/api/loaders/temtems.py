from typing import Dict, Any, List, Optional

from temapi.api.loaders.loader import Loader
from temapi.commons.models import Temtem


class TemtemLoader(Loader):
    file = 'temtems.json'

    temtems: List[Any]
    by_id: Dict[int, Any]
    by_name: Dict[str, Any]

    def setup(self, temtems):
        self.temtems = temtems

        self.by_id = dict(
            (temtem['id'], temtem)
            for temtem in temtems
        )

        self.by_name = dict(
            (temtem['name'].lower(), temtem)
            for temtem in temtems
        )

    def get_by_id(self, tid) -> Optional[Temtem]:
        return self.by_id.get(tid)

    def get_by_name(self, name) -> Optional[Temtem]:
        return self.by_name.get(name.lower())

    def all(self) -> List[Temtem]:
        return self.temtems
