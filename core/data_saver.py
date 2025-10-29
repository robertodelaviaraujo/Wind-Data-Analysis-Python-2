import gzip
import pickle
from core.data_store import DataStore


def save_project(file_path: str, data_store: DataStore):
    with gzip.open(file_path, "wb") as f:
        pickle.dump(data_store, f)


def load_project(file_path: str) -> DataStore:
    with gzip.open(file_path, "rb") as f:
        data = pickle.load(f)
    return data
