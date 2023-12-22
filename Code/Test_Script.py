from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
from detectron2.data import MetadataCatalog
from detectron2.utils.visualizer import Visualizer, ColorMode
import matplotlib.pyplot as plt
import cv2

test_data = [{'testpic':"/home/tdubuntu/Desktop/AI_Flask/Yaml_and_Friend/IMG_2433.jpg"}]#input

cfg = get_cfg()
cfg.merge_from_file("/home/tdubuntu/Desktop/AI_Flask/Yaml_and_Friend/config_finetune.yml")
cfg.MODEL.WEIGHTS = "/home/tdubuntu/Desktop/AI_Flask/Yaml_and_Friend/model_finetune.pth"
predictor = DefaultPredictor(cfg)

im = cv2.imread(test_data[0]["testpic"])
if im is not None:
    new_width = 640
    new_height = 640
    resized_image = cv2.resize(im, (new_width, new_height))

outputs = predictor(resized_image)

# Mapping class IDs to custom labels
class_mapping = {
    0:"5gen11",
    1:"5gen11",
    2:"10gen11",
    3:"10gen11",
    4:"20gen11",
    5:"20gen11",
    6:"100gen11",
    7:"100gen11",
    8:"500gen11",
    9:"500gen11",
    10:"10gen12",
    11:"10gen12",
    12:"20gen12",
    13:"20gen12",
    14:"100gen12",
    15:"100gen12",
    16:"50gen13",
    17:"50gen13",
    18:"500gen13",
    19:"500gen13",
    20:"100gen14",
    21:"100gen14",
    22:"500gen14",
    23:"500gen14",
    24:"1000gen14",
    25:"1000gen14",
    26:"20gen15",
    27:"20gen15",
    28:"50gen15",
    29:"50gen15",
    30:"100gen15",
    31:"100gen15",
    32:"500gen15",
    33:"500gen15",
    34:"1000gen15",
    35:"1000gen15",
    36:"20gen16",
    37:"20gen16",
    38:"50gen16",
    39:"50gen16",
    40:"100gen16",
    41:"100gen16",
    42:"500gen16",
    43:"500gen16",
    44:"1000gen16",
    45:"1000gen16",
    46:"20gen17",
    47:"20gen17",
    48:"50gen17",
    49:"50gen17",
    50:"100gen17",
    51:"100gen17",
    52:"500gen17",
    53:"500gen17",
    54:"1000gen17",
    55:"1000gen17",
    56:"memo1987",
    57:"memo1987",
    58:"memo1990",
    59:"memo1992",
    60:"memo1992",
    61:"memo1992",
    62:"memo1995",
    63:"memo1995",
    64:"memo1996",
    65:"memo1996",
    66:"memo1999",
    67:"memo1999",
    68:"memo2000",
    69:"memo2000",
    70:"memo2004",
    71:"memo2004",
    72:"memo2006",
    73:"memo2006",
    74:"memo2007",
    75:"memo2007",
    76:"memo2010",
    77:"memo2010",
    78:"memo2011",
    79:"memo2011",
    80:"memo2012.10",
    81:"memo2012.10",
    82:"memo2012.kq",
    83:"memo2012.kq",
    84:"memo2015",
    85:"memo2015",
    86:"memo2016.k",
    87:"memo2016.k",
    88:"memo2016.q",
    89:"memo2016.q",
    90:"memo2017",
    91:"memo2017",
    92:"memo2019",
    93:"memo2019"
}

class_ids = outputs["instances"].pred_classes

# Modify class IDs based on mapping
mapped_class_ids = [class_mapping.get(class_id.item(), class_id.item()) for class_id in class_ids]
mapped_result = mapped_class_ids[0] if mapped_class_ids else None

print("Mapped result =", mapped_result)
