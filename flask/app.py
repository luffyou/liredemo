from flask import Flask, render_template, Response
from flask import request, json, jsonify
import base64
import jpype # pip install jpype1
import os
import time
from PIL import Image
from io import BytesIO

ALLOWED_EXTENSIONS = ['jpg', 'png', 'bmp', 'jpeg']
RES_IMG_SIZE = 256
RES_IMG_ROW = 3
RES_IMG_COL = 2

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
        return jsonify({'status':res_str }) 

    img_name = 'static/upload.{}'.format(name_sub)
    req_file.save(img_name)

    start_time = time.time()
    res_jstr = js.func(img_name) # <class 'jpype._jclass.java.lang.String[]'> 
    print("api cost: ", time.time()-start_time)
    post_time = time.time()

    # html_str = '''''' # None
    # for idx, res_path in enumerate(res_jstr):
    #     # print(res_path)
    #     img_f = open(res_path, 'rb')
    #     bs64data = base64.b64encode(img_f.read()).decode()
    #     img_f.close()
    #     html_str += '''<img src="data:image/jpeg;base64,{}" style="width:100%;height:100%;"/> <br/>'''.format(bs64data)
    # print("post cost: ", time.time()-post_time)
    # return jsonify({'viz': html_str, 'status':str(time.time()-start_time)})

    to_image = Image.new('RGB', (RES_IMG_COL * RES_IMG_SIZE, RES_IMG_ROW * RES_IMG_SIZE))
    for y in range(1, RES_IMG_ROW + 1):
        for x in range(1, RES_IMG_COL + 1):
            from_image = Image.open(res_jstr[RES_IMG_COL * (y - 1) + x - 1]).resize((RES_IMG_SIZE, RES_IMG_SIZE),Image.ANTIALIAS)
            to_image.paste(from_image, ((x - 1) * RES_IMG_SIZE, (y - 1) * RES_IMG_SIZE))
    output_buffer = BytesIO()
    to_image.save(output_buffer, format='JPEG')
    byte_data = output_buffer.getvalue()
    bs64data = base64.b64encode(byte_data).decode()
    html_str = '''<img src="data:image/jpeg;base64,{}" style="width:100%;height:100%;"/> <br/>'''.format(bs64data)
    print("post cost: ", time.time()-post_time)
    return jsonify({'viz': html_str, 'status':str(time.time()-start_time)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001 , threaded=True)