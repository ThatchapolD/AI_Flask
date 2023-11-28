# Bank_note_ID id: 0 = 10Gen11, id: 1 = 100Gen11, 2 = 20Gen11, 3 = 5Gen11, 4 = 500Gen11

import os

# For Image Proc
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
from detectron2.data import MetadataCatalog
from detectron2.utils.visualizer import Visualizer, ColorMode
import cv2

# Flask stuff
from flask import Flask, request, jsonify
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Setting image folder and path
folder_path = '/Users/td1932/REfolder/Project/AI_Flask/uploads'
file_name = 'image.jpg'  # Replace with the name of the file you're checking for

file_path = os.path.join(folder_path, file_name)

# Configure the upload settings
photos = UploadSet("photos", IMAGES)
app.config["UPLOADED_PHOTOS_DEST"] = "uploads/"
configure_uploads(app, photos)

@app.route("/uploadimage", methods=["POST"])
def upload_image():
    if "image" not in request.files:
        return jsonify({"error": "No image file uploaded."}), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({"error": "No selected file."}), 400

    if file and allowed_file(file.filename):
        filename = photos.save(file)
        size = len(file.read())
        # Perform any additional processing, such as saving the file path to a database, if needed
        
        if os.path.isfile(file_path):
            test_data = [{'testpic': file_path}] #input image
            result = get_Prediction(test_data)

            # Send the result back to the app
            # os.remove(file_path)
            return jsonify({"BanknoteID": result},
                           {"Serial_Number": "6969"},
                           {"MF_Sig": "LeeKee1"},
                           {"BOT_Sig": "Leekee2"},
                           {"Price Estimation": "2mil"})

        else:
            print(f"The file '{file_name}' does not exist in the folder.")

        # return jsonify({
        #     "message": "Image uploaded successfully.",
        # })

    return jsonify({"error": "Invalid file type. Only images are allowed."}), 400

def get_Prediction(test_data):
    cfg = get_cfg()
    cfg.merge_from_file('/Users/td1932/REfolder/Project/AI_Flask/Yaml_and_Friend/config.yml')# path for custom config model
    cfg.MODEL.WEIGHTS = "/Users/td1932/REfolder/Project/AI_Flask/Yaml_and_Friend/model_final.pth" # path for model
    predictor = DefaultPredictor(cfg)
    im = cv2.imread(test_data[0]["testpic"])
    if im is not None:
        new_width = 640  
        new_height = 640
        resized_image = cv2.resize(im, (new_width, new_height))
    outputs = predictor(resized_image)
    
    # Access the class IDs of detected instances
    class_ids = outputs["instances"].pred_classes
    unique_class_ids = set(class_ids)

    # Print class IDs as integers
    Banknote_ID = [class_id.item() for class_id in unique_class_ids]
    os.remove(file_path)
    # print("IDs of detected instances:", [class_id.item() for class_id in unique_class_ids])# Class_id

    def case0():
        return "10Gen11"

    def case1():
        return "100Gen11"

    def case2():
        return "20Gen11"
    
    def case3():
        return "5Gen11"
    
    def case4():
        return "500Gen11"

    def default():
        return "Error something's wrong"

    def switch_case(case_value):
        switch_dict = {
            0: case0,
            1: case1,
            2: case2,
            3: case3,
            4: case4
        }

        # Use get() with a default function to handle the default case
        selected_case = switch_dict.get(case_value, default)

        # Call the selected case function
        result = selected_case()
        
        return result

    # print("This is some",Banknote_ID)
    if len(Banknote_ID) == 0:
        return "Can't detect Banknotes"
    result = switch_case(Banknote_ID[0])   
    print(result)

    return result

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {"jpg", "jpeg", "png", "gif"}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=500, debug=True)
