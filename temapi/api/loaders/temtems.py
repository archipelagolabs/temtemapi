from typing import Dict, Any, List

from temapi.api.loaders.loader import Loader


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
            (temtem['name'], temtem)
            for temtem in temtems
        )

    def get_by_id(self, _id):
        return self.by_id.get(_id)

    def get_by_name(self, name):
        return self.by_name.get(name)

    def list(self):
        return self.temtems
