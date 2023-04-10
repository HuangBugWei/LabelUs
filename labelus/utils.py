import cv2
import numpy as np
from PIL import Image
import pycocotools.mask

def floodFill(source, mask, seedPoint, newVal, loDiff, upDiff, flags=cv2.FLOODFILL_FIXED_RANGE):
    result = source.copy()
    cv2.floodFill(result, mask=mask, seedPoint=seedPoint, newVal=newVal, loDiff=loDiff, upDiff=upDiff, flags=flags)
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

def dilate(input: np.array, width: int = 2) -> np.array:
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

if __name__ == '__main__':
    img = cv2.imread("sample2.png")
