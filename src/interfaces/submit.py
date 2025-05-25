from abc import ABC, abstractmethod
from typing import Any
class DataSubmit(ABC):
    @abstractmethod
    def submit(self,data) -> Any:
        """
        提交数据到服务器的抽象方法。
        """
        pass