import pandas as pd
from pathlib import Path


class DataFrameCache:
    def __init__(self) -> None:
        self.df: pd.DataFrame = None
        self.cache_path: str = None

    def exists(self, cache_path: str) -> bool:
        return Path(cache_path).exists()

    def get(self, cache_path: str) -> pd.DataFrame:
        return pd.read_pickle(cache_path)

    def save(self, cache_path) -> None:
        if self.df is None:
            raise ValueError("The dataframe is not defined.")
        self.df.to_pickle(cache_path)
