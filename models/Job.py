from abc import abstractmethod, ABC

class Job(ABC):

    @abstractmethod
    def init(self):
        raise NotImplementedError

    @abstractmethod
    def cleanUp(self):
        raise NotImplementedError

    @abstractmethod
    def checkStatus(self):
        raise NotImplementedError

    @abstractmethod
    def run(self):
        raise NotImplementedError