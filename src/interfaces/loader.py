from abc import ABC, abstractmethod
from typing import Any


class Loader(ABC):
    @abstractmethod
    def loader(self,load_type,**kwargs) -> Any:
        pass


