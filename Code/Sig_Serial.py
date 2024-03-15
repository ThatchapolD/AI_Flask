import cv2
from cv2.typing import MatLike
from shapely.geometry import Polygon
import numpy as np
from keras.models import load_model
from ultralytics import YOLO

# HERE, run this and fucks all
# NOTES: if you want to put in numbers( as in 0: '1000gen14back', 1: '1000gen14front' ), uncomment at line 26,27 (type: str is just suggestion, not forced. so changing that is unnecessary.)
def run(img: MatLike,type: str)-> list:
    
    # For fine-tuning the preprocess

    SAT = 0 # saturation control (-100 - 100) more -> image more vibrant, less -> image becoming grayscale 
    BLUR = 0 # blur control (odd number only) 
    THRESH = 128 # threshold control 
    EPSILON = 0.02 # contour approximation control how much (in decimal-percent) approxmation can deviate from original contour more -> more chaos, min at 0
    
    NOTE_SIZE_PASS = 90 # how big (in percent) the bank notes can be relative to image size
    INTERSECT_SIZE_PASS = 5 # how much the notes detected can deviate from being a rectangle relative to image size (in percent)
    
    OUTPUT_WIDTH = 2000 # Output image width after persepective transformation
    OUTPUT_HEIGHT = 1000 # Output image height after persepective transformation
    
    # UNCOMMENT HERE TO CHANGE TO NUMBER SYSTEM
    # class_dict = load_class()
    # type = class_dict[type]
    
    # if it is the back of banknotes this will not bother doing it (check via len(output = 2))
    if 'back' in type:
        return [0,0]
    
    # Cet contours to crop out only banknotes
    img_appraiser = commissar(img,SAT,BLUR)
    img_bw_appraiser = cv2.cvtColor(img_appraiser,cv2.COLOR_BGR2GRAY)
    ret, tet_appraiser = cv2.threshold(img_bw_appraiser,THRESH,255,cv2.THRESH_BINARY)
    cont_appraiser, hier = cv2.findContours(tet_appraiser, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    sorted_cont= sorted(cont_appraiser, key=cv2.contourArea, reverse= True)
    peri = cv2.arcLength(sorted_cont[0],True)
    approx = cv2.approxPolyDP(sorted_cont[0], EPSILON * peri, True)

    # Check if contour is suitable or not
    rect = cv2.minAreaRect(approx)
    box_legit = cv2.boxPoints(rect)
    box_legit = np.intp(box_legit)
    box_area = cv2.contourArea(box_legit)
    img_area = img.shape[0]*img.shape[1]
    cnt_poly = Polygon(np.squeeze(approx))
    box_poly = Polygon(np.squeeze(box_legit))
    sect_area = cnt_poly.intersection(box_poly).area
    cnt_cent = round((sect_area/img_area)*100,2)
    diff_cent = round(abs(sect_area-box_area)/img_area*100,2)
    legit = ((cnt_cent <= NOTE_SIZE_PASS) and (diff_cent <= INTERSECT_SIZE_PASS) and approx.shape[0] == 4)
    
    # if it is not suitable, stop (return output with length of 1 to differentiate between backside and error)
    if legit == False:
        return [0]
    
    # Perspective Warping
    cnt_2d = np.squeeze(approx)
    cnt_2d = np.array(cnt_2d)
    cnt_2d = cnt_2d[cnt_2d[:,0].argsort()]
    left_cnt,right_cnt = np.split(cnt_2d,2) 
    left_cnt = left_cnt[left_cnt[:,1].argsort()]
    right_cnt = right_cnt[right_cnt[:,1].argsort()]
    srcpt = np.float32([left_cnt[0],right_cnt[0],left_cnt[1],right_cnt[1]])
    dstpt = np.float32([[0,0],[OUTPUT_WIDTH,0],[0,OUTPUT_HEIGHT],[OUTPUT_WIDTH,OUTPUT_HEIGHT]])
    mat = cv2.getPerspectiveTransform(srcpt,dstpt)
    img_show = cv2.warpPerspective(img,mat,(OUTPUT_WIDTH,OUTPUT_HEIGHT))
    
    # Load Coordinate of Serial Number for Each Classes
    coor_dict = load_coor()
    start = coor_dict[type][0] 
    end = coor_dict[type][1]
    
    # Section out the serial number
    img_show = img_show[start[1]:end[1], start[0]:end[0], :]
    
    # Create Bounding box and export out the digits
    digits = []
    img_boxer = commissar(img_show,-100,0)
    img_bw_boxer = cv2.cvtColor(img_boxer,cv2.COLOR_BGR2GRAY)
    ret, tet_boxer = cv2.threshold(img_bw_boxer,80,255,cv2.THRESH_BINARY_INV)
    text = cv2.dilate(tet_boxer,np.ones((2,2),np.uint8))
    text = cv2.cvtColor(text,cv2.COLOR_GRAY2BGR)
    box_boxer = cv2.dilate(tet_boxer,np.ones((3,3),np.uint8))
    box_boxer = cv2.morphologyEx(box_boxer, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,7)))
    cont_boxer, hier = cv2.findContours(box_boxer, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cont_boxer = sorted(cont_boxer, key=lambda c: (cv2.boundingRect(c)[0], cv2.boundingRect(c)[1]))
    for i in cont_boxer:
        x,y,w,h = cv2.boundingRect(i)
        if w*h >= 500 and w*h <= 2000 and h <120:
            digit = text[y:(y+h),x:(x+w),:]
            # digit = np.array(digit,dtype=np.float32)
            # digit = digit/255
            digit = cv2.bitwise_not(digit)
            digit = cv2.resize(digit,(64,64)) 
            digits.append(digit)

    # Load OCR model and decode table
    ocr_model = load_model("../OCR_Model/model.h5")
    alpha_eng = load_alpha()
    
    # OCR
    digits = np.array(digits, dtype=np.float32)
    digits = digits/255
    preds = ocr_model.predict(digits)
    out = np.argmax(preds, axis=1)
    replace_func_vec = np.vectorize(replace_func)
    decoded_out = replace_func_vec(out,alpha_eng)
    
    # OUTPUT 1 : SERIAL NUMBER
    sn = ''.join(decoded_out)
    
    sig_model = YOLO('../OCR_Model/best.pt')
    results = sig_model.predict(img,imgsz = 640,conf = 0.5,iou = 0.5)
    names = sig_model.names
    res = []
    for r in results:
        for c in r.boxes.cls:
            res.append(names[int(c)])
    
    # Bad detection catch
    if len(res) != 2:
       return [0]
    
    #load name and shit 
    FIN_list,BOT_list,fullname_fin,fullname_bot = name_enclo()
       
    res0Fin = res[0] in FIN_list
    res0Bot = res[0] in BOT_list
    res1Fin = res[1] in FIN_list
    res1Bot = res[1] in BOT_list

    #normal case
    if(res0Fin != res0Bot and res1Fin != res1Bot):
        if res0Fin:
            outfin = fullname_fin[res[0]]
            outbot = fullname_bot[res[1]]
        elif res1Fin:
            outfin = fullname_fin[res[1]]
            outbot = fullname_bot[res[0]]
    elif(res0Fin == res0Bot and res1Fin != res1Bot):
        if res1Fin:
            outfin = fullname_fin[res[1]]
            outbot = fullname_bot[res[0]]
        else:
            outfin = fullname_fin[res[0]]
            outbot = fullname_bot[res[1]]
    elif(res1Fin == res1Bot and res0Fin != res0Bot):
        if res0Fin:
            outfin = fullname_fin[res[0]]
            outbot = fullname_bot[res[1]]
        else:
            outfin = fullname_fin[res[1]]
            outbot = fullname_bot[res[0]]
    else: 
        return [0] # bad detection catch
    
    # OUTPUT 2-5 signature
    fin_en = outfin[0] 
    fin_th = outfin[1]
    bot_en = outbot[0]
    bot_th = outbot[1]
    
    return [sn,fin_en,fin_th,bot_en,bot_th]

# ===================================== END ==============================================
    
def commissar(img: MatLike, sat: int = 0, blur: int = 0) -> MatLike:
    
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

def load_class() -> dict[int:str]:
    dict = {
    0: '1000gen14back', 1: '1000gen14front', 2: '1000gen15back', 3: '1000gen15front', 
    4: '1000gen16back', 5: '1000gen16front', 6: '1000gen17back', 7: '1000gen17front', 
    8: '100gen11back', 9: '100gen11front', 10: '100gen12back', 11: '100gen12front', 
    12: '100gen14back', 13: '100gen14front', 14: '100gen15back', 15: '100gen15front', 
    16: '100gen16back', 17: '100gen16front', 18: '100gen17back', 19: '100gen17front', 
    20: '10gen11back', 21: '10gen11front', 22: '10gen12back', 23: '10gen12front', 
    24: '20gen11back', 25: '20gen11front', 26: '20gen12back', 27: '20gen12front', 
    28: '20gen15back', 29: '20gen15front', 30: '20gen16back', 31: '20gen16front', 
    32: '20gen17back', 33: '20gen17front', 34: '500gen11back', 35: '500gen11front', 
    36: '500gen13back', 37: '500gen13front', 38: '500gen14back', 39: '500gen14front', 
    40: '500gen15back', 41: '500gen15front', 42: '500gen16back', 43: '500gen16front', 
    44: '500gen17back', 45: '500gen17front', 46: '50gen13back', 47: '50gen13front', 
    48: '50gen15back', 49: '50gen15front', 50: '50gen16back', 51: '50gen16front', 
    52: '50gen17back', 53: '50gen17front', 54: '5gen11back', 55: '5gen11front', 
    56: 'memo_2530back', 57: 'memo_2530front', 58: 'memo_2539_50back', 
    59: 'memo_2539_50front', 60: 'memo_2547back', 61: 'memo_2547front', 
    62: 'memo_2549back', 63: 'memo_2549front', 64: 'memo_2550back', 
    65: 'memo_2550front', 66: 'memo_2553back', 67: 'memo_2554back', 
    68: 'memo_2554front', 69: 'memo_2555_100back', 70: 'memo_2555_80back', 
    71: 'memo_2555_80front', 72: 'memo_2558back', 73: 'memo_2559_500back', 
    74: 'memo_2559_70back', 75: 'memo_2559_70front', 76: 'memo_2562_1000back', 
    77: 'memo_2562_1000front', 78: 'memo_2562_100back', 79: 'memo_2562_100front'
    }
    
    return dict 

def load_coor() -> dict[str:list[tuple[int,int]]]:
    dict = {
    '1000gen14front': ((1521,844),(1932,949)),
    '1000gen15front': ((1560,653),(1963,820)),
    '1000gen16front': ((1221,821),(1646,951)),
    '1000gen17front': ((1860,203),(1954,760)),
    '100gen11front': ((279,105),(809,197)),
    '100gen12front': ((413,93),(1014,250)),
    '100gen14front': ((1521,844),(1932,949)),
    '100gen15front': ((1560,653),(1963,820)),
    '100gen16front': ((1221,821),(1646,951)),
    '100gen17front': ((1860,203),(1954,760)),
    '10gen11front': ((279,105),(809,197)),
    '10gen12front': ((413,93),(1014,250)),
    '20gen11front': ((279,105),(809,197)),
    '20gen12front': ((413,93),(1014,250)),
    '20gen15front': ((1560,653),(1963,820)),
    '20gen16front': ((1395,805),(1942,972)),
    '20gen17front': ((1860,203),(1954,760)),
    '500gen11front': ((279,105),(809,197)),
    '500gen13front': ((364,198),(994,74)),
    '500gen14front': ((1521,844),(1932,949)),
    '500gen15front': ((1560,653),(1963,820)),
    '500gen16front': ((1221,821),(1646,951)),
    '500gen17front': ((1860,203),(1954,760)),
    '50gen13front': ((364,198),(994,74)),
    '50gen15front': ((1560,653),(1963,820)),
    '50gen16front': ((1395,805),(1942,972)),
    '50gen17front': ((1860,203),(1954,760)),
    '5gen11front': ((279,105),(809,197)),
    
    'memo_2530front': ((100,100),(100,100)),
    'memo_2539_50front': ((100,100),(100,100)),
    'memo_2547front': ((100,100),(100,100)),
    'memo_2549front': ((100,100),(100,100)),
    'memo_2550front': ((100,100),(100,100)),
    'memo_2554front': ((100,100),(100,100)),
    'memo_2555_80front': ((100,100),(100,100)),
    'memo_2559_70front': ((100,100),(100,100)),
    'memo_2562_1000front': ((100,100),(100,100)),
    'memo_2562_100front': ((100,100),(100,100))
    }
    return dict
    
def load_alpha() -> dict:
    dict = {
    0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9',
    10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F', 16: 'G', 17: 'H', 18: 'I', 19: 'J',
    20: 'K', 21: 'L', 22: 'M', 23: 'N', 24: 'O', 25: 'P', 26: 'Q', 27: 'R', 28: 'S', 29: 'T',
    30: 'U', 31: 'V', 32: 'W', 33: 'X', 34: 'Y', 35: 'Z'}
    return dict
    
def replace_func(value,dicto):
    return dicto.get(value, 'UNKNOWN')

def name_enclo() -> tuple[list,list,dict,dict]:
    FIN_list = ['SermV','BoonmaW','BoonchuR','SavetrP','SupatS','KriengsakC','SommaiH','PramualS','VeerapongR','BanharnS','SutheeS','PanatS','SurakietS','BodeeJ','ChaiwatW','AmnuayV','KositP','TarrinN','SomkidJ','SuchatJ','ThanongB','PridiyathornD','Chalongphob','SurapongS','SuchartT','KornC','ThirachaiP','SommaiP','KittirattN','ApisakT','UttamaS','PreedeeD','ArkhomT','SretthaT']
    BOT_list = ['PueyU','BisudhiN','SnohU','NukulP','KamchornS','ChavalitT','VijitS','RerngchaiM','ChaiwatW','ChatumongolS','PridiyathornD','TarisaW','PrasarnT','VeerathaiS','SethaputS']

    fullname_fin = {'SermV': ['Mr. Serm Vinitchaikun','นายเสริม วินิจฉัยกุล'],
                    'BoonmaW': ['Mr. Boonma Wongsawan','นายบุญมา วงศ์สวรรค์'],
                    'BoonchuR': ['Mr.Boonchu Rojanasathien','นายบุญชู โรจนเสถียร'],
                    'SavetrP': ['Mr.Savetr Piempongsan','นายเสวตร เปี่ยมพงศ์สานต์'],
                    'SupatS': ['Mr.Supat Suthatham','นายสุพัฒน์ สุธาธรรม'],
                    'KriengsakC': ['Mr. Sommai Huntakul','พลเอก เกรียงศักดิ์ ชมะนันทน์'],
                    'SommaiH': ['Mr. Sommai Huntakul','นายสมหมาย ฮุนตระกูล'],
                    'PramualS': ['Mr.Pramual Sapavasu','นายประมวล สภาวสุ'],
                    'VeerapongR': ['Mr.Veerapong Ramangkul','นายวีรพงษ์ รามางกูร'],
                    'BanharnS': ['Mr. Banharn Silpa-Archa','นายบรรหาร ศิลปอาชา'],
                    'SutheeS': ['Mr. Suthee Singsane','นายสุธี สิงห์เสน่ห์'],
                    'PanatS': ['Mr.Panat Simasathien','นายพนัส สิมะเสถียร'],
                    'SurakietS': ['Dr. Surakiet Sathienthai','นายสุรเกียรติ์ เสถียรไทย'],
                    'BodeeJ': ['Mr. Bodee Junnanon','นายบดี จุณณานนท์'],
                    'ChaiwatW': ['Mr. Chaiwat Wiboonsawat','นายชัยวัฒน์ วิบูลย์สวัสดิ์'],
                    'AmnuayV': ['Dr. Amnuay Veeravan','นายอำนวย วีรวรรณ'],
                    'KositP': ['Mr. Kosit Panpiemras','นายโฆษิต ปั้นเปี่ยมรัษฎ์'],
                    'TarrinN': ['Mr. Tarrin Nimmanahaeminda','นายธารินทร์ นิมมานเหมินท์'],
                    'SomkidJ': ['Dr. Somkid Jatusripitak','นายสมคิด จาตุศรีพิทักษ์'],
                    'SuchatJ': ['Captain Suchat Jaovisidha','ร้อยเอกสุชาติ เชาว์วิศิษฐ'],
                    'ThanongB': ['Dr. Thanong Bidaya','นายทนง พิทยะ'],
                    'PridiyathornD': ['M.R. Pridiyathorn Devakula','หม่อมราชวงศ์ปรีดิยาธร เทวกุล'],
                    'Chalongphob': ['Dr. Chalongphob Sussangkarn','นายฉลองภพ สุสังกร์กาญจน์'],
                    'SurapongS': ['Mr. Surapong Suebwonglee','นายสุรพงษ์ สืบวงศ์ลี'],
                    'SuchartT': ['Mr. Suchart Thada-Thamrongvech','นายสุชาติ ธาดาธำรงเวช'],
                    'KornC': ['Mr. Korn Chatikavanij','นายกรณ์ จาติกวณิช'],
                    'ThirachaiP': ['Mr. Thirachai Phuvanatnaranubala','นายธีระชัย ภูวนาถนรานุบาล'],
                    'SommaiP': ['Mr. Sommai Phasee','นายสมหมาย ภาษี'],
                    'KittirattN': ['Mr. Kittiratt Na-Ranong','นายกิตติรัตน์ ณ ระนอง'],
                    'ApisakT': ['Mr. Apisak Tantivorawong','นายอภิศักดิ์ ตันติวรวงศ์'],
                    'UttamaS': ['Mr.Uttama Savanayana','นายอุตตม สาวนายน'],
                    'PreedeeD': ['Mr.Preedee Daochai','นายปรีดี ดาวฉาย'],
                    'ArkhomT': ['Mr.Arkhom Termpittayapaisith','นายอาคม เติมพิทยาไพสิฐ'],
                    'SretthaT': ['Mr. Srettha Thawisin','นาย เศรษฐา ทวีสิน']}
    
    fullname_bot = {'PueyU': ['Dr. Puey Ungphakorn','นายป๋วย อึ๊งภากรณ์'],
                    'BisudhiN': ['Mr. Bisudhi Nimmanhaemin','นายพิสุทธิ์ นิมมานเหมินท์'],
                    'SnohU': ['Mr. Snoh Unakul','นายเสนาะ อูนากูล'],
                    'NukulP': ['Mr. Nukul Prachuabmoh','นายนุกูล ประจวบเหมาะ'],
                    'KamchornS': ['Mr. Kamchorn Sathirakul','นายกำจร สถิรกุล'],
                    'ChavalitT': ['Mr. Chavalit Thanachanan','นายชวลิต ธนะชานันท์'],
                    'VijitS': ['Mr. Vijit Supinit','นายวิจิตร สุพินิจ'],
                    'RerngchaiM': ['Mr. Rerngchai Marakanond','นายเริงชัย มะระกานนท์'],
                    'ChaiwatW': ['Mr. Chaiyawat Wibulswasdi','นายชัยวัฒน์ วิบูลย์สวัสดิ์'],
                    'ChatumongolS': ['M.R.Chatu Mongol Sonakul','หม่อมราชวงศ์จัตุมงคล โสณกุล'],
                    'PridiyathornD': ['M.R. Pridiyathorn Devakula','หม่อมราชวงศ์ปรีดิยาธร เทวกุล'],
                    'TarisaW': ['Dr. Tarisa Watanagase','นางธาริษา วัฒนเกส'],
                    'PrasarnT': ['Mr. Prasarn Trairatvorakul','นายประสาร ไตรรัตน์วรกุล'],
                    'VeerathaiS': ['Mr.Veerathai Santiprabhob','นายวิรไท สันติประภพ'],
                    'SethaputS': ['Mr. Sethaput Suthiwartnarueput','นายเศรษฐพุฒิ สุทธิวาทนฤพุฒิ']}
    return FIN_list,BOT_list,fullname_fin,fullname_bot   

if __name__ == '__main__':
    img = cv2.imread('../Test_Picture/5Sat.png')
    listo = run(img,'5gen11front')
    print(listo)
