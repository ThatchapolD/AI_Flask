# This is the merge of Faster-RCNN and Flask with the result becoming RESTAPI

## Follow this step to create venv and download model.pth
**The python version needs in this code is <=3.9**  

1. create a venv or virtual env python3.9<= for this project by any tools  
2. ```git clone https://github.com/facebookresearch/detectron2.git``` 
3. ```pip install torch torchvision tornado```   
4. ```python -m pip install -e detectron2``` 
   python -m pip install -e detectron2 ?? Not working for mac ? can't find module name torch  
   Run this instead: ```python detectron2/setup.py build develop```  
5. Download a model.pth from this [Google_Drive](https://drive.google.com/drive/folders/1MBk-m1igazL-uVFpjUKbL8pynuPNpZ2V?usp=sharing) and put the model into Yaml_and_Friend/ folder  
7. ```pip install opencv-python```
7. ```pip install Flask Flask-Uploads flask-cors```
8. go to code folder and run app.py  
   (Script.py is just a model prediction, test.py is WIP)  
                                    **Don't forget to Change the File Path**  

- **Remarks**
  Flask "werkzeug" cannot import name 'secure_filename' from 'werkzeug'  
  Change from: from werkzeug import secure_filename, FileStorage to  
  ```from werkzeug.utils import secure_filename 
     from werkzeug.datastructures import FileStorage```  

### Bank_note_ID id: 0 = 10Gen11, id: 1 = 100Gen11, 2 = 20Gen11, 3 = 5Gen11, 4 = 500Gen11
### Model.pth,config.yml should be along with test picture in Yaml_and_Friend
