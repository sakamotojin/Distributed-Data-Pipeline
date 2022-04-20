from queue import Queue
from threading import Thread
from time import sleep

from utils.Logger import Logger
MAX_WAIT_TIME = 500000
SLEEP_TIME = 200


class ConcurrentExecutor:
    __instance = None
    def __init__(self, concurrent):
        if ConcurrentExecutor.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            ConcurrentExecutor.__instance = self
            self.concurrent = concurrent
            self.queue = Queue(concurrent * 2)
            self.threads = []
            self.initDaemons()
            Logger.getInstance().logInfo('ConcurrentExecutor :  STARTED, concurrent = ' + str(concurrent))

    @staticmethod
    def getInstance(concurrent):
        if ConcurrentExecutor.__instance is None:
            ConcurrentExecutor(concurrent)
        return ConcurrentExecutor.__instance


    def initDaemons(self):
        for i in range(self.concurrent):
            t = Thread(target=self.doWork)
            t.daemon = True
            self.threads.append(t)



    def submitJobs(self, jobs):
        try:
            for job in jobs:
                self.queue.put(job)
        except Exception as e:
            raise Exception('ConcurrentExecutor :  submitJobs : Error While Submiting Jobs : ' + str(e))

    def doWork(self):
        waitTime = MAX_WAIT_TIME
        while True:
            try:
                job = self.queue.get(block=False)
                job.init()
                job.run()
                job.cleanUp()
            except Exception as e:
                Logger.getInstance().logInfo('ConcurrentExecutor : Queue Empty ' + str(e))
                sleep(SLEEP_TIME)
                waitTime = waitTime - SLEEP_TIME
                if waitTime < 0 :
                    return

    def start(self):
        for t in self.threads:
            t.start()

    def waitForAll(self):
        for t in self.threads:
            t.join()
