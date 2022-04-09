from abc import ABC, abstractmethod
from ..Constant import Constant


class BaseComponent(ABC):
    ''' base component handler '''

    @abstractmethod
    def toJson(self):
        """
        Return all useful value as a dict. This dict must
        be transform to json by the caller
        """
        pass
