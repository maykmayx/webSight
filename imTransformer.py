from scipy.misc import imread, imsave
import numpy as np

MAX_INTENSITY = 255


def process(image_path):
    """
    Performs basic manipulation (color inverse) on the image in the image_path.
    Notice: the image in the given path will be changed!
    :param image_path: path to the image file (of any well-known format).
                       Assumes the path is correct and has the image file already.
    :return: nothing.
    """
    # read the image and normalize it for values in [0,1]:
    print(image_path)
    image = (imread(image_path).astype(np.float32))/MAX_INTENSITY
    # get the inverted intensities and convert back to original value-scales:
    inverted = (np.ones(image.shape) - image)*MAX_INTENSITY
    imsave(image_path, inverted)
    return