from typing import List, Optional

from temapi.api.loaders.loader import Loader
from temapi.commons.models import Item


class ItemLoader(Loader):
    file = 'items.json'

    items: List[Item]

    def setup(self, data):
        self.items = [Item(**d) for d in data]

        self.by_name = dict(
            (item['name'].lower(), item)
            for item in data
        )
    
    def get_by_name(self, name) -> Optional[Item]:
        return self.by_name.get(name.lower())

    def all(self) -> List[Item]:
        return self.items
