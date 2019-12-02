from flask import Flask, render_template, Response
from flask import request, json, jsonify
import base64
import jpype # pip install jpype1
import os
import time

ALLOWED_EXTENSIONS = ['jpg', 'png', 'bmp', 'jpeg']

class JavaServer(object):
    root_dir = "../"
    jvmPath = "/usr/lib/jvm/jdk1.8.0_172/jre/lib/amd64/server/libjvm.so"
    jarPath = os.path.join(root_dir, "dist/liredemo.jar")
    dependency = os.path.join(root_dir, "dist/lib")
    server = None

    def __init__(self):
        # convertStrings=True is necessary for converting java String to python string
        try:
            self.jvmPath = jpype.getDefaultJVMPath()
        except JVMNotFoundException:
            self.jvmPath = "/usr/lib/jvm/jdk1.8.0_172/jre/lib/amd64/server/libjvm.so"
        jpype.startJVM(self.jvmPath, "-ea", "-Djava.class.path=%s" % self.jarPath, "-Djava.ext.dirs=%s" % self.dependency, convertStrings=True)
        JDClass = jpype.JClass("liredemo.Main")
        self.server = JDClass()

    def func(self, img_name): 
        # img_name: str 
        return self.server.searchImage(img_name) # waste half a day for lack of return!!!

    def __del__(self):
        jpype.shutdownJVM()

app = Flask(__name__) 
js = JavaServer()

@app.route('/') 
def index_upload():
    return render_template('upload.html')

# save the image as a picture
@app.route('/img_upload', methods=['POST'])
def img_upload():
    req_file = request.files['imgFile']  # get the image
    # print(type(req_file),req_file) # <class 'werkzeug.datastructures.FileStorage'> <FileStorage: 'blob' ('image/jpeg')>
    name_sub = req_file.filename.split('.')[1].lower()
    if name_sub not in ALLOWED_EXTENSIONS:
        res_str = "request image error: format not support"
        print(res_str)
        return res_str 

    img_name = 'static/upload.{}'.format(name_sub)
    req_file.save(img_name)

    start_time = time.time()
    res_jstr = js.func(img_name) # <class 'jpype._jclass.java.lang.String[]'> 
    print("api cost: ", time.time()-start_time)
    
    html_str = '''''' # None
    for idx, res_path in enumerate(res_jstr):
        # print(res_path)
        img_f = open(res_path, 'rb')
        bs64data = base64.b64encode(img_f.read()).decode()
        img_f.close()
        html_str += '''<img src="data:image/jpeg;base64,{}" style="width:100%;height:100%;"/> <br/>'''.format(bs64data)
    return html_str


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001 , threaded=True)