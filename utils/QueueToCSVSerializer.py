import os
from time import sleep

import pandas as pd

from models.CSVMeta import CSVMeta
from models.CSVModel import CSVModel
from utils.QueueManager import QueueManager


class SerializerToCSV:

    @staticmethod
    def serializeQueueToCSv(queueName: str, csvMeta: CSVMeta):
        while True :
            file = csvMeta.outputFile
            batch = SerializerToCSV.getProductsFromQueue(queueName)
            if batch is None:
                return
            df = pd.DataFrame(batch, index=None)
            if csvMeta.fields is not None:
                df.to_csv(file, index=False, encoding='utf-8', mode='a', header=not os.path.exists(file), columns=csvMeta.fields)
            else:
                df.to_csv(file, index=False, encoding='utf-8', mode='a', header=not os.path.exists(file))

    @staticmethod
    def getProductsFromQueue(queueName, MAX_WAIT=30000000000):
        waitTime = MAX_WAIT
        batch = SerializerToCSV.getBatchProducts(queueName)
        while not batch:
            sleep(20)
            if waitTime == 0:
                return None
            batch = SerializerToCSV.getBatchProducts(queueName)
            waitTime = waitTime - 1
        return batch

    @staticmethod
    def getBatchProducts(queueName, MAX_BATCH_SIZE=10000):
        batch = []
        productsInBatch = 0
        queueManager = QueueManager.getInstance()
        while True:
            product = queueManager.getFromQueue(queueName)
            if product is None:
                break
            else:
                product = CSVModel(product)
                batch.append(product.getDictForCSV())
                if productsInBatch == MAX_BATCH_SIZE:
                    break
            productsInBatch = productsInBatch + 1
        return batch


def test():
    p1 = {'a': 1, 'b': 2, 'c': {'a': 1}}
    p2 = {'a': 2, 'b': 2, 'c': 3}
    p3 = {'a': 3, 'b': 2, 'c': 3}
    c = CSVMeta('test.csv')
    c.setFields(['a', 'b', 'c'])

    q = QueueManager.getInstance()
    q.createQueue("test", 10)
    q.submitToQueue("test", p1)
    q.submitToQueue("test", p2)
    q.submitToQueue("test", p3)

    SerializerToCSV.serializeQueueToCSv('test', c)