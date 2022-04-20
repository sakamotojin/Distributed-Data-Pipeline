from queue import Queue


class QueueManager:
    __instance = None
    def __init__(self):
        if QueueManager.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            QueueManager.__instance = self
            self.queueMap = {}

    @staticmethod
    def getInstance():
        if QueueManager.__instance is None:
            QueueManager()
        return QueueManager.__instance

    def createQueue(self, name, queueSize):
        if name not in self.queueMap:
            self.queueMap[name] = Queue(queueSize + 500)

    def submitToQueue(self, name, data):
        try:
            if name not in self.queueMap:
                raise Exception('Invalid Queue Name : ' + name)
            self.queueMap[name].put(data)
        except Exception as e:
            pass

    def getFromQueue(self, name):
        try:
            if name not in self.queueMap:
                raise Exception('Invalid Queue Name : ' + name)
            if self.queueMap[name].empty():
                return None
            value = self.queueMap[name].get(block=False)
            self.queueMap[name].task_done()
            return value
        except Exception as e:
            return None