from typing import Dict, List, Optional

from temapi.api.loaders.loader import Loader
from temapi.commons.models import Technique


class TechniqueLoader(Loader):
    file = 'techniques.json'

    techniques: List[Technique]
    by_name: Dict[str, Technique]

    def setup(self, data):
        self.techniques = [Technique(**d) for d in data]

        self.by_name = dict(
            (technique.name.lower(), technique) for technique in self.techniques
        )

    def get_by_name(self, name) -> Optional[Technique]:
        return self.by_name.get(name.lower().replace('-', ' '))


technique_loader = TechniqueLoader()
