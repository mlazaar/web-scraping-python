class Utils:
    
    def __init__(self):
        super().__init__()

    def convertStringToInt(self, string):
        try:
            toInt = int(string)
        except:
            toInt = 0
        return toInt