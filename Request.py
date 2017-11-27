import os

"""
    This class is an abstract interface wrapper for a request to any module of webSight.
    You must use this class as a request to specific module you want to use.
"""
class Request:

    """
    Request c-tor

    Args:
        - imgPath: a path to an image you want to load to webSite

    Attributes:
        - (private) _imgPath: a string that contains the image path
    """
    def __init__(self, imgPath):
        if(os.path.exists(imgPath)):
            self._imgPath = imgPath

    """
    Returns the image
    """
    def getImage(self):
        if(self._imgPath != ''):
            return None
        return self._imgPath
