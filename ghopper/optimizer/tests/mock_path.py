from ghopper.util.path import Path


class MockPath(Path):
    def __init__(self):
        self._size_in_bytes = None
        self._glob = None

    def return_size_in_bytes(self, value):
        self._size_in_bytes = value

    def size_in_bytes(self, executable_path):
        return self._size_in_bytes

    def return_glob(self, value):
        self._glob = value

    def glob(self, path, pattern):
        return self._glob
