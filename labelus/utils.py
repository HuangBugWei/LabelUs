import cv2
import numpy as np
from PIL import Image
import pycocotools.mask

def floodFill(source, mask, seedPoint, newVal, loDiff, upDiff, flags=cv2.FLOODFILL_FIXED_RANGE):
    result = source.copy()
    mmask = mask.copy()
    cv2.floodFill(result, mmask, seedPoint=seedPoint, newVal=newVal, loDiff=loDiff, upDiff=upDiff, flags=flags)
    return result

def creatMask(image: np.array) -> np.array:
    '''
    image: (h, w, c)
    return label: (h, w, 1)
    0 is black
    255 is white
    '''
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    # mask = 255 - mask
    channelFirst = np.transpose(image, (2, 0, 1))
    threshold = 180
    first = channelFirst[0] < threshold
    second = channelFirst[1] < threshold
    third = channelFirst[2] < threshold
    # get position which [r, g, b] = [255, 255, 255]
    logit = np.logical_and(np.logical_and(first, second), third)
    mask[logit] = 255
    def pad_with(vector, pad_width, iaxis, kwargs):
        pad_value = kwargs.get('padder', 10)
        vector[:pad_width[0]] = pad_value
        vector[-pad_width[1]:] = pad_value
    
    mmask = np.pad(mask, 1, pad_with, padder=0, dtype=np.uint8)
    return mmask

def dilate(input: np.array, width: int = 1) -> np.array:
    """
    this function will expand white(255) on image with specified width
    """
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    mask_dilated = cv2.dilate(input, kernel, iterations=6)
    return mask_dilated

def storeRLE(input: np.array) -> dict:
    """
    we want white part in input
    so we call bool_mask = input > 0 to get the part which is not equal to 0 (black)
    if input have 3 channels, then return will be list(dict)
    thus we get the first one.
    """
    bool_mask = input > 0
    rle_encoding_mask = pycocotools.mask.encode(np.asfortranarray(bool_mask))
    if type(rle_encoding_mask) == list:
        return rle_encoding_mask[0]
    else:
        return rle_encoding_mask
def decodeRLE(input):
    return pycocotools.mask.decode(input)

def storeImage(input: np.array):
    Image.fromarray(input).save("store.png")

def getContours(input: np.array):
    gray = cv2.cvtColor(input, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 127, 255, 0)
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # concat shape is (n, 1, 2), n points, 2 stands for x, y
    concat = np.concatenate([contour for contour in contours], axis = 0)
    nonsortXY = np.transpose(concat, (2, 0, 1)).reshape(2, -1)

    sortedX, sortedY = sortXY(nonsortXY[0], nonsortXY[1])
    sortedXY = (np.stack((sortedX, sortedY))).transpose().reshape(-1, 1, 2)
    hull = cv2.convexHull(sortedXY)
    return hull


def sortXY(x, y):
    # ref: https://stackoverflow.com/a/58874392
    # sort xy into counter-clockwise order
    x0 = np.mean(x)
    y0 = np.mean(y)

    r = np.sqrt((x-x0)**2 + (y-y0)**2)

    angles = np.where((y-y0) > 0, np.arccos((x-x0)/r), 2*np.pi-np.arccos((x-x0)/r))

    mask = np.argsort(angles)

    x_sorted = x[mask]
    y_sorted = y[mask]

    return x_sorted, y_sorted

if __name__ == '__main__':
    img = cv2.imread("sample2.png")
