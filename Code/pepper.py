import cv2
from numpy import uint8
from numpy.typing import NDArray
import numpy as np
from shapely.geometry import Polygon
from matplotlib import pyplot as plt

# make these as functions(3/5+)

# preprocess before dump shit to model or OCR
def commissar(img: NDArray[uint8], sat: int = 0, blur: int = 0) -> NDArray[uint8]:
    
    if sat not in range(-255,256,1): # sat range checker
        raise ValueError("Invalid value for 'sat'. Expected value in range -100 to 100")
    if blur % 2 == 0 and blur != 0:# blur odd number checker
        raise ValueError("Invalid value for 'blur'. Expected odd value or zero(no blur)")
    
    if sat != 0 : # sat control
        img_hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        H, S, V = cv2.split(img_hsv.astype('uint8'))
        S = S.astype(float)
        S = S * (1 + (sat/100))
        S = np.clip(S,0,255)
        S = S.astype('uint8')
        img_hsv = cv2.merge([H,S,V])
        img = cv2.cvtColor(img_hsv.astype('uint8'),cv2.COLOR_HSV2BGR)
        
    if blur != 0 : # blur
        img = cv2.GaussianBlur(img,(blur,blur),0)
    
    return img

    
# get contour/corner for serial number and sig
def appraiser(img: NDArray[uint8]) -> NDArray:
    SAT = 0 # saturation control (-100 - 100) more -> image more vibrant, less -> image becoming grayscale 
    BLUR = 0 # blur control (odd number only) 
    THRESH = 128 # threshold control 
    EPSILON = 0.02 # contour approximation control how much (in decimal-percent) approxmation can deviate from original contour more -> more chaos, min at 0
    
    img = commissar(img,SAT,BLUR)
    img_bw = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, tet = cv2.threshold(img_bw,THRESH,255,cv2.THRESH_BINARY)
    cont, hier = cv2.findContours(tet, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    sorted_cont= sorted(cont, key=cv2.contourArea, reverse= True)
    peri = cv2.arcLength(sorted_cont[0],True)
    approx = cv2.approxPolyDP(sorted_cont[0], EPSILON * peri, True)
    return approx

# check contour validity
def validator(cnt: NDArray,img: NDArray[uint8]) -> bool:
    NOTE_SIZE_PASS = 90 # how big (in percent) the bank notes can be relative to image size
    INTERSECT_SIZE_PASS = 5 # how much the notes detected can deviate from being a rectangle relative to image size (in percent)
    
    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect)
    box = np.intp(box)
    box_area = cv2.contourArea(box)
    img_area = img.shape[0]*img.shape[1]
    cnt_poly = Polygon(np.squeeze(cnt))
    box_poly = Polygon(np.squeeze(box))
    sect_area = cnt_poly.intersection(box_poly).area
    cnt_cent = round((sect_area/img_area)*100,2)
    diff_cent = round(abs(sect_area-box_area)/img_area*100,2)

    return ((cnt_cent <= NOTE_SIZE_PASS) and (diff_cent <= INTERSECT_SIZE_PASS) and cnt.shape[0] == 4),cnt_cent,diff_cent,cnt.shape[0]

# Perspective Warp and save as new Image
def cruxify(img: NDArray[uint8],cnt: NDArray) -> None:
    OUTPUT_WIDTH = 2000 # Output image width after persepective transformation
    OUTPUT_HEIGHT = 1000 # Output image height after persepective transformation
    
    cnt_2d = np.squeeze(cnt)
    cnt_2d = np.array(cnt_2d)
    cnt_2d = cnt_2d[cnt_2d[:,0].argsort()]
    left_cnt,right_cnt = np.split(cnt_2d,2) 
    left_cnt = left_cnt[left_cnt[:,1].argsort()]
    right_cnt = right_cnt[right_cnt[:,1].argsort()]
    srcpt = np.float32([left_cnt[0],right_cnt[0],left_cnt[1],right_cnt[1]])
    dstpt = np.float32([[0,0],[OUTPUT_WIDTH,0],[0,OUTPUT_HEIGHT],[OUTPUT_WIDTH,OUTPUT_HEIGHT]])
    mat = cv2.getPerspectiveTransform(srcpt,dstpt)
    img_show = cv2.warpPerspective(img,mat,(OUTPUT_WIDTH,OUTPUT_HEIGHT))
    
    return img_show
    
