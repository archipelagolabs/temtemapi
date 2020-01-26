from typing import List

from temapi.api.loaders.loader import Loader
from temapi.commons.models import Trait


class TraitLoader(Loader):
    file = 'traits.json'

    traits: List[Trait]

    def setup(self, data):
        self.traits = [Trait(**d) for d in data]

    def all(self) -> List[Trait]:
        return self.traits
