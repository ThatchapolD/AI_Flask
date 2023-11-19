# Bank_note_ID id: 0 = 10Gen11, id: 1 = 100Gen11, 2 = 20Gen11, 3 = 5Gen11, 4 = 500Gen11

from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
from detectron2.data import MetadataCatalog
from detectron2.utils.visualizer import Visualizer, ColorMode
import cv2
test_data = [{'testpic': '/Users/td1932/REfolder/Project/AI_Flask /Python_Srcipt/uploads/image.jpg'}] #input image

cfg = get_cfg()
cfg.merge_from_file('/Users/td1932/REfolder/Project/AI_Flask /Python_Srcipt/Yaml_and_Friend/config.yml')# path for custom config model
cfg.MODEL.WEIGHTS = "/Users/td1932/REfolder/Project/AI_Flask /Python_Srcipt/Yaml_and_Friend/model_final.pth" # path for model
predictor = DefaultPredictor(cfg)
im = cv2.imread(test_data[0]["testpic"])
if im is not None:
    new_width = 640  
    new_height = 640
    resized_image = cv2.resize(im, (new_width, new_height))
    # cv2.imshow('Pre_Image', resized_image)
    # cv2.waitKey(0)
outputs = predictor(resized_image)
v = Visualizer(resized_image[:, :, ::-1],
               metadata=MetadataCatalog.get(cfg.DATASETS.TRAIN[0]),
               scale=0.5,
               instance_mode=ColorMode.IMAGE_BW)
out = v.draw_instance_predictions(outputs["instances"].to("cpu")) 
# img = cv2.cvtColor(out.get_image()[:, :, ::-1], cv2.COLOR_RGBA2RGB)
# Access the class IDs of detected instances
class_ids = outputs["instances"].pred_classes
unique_class_ids = set(class_ids)

# Print class IDs as integers
x = [class_id.item() for class_id in unique_class_ids]
# if x[0] == 2 :
#     print("Bank 20 I sus")
print("IDs of detected instances:", [class_id.item() for class_id in unique_class_ids])# Class_id
# cv2.imshow('Final',img)
# cv2.waitKey(0)
# cv2.destroyAllWindows() 