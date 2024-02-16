# For modifying file
import os
import shutil

# For Image Proc
import torch 
from ultralytics import YOLO
from class_Mapper import ClassMapper

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
            # test_data = [{'testpic': file_path}] #input image
            # torch.no_grad()
            result = get_Prediction(file_path)

            print(result)
            remove_user_folder(session['user_id'])
            # torch.cuda.empty_cache()
            # Send the result back to the app
            return jsonify({"BanknoteID": result},
                           {"Serial_Number": "TBA"},
                           {"MF_Sig": "TBA"},
                           {"BOT_Sig": "TBA"},)

        else:
            print(f"The file '{file.filename}' does not exist in the folder.")

    return jsonify({"error": "Invalid file type. Only images are allowed."}), 400

def get_Prediction(file_path):
    model = YOLO("/home/tdubuntu/Desktop/AI_Flask/YoloV8_Model/AI_Model_YoloV8.pt")  #model
    results = model(file_path)  #input from app

    result = results[0]

    if len(result.boxes) == 0:
        #Removed file after image processing is comeplete
        os.remove(file_path)
        
        return "Can't detect Banknotes"

    else: 
        box = result.boxes[0]
        class_id = box.cls[0].item()
        # print("Class Item: ", round(class_id))

        #Calling class_mapper class to sort the id into name
        class_mapper = ClassMapper()
        mapped_result = class_mapper.map_classes(round(class_id))
        # print("The Result: ", mapped_result)
        
        #Removed file after image processing is comeplete
        os.remove(file_path)
        
        return mapped_result


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
