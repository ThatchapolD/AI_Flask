"""
THIS IS THE EXAMPLE CODE OF WHAT I ENVISION THE MODEL TO BE
"""

import cv2
import numpy as np
from pepper import *
from salt import *
from matplotlib import pyplot as plt
 
class Serial_Sig:
    def __init__(self, img):
        self.input_img = img # image input(same as going to ai model) get this from your app or some shit idc.
        self.input_img = cv2.imread(self.input_img)
        self.img_amped = commissar(self.input_img,100,0) # boost image for saturation boost idea before put in the model.
        
    def Serial_Num(self, class_name):        
        dict = coordinate_dict() # import dictionary of serial number coordinate for each class
        
        cont = appraiser(self.input_img) # get contour of image
        cont_cond,note,diff,corner = validator(cont,self.input_img) # validify contour if this is a good contour or not
        
        if cont_cond == False:
            print('Bad Contour. please try taking the picture again. NOTE SIZE : ' + str(note) + '| CONTOUR DIFF : ' + str(diff) + '| CORNERS : ' + str(corner))
            quit()
        else:
            pass
        
        img_cruxed = cruxify(self.input_img,cont)
        cv2.imwrite('../Test_Picture/100Baht_Crux.jpg',img_cruxed)
        sn = slicer(img_cruxed,dict[class_name][0],dict[class_name][1]) 
        sn_img = boxer(sn)
    
        Serial_Resutl = ocr(sn_img)
        
        return Serial_Resutl
        