from abc import ABC, abstractmethod
from typing import Any
class DataParse(ABC):
    @abstractmethod
    def parse(self, data) -> Any:
        pass
