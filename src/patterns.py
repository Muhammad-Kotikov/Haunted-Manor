from abc import abstractmethod, ABC

class Command(ABC):

    def __init__(self, receiver):
            self.receiver = receiver

    @abstractmethod
    def execute(self) -> None:
        pass