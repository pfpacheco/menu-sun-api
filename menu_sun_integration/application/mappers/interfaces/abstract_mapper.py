import abc
from typing import Dict, Optional


class AbstractMapper(abc.ABC):
    @abc.abstractmethod
    def visit(self, entity) -> Optional[Dict]:
        raise NotImplementedError
