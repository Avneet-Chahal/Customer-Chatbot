from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def get_data_dir() -> Path:
    """Resolve data folder (repo uses Data/, code historically used data/)."""
    for name in ("data", "Data"):
        path = PROJECT_ROOT / name
        if path.is_dir():
            return path
    raise FileNotFoundError(
        "Data directory not found. Expected 'Data/' or 'data/' at project root."
    )


def data_path(filename: str) -> Path:
    return get_data_dir() / filename
