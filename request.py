import os

class request:
    def __init__(self, imgPath):
        if(os.path.exists(imgPath)):
            self._imgPath = imgPath


    def getImage(self):
        if(self._imgPath != ''):
            return None
        return self._imgPath
