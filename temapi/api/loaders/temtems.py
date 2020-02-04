from typing import Dict, List, Optional

from temapi.api.loaders.loader import Loader
from temapi.api.loaders.traits import trait_loader
from temapi.api.models import FullTemtem


class TemtemLoader(Loader):
    file = 'temtems.json'

    temtems: List[FullTemtem]
    by_id: Dict[int, FullTemtem]
    by_name: Dict[str, FullTemtem]

    def setup(self, data):
        self.temtems = [
            FullTemtem(**{
                **d,
                'traits': trait_loader.get_multiple_by_name(d['traits'])
            })
            for d in data
        ]

        self.by_id = dict(
            (temtem.id, temtem)
            for temtem in self.temtems
        )

        self.by_name = dict(
            (temtem.name.lower(), temtem)
            for temtem in self.temtems
        )

    def get_by_id(self, tid) -> Optional[FullTemtem]:
        return self.by_id.get(tid)

    def get_by_name(self, name) -> Optional[FullTemtem]:
        return self.by_name.get(name.lower())

    def all(self) -> List[FullTemtem]:
        return self.temtems


temtem_loader = TemtemLoader()
