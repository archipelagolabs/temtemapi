from typing import Dict, List

from temapi.api.loaders.loader import Loader
from temapi.commons.models import Trait


class TraitLoader(Loader):
    file = 'traits.json'

    traits: List[Trait]
    by_name: Dict[str, Trait]

    def setup(self, data):
        self.traits = [Trait(**d) for d in data]

        self.by_name = dict(
            (t.name, t)
            for t in self.traits
        )

    def all(self) -> List[Trait]:
        return self.traits

    def get_by_name(self, name):
        return self.by_name.get(name)

    def get_multiple_by_name(self, names):
        traits = (
            self.get_by_name(n)
            for n in names
        )

        return [
            t
            for t in traits
            if t is not None
        ]


trait_loader = TraitLoader()
