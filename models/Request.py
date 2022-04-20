class Request(object):

    def __init__(self, url, headers, body, params):
        self.url = url
        self.headers = headers
        self.body = body
        self.params = params

    def __str__(self):
        return str(self.__dict__)