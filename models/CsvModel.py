from utils.Visenze import convertListToStr


class CSVModel:

    def __init__(self, obj):
        self.obj = obj

    def getDictForCSV(self):
        try:
            finalDict = {}
            for key in self.obj.__dict__.keys():
                if self.obj.__dict__[key] is None:
                    finalDict[key] = convertListToStr('')
                elif isinstance(self.obj.__dict__[key], list):
                    finalDict[key] = convertListToStr(self.obj.__dict__[key], '|')
                else:
                    finalDict[key] = str(self.obj.__dict__[key])
            return finalDict
        except Exception as e:
            return str(self.obj)