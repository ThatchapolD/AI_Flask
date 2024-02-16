from numpy.typing import NDArray
from keras.models import load_model
import os
import cv2
import numpy as np
from matplotlib import pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import shuffle
from keras.models import Sequential
from keras.layers import Conv2D, Flatten, MaxPooling2D, Dense

def replace_func(value,dicto):
    return dicto.get(value, 'UNKNOWN')

def load_alphabets() -> dict:
  class_mapping = {
  0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9',
  10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F', 16: 'G', 17: 'H', 18: 'I', 19: 'J',
  20: 'K', 21: 'L', 22: 'M', 23: 'N', 24: 'O', 25: 'P', 26: 'Q', 27: 'R', 28: 'S', 29: 'T',
  30: 'U', 31: 'V', 32: 'W', 33: 'X', 34: 'Y', 35: 'Z'}
  class_mapping_thai = {}
  return class_mapping,class_mapping_thai

def ocr(x: NDArray)-> str:
    loaded_model = load_model("../OCR_Model/model.h5")
    alpha_eng,alpha_thai = load_alphabets()
    x = np.array(x, dtype=np.float32)
    x = x/255
    preds = loaded_model.predict(x)
    out = np.argmax(preds, axis=1)
    replace_func_vec = np.vectorize(replace_func)
    decoded_out = replace_func_vec(out,alpha_eng)
    true_out = ''.join(decoded_out)
    print(true_out)

    return true_out

if __name__ == '__main__':
  ocr(1) 