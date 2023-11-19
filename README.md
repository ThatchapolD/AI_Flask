# This is the merge of Faster-RCNN and Flask with the result becoming RESTAPI

## Follow this step to create venv and download model.pth
1. ```git clone https://github.com/facebookresearch/detectron2.git```  
2. ```pip install -r requirements.txt```  
   python -m pip install -e detectron2 ?? Not working for mac ? can't find module name torch  
   Run this instead: ```python setup.py build develop```
3. go to code folder and run app.py
   (Script.py is just a model prediction, test.py is WIP)

- **Remarks**
  Flask "werkzeug" cannot import name 'secure_filename' from 'werkzeug'  
  Change from: from werkzeug import secure_filename, FileStorage  
  To: from werkzeug.utils import secure_filename  
  from werkzeug.datastructures import FileStorage  

### Bank_note_ID id: 0 = 10Gen11, id: 1 = 100Gen11, 2 = 20Gen11, 3 = 5Gen11, 4 = 500Gen11
### Model.pth,config.yml and some dic pic test are in Yaml_and_Friend
