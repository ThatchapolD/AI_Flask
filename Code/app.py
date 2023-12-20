# Bank_note_ID id: 0 = 10Gen11, id: 1 = 100Gen11, 2 = 20Gen11, 3 = 5Gen11, 4 = 500Gen11

# For modifying file
import os
import shutil

# For Image Proc
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
import cv2

# Flask stuff
from flask import Flask, request, jsonify, session
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_cors import CORS
import uuid

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secret_key_for_session'

# Setting image folder and path
base_folder_path = '/home/tdubuntu/Desktop/AI_Flask/uploads'
app.config["UPLOADED_PHOTOS_DEST"] = base_folder_path
photos = UploadSet("photos", IMAGES)
configure_uploads(app, photos)

@app.route("/test")
def hello_world():
    return "Test 123"

@app.route("/uploadimage", methods=["POST"])
def upload_image():
    if "image" not in request.files:
        return jsonify({"error": "No image file uploaded."}), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({"error": "No selected file."}), 400

    if file and allowed_file(file.filename):
        session['user_id'] = str(uuid.uuid4())

        folder_path = os.path.join(base_folder_path, session['user_id'])
        os.makedirs(folder_path, exist_ok=True)

        file_path = os.path.join(folder_path, file.filename)
        filename = photos.save(file, folder=session['user_id'])
        size = len(file.read())
        
        if os.path.isfile(file_path):
            test_data = [{'testpic': file_path}] #input image
            result = get_Prediction(test_data, file_path)

            remove_user_folder(session['user_id'])
            # Send the result back to the app
            return jsonify({"BanknoteID": result},
                           {"Serial_Number": "TBA"},
                           {"MF_Sig": "TBA"},
                           {"BOT_Sig": "TBA"},)

        else:
            print(f"The file '{file.filename}' does not exist in the folder.")

    return jsonify({"error": "Invalid file type. Only images are allowed."}), 400

def get_Prediction(test_data, file_path):
    cfg = get_cfg()
    cfg.merge_from_file('/home/tdubuntu/Desktop/AI_Flask/Yaml_and_Friend/config.yml')# path for custom config model
    cfg.MODEL.WEIGHTS = "/home/tdubuntu/Desktop/AI_Flask/Yaml_and_Friend/model_final.pth" # path for model
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

def remove_user_folder(user_id):
    folder_path = os.path.join(base_folder_path, user_id)
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    else:
        print(f"The folder for user {user_id} does not exist.")

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {"jpg", "jpeg", "png", "gif"}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6000)
