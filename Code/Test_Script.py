from ultralytics import YOLO
from class_Mapper import ClassMapper

model = YOLO("/home/tdubuntu/Desktop/AI_Flask/YoloV8_Model/AI_Model_YoloV8.pt")  #model
results = model('/home/tdubuntu/Desktop/AI_Flask/Yaml_and_Friend/IMG_2565.jpg')  #input from app

result = results[0]

if len(result.boxes) == 0:
    print("Can't detect Banknotes")

else: 

    box = result.boxes[0]
    class_id = box.cls[0].item()
    # print("Class Item: ", round(class_id))

    #Calling class_mapper class to sort the id into name
    class_mapper = ClassMapper()
    mapped_result = class_mapper.map_classes(round(class_id))
    print("The Result: ", mapped_result)

# len(result.boxes)
# cords = box.xyxy[0].tolist()
# conf = box.conf[0].item()
# cords = box.xyxy[0].tolist()
# cords = [round(x) for x in cords]
# class_id = result.names[box.cls[0].item()]# output to app 
# conf = round(box.conf[0].item(), 2)
# print("Object type:", class_id)
