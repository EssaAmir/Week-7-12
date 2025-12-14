class Dataset:
    """Represents a data science dataset in the platform."""

    def __init__(self, dataset_id: int, name: str, size_bytes: int, rows: int, source: str):
        self._id = dataset_id
        self._name = name
        self._size_bytes = size_bytes
        self._rows = rows
        self._source = source

    def calculate_size_mb(self) -> float:
        return self._size_bytes / (1024 * 1024)

    def get_source(self) -> str:
        return self._source

    def __str__(self) -> str:
        return f"Dataset: {self._name} ({self.calculate_size_mb():.2f} MB)"