def slicer(img: NDArray[uint8], start: tuple, end: tuple)-> NDArray[uint8]:
    IMAGE_WIDTH = 2000
    IMAGE_HEIGHT = 1000
    SECTIONS = 20
    
    width_sec_size = int(IMAGE_WIDTH/SECTIONS)
    height_sec_size = int(IMAGE_HEIGHT/SECTIONS)
    # print(start[0]*width_sec_size)
    # print(end[0]*width_sec_size)
    img_show = img[start[1]*height_sec_size:end[1]*height_sec_size,start[0]*width_sec_size:end[0]*width_sec_size,  :]
    
    return img_show
    
    

def coordinate_dict() -> dict:
    coor_list = {
        "5gen11front" : ((3,2),(8,4),(12,16),(17,19)),
        "10gen11front" : ((3,2),(8,4),(12,16),(17,19)),
        "20gen11front" : ((3,2),(8,4),(12,16),(17,19)),
        "100gen11front" : ((3,2),(8,4),(12,16),(17,19)),
        "500gen11front" : ((3,2),(8,4),(12,16),(17,19))
        }
    return coor_list

def boxer(img: NDArray[uint8])-> NDArray: # get serial number from the bounding box as array of normalized opencv images
    digits = []
    img = commissar(img,-100,0)
    img_bw = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, tet = cv2.threshold(img_bw,80,255,cv2.THRESH_BINARY_INV)
    text = cv2.dilate(tet,np.ones((2,2),np.uint8))
    text = cv2.cvtColor(text,cv2.COLOR_GRAY2BGR)
    box = cv2.dilate(tet,np.ones((3,3),np.uint8))
    box= cv2.morphologyEx(box, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,7)))
    cont, hier = cv2.findContours(box, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cont = sorted(cont, key=lambda c: (cv2.boundingRect(c)[0], cv2.boundingRect(c)[1]))
    for i in cont:
        x,y,w,h = cv2.boundingRect(i)
        if w*h >= 500 and w*h <= 2000 and h <120:
            digit = text[y:(y+h),x:(x+w),:]
            # digit = np.array(digit,dtype=np.float32)
            # digit = digit/255
            digit = cv2.bitwise_not(digit)
            digit = cv2.resize(digit,(64,64)) 
            digits.append(digit) 
    return digits

def boxer_demo(img: NDArray[uint8])-> None:  # create bounding box to check if the bounding box is alright
    digits = []
    img = commissar(img,-100,0)
    img_bw = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, tet = cv2.threshold(img_bw,80,255,cv2.THRESH_BINARY_INV)
    plt.imshow(tet)
    plt.show()    
    text = cv2.dilate(tet,np.ones((2,2),np.uint8))
    text = cv2.cvtColor(text,cv2.COLOR_GRAY2BGR)
    box = cv2.dilate(tet,np.ones((3,3),np.uint8))
    box= cv2.morphologyEx(box, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,7)))
    plt.imshow(box)
    plt.show()
    cont, hier = cv2.findContours(box, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cont = sorted(cont, key=lambda c: (cv2.boundingRect(c)[0], cv2.boundingRect(c)[1]))
    img_show = tet.copy()
    img_show = cv2.cvtColor(img_show,cv2.COLOR_GRAY2BGR)
    for i in cont:
        x,y,w,h = cv2.boundingRect(i)
        if w*h >= 500 and w*h <= 2000 and h <200:
            img_show = cv2.rectangle(img_show,(x,y),(x+w,y+h),(0,0,255),2)
    plt.imshow(img_show)
    plt.show()
    return 0

# get necessary as text/json
    # do this after OCR pattern forms

def helloworld() -> str:
    print("Hello World")

def nihlity(x):
    pass

if __name__ == '__main__':
    helloworld()












