import json

from temapi.commons.paths import OUTPUTS_DIR


class Loader:
    file = None

    def __init__(self):
        assert self.file is not None

        _file = OUTPUTS_DIR / self.file

        with _file.open() as f:
            data = json.load(f)

        self.setup(data)

    def setup(self, data):
        pass
