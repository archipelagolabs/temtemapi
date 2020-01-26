import ujson

from temapi.api.loaders.utils import PROJECT_ROOT, OUTPUTS_DIR


class Loader:
    file = None

    def __init__(self):
        assert self.file is not None

        _file = OUTPUTS_DIR / self.file

        with _file.open() as f:
            data = ujson.load(f)

        self.setup(data)

    def setup(self, data):
        pass
