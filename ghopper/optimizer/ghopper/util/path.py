import os
from os import path
import pathlib


class Path:
    """
    Functions to manipulate the filesystem.
    """

    def __init__(self, path: str = ""):
        self.path = path
        self.stem = pathlib.Path(path).stem

    def size_in_bytes(self, path: str = ""):
        return pathlib.Path(path).stat().st_size

    def mkdir(self):
        os.mkdir(self.path)

    def makedirs(self):
        os.makedirs(self.path)

    def rmdir(self):
        os.rmdir(self.path)

    def removedirs(self):
        os.removedirs(self.path)

    def remove(self):
        os.remove(self.path)

    def exists(self):
        return path.exists(self.path)

    def glob(self, path, pattern: str) -> list[str]:
        files = []
        paths = pathlib.Path(path).glob(pattern)
        for pure_path in paths:
            files += [str(pure_path)]
        return files

    def with_suffix(self, suffix: str):
        return str(pathlib.Path(self.path).with_suffix(suffix))
