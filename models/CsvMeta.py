class CSVMeta:
    
    def __init__(self, outputFile):
        self.outputFile = outputFile

        
    def setFields(self, fields:list):
        self.fields = fields