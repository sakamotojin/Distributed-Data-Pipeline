from time import sleep
import requests

from models.Request import Request
from utils.Logger import Logger

TIMEOUT = 15

class HTTPClient:

    @staticmethod
    def getPOSTResponse(request: Request, max_tries=3):
        errorResp = ''
        while max_tries > 0:
            response = requests.request("POST", request.url, headers=request.headers, data=request.body, timeout=TIMEOUT)
            if response.status_code != 200:
                max_tries = max_tries - 1
                errorResp = response
                sleep(1)
                continue
            else:
                return response
        Logger.getInstance().logError(" HTTP Client POST : " + str(request))
        raise Exception("HTTPClient-getPOSTResponse MAX-TRIES " + str(max_tries) + " Exceeded " + str(errorResp.status_code) + str(errorResp.reason))

    @staticmethod
    def getGETResponse(request: Request, max_tries=3):
        errorResp = ''
        while max_tries > 0:
            response = requests.request("GET", request.url, headers=request.headers, params=request.params, timeout=TIMEOUT)
            if response.status_code != 200:
                max_tries = max_tries - 1
                errorResp = response
                sleep(1)
                continue
            else:
                return response
        raise Exception("HTTPClient-getGETResponse MAX-TRIES " + str(max_tries) + " Exceeded " + str(errorResp))