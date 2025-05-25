from abc import ABC, abstractmethod
from typing import Any


class NetworkFetch(ABC):

    @abstractmethod
    def fetch(self, data) -> Any:
        pass
