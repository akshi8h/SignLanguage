from abc import ABC, abstractmethod

class BasePredictor(ABC):
    @abstractmethod
    def predict(self, features):
        """
        Returns:
        label (str), confidence (float)
        """
        pass
