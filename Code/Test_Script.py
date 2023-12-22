from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
import cv2
from class_Mapper import ClassMapper

test_data = [{'testpic':"/home/tdubuntu/Desktop/AI_Flask/Yaml_and_Friend/IMG_2566.jpg"}]#input

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
class_ids = outputs["instances"].pred_classes

#Calling class_mapper class to sort the id into name
class_mapper = ClassMapper()

mapped_result = class_mapper.map_classes(class_ids)
print(mapped_result)
