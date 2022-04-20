from dask import dataframe as dd
from utils.Logger import Logger
from models.Product import Product
from utils.QueueManager import QueueManager


class ProductDeSerializer:

    @staticmethod
    def submitProductsToQueue(filename, queueName):
        Logger.getInstance().logInfo('ProductDeSerializer : submitProductsToQueue STARTED')
        try:
            queueManager = QueueManager.getInstance()
            dask_df = dd.read_csv(filename)
            for index, row in dask_df.iterrows():
                try:
                    queueManager.submitToQueue(queueName, ProductDeSerializer.createProduct(row))
                except Exception as e:
                    Logger.getInstance().logError('ProductDeSerializer : submitProductsToQueue : ' + str(e))
        except Exception as e:
            raise Exception('ProductDeSerializer : submitProductsToQueue : ' + str(e))

        Logger.getInstance().logInfo('ProductDeSerializer : submitProductsToQueue COMPLETED')

    @staticmethod
    def createProduct(row):
        if 'product_id' not in row:
            raise Exception(' FSN Not Found ' + str(row))
        product = Product(row['product_id'])
        return product