"""
THIS IS THE EXAMPLE CODE OF WHAT I ENVISION THE MODEL TO BE
"""

import cv2
import numpy as np
from pepper import *
from salt import *
from matplotlib import pyplot as plt

if __name__ == "__main__":
    input_img = '../Test_Picture/IMG_2433.jpg' # image input(same as going to ai model) get this from your app or some shit idc.
    input_img = cv2.imread(input_img)
    img_amped = commissar(input_img,100,0) # boost image for saturation boost idea before put in the model.
    
    #model(img_amped):       # mock up of model the idea is that it return the predicted class back 
    #    return(class_name)
     
    class_name = '10gen11front' # what class is detected from faster r-cnn
    
    dict = coordinate_dict() # import dictionary of serial number coordinate for each class
    
    cont = appraiser(input_img) # get contour of image
    cont_cond,note,diff,corner = validator(cont,input_img) # validify contour if this is a good contour or not
    
    if cont_cond == False:
        print('Bad Contour. please try taking the picture again. NOTE SIZE : ' + str(note) + '| CONTOUR DIFF : ' + str(diff) + '| CORNERS : ' + str(corner))
        quit()
    else:
        pass
    
    img_cruxed = cruxify(input_img,cont)
    
    cv2.imwrite('../Test_Picture/100Baht_Crux.jpg',img_cruxed)
    
    # plt.imshow(img_cruxed)
    # plt.show()
    
    sn = slicer(img_cruxed,dict[class_name][0],dict[class_name][1]) 
    # boxer_demo(sn)
    sn_img = boxer(sn)
    
    # for shit in sn_img:
    #     cv2.imshow('test',shit)
    #     cv2.waitKey(0)
        
    ocr(sn_img)
    
    # cv2.destroyAllWindows()

    

    
    