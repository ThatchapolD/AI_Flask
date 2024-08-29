# This is the merge of Faster-RCNN and Flask with the result becoming RESTAPI

**The python version needs in this code is <=3.9**

- **Remarks**
  Flask "werkzeug" cannot import name 'secure_filename' from 'werkzeug'  
  Change from: from werkzeug import secure_filename, FileStorage to  
  `from werkzeug.utils import secure_filename`  
  `from werkzeug.datastructures import FileStorage`

### Bank_note_ID will always start with value then generation series Ex. 5Gen11 means 5 baht gen 11
