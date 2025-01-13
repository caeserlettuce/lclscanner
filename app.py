from flask import Flask, Response, send_from_directory, request, redirect, jsonify, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os, sys, io
import json
import math
import random
import atexit
import logging
import numpy as np
from PIL import Image
import cv2
import base64



class bc:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


# [{"name": "wlamrat", "contents": [{"name": "cheese", "checked": true}, {"name": "parmesan", "checked": true}, {"name": "rat castle", "checked": true}]}]
# if the groceries.json ever needs to be reset

# print(bc.BLUE + "loading lumber.json" + bc.END)
# lumber_file = open('lumber.json', 'r+')
# lumber_json = json.load(lumber_file)
# lumber_file.close()

def exit_handler():
    # print(bc.CYAN + "\nwriting lumber.json..." + bc.END)
    # lumber_file_save = open("lumber.json", "w")
    # lumber_file_save.write(json.dumps(lumber_json))
    # lumber_file_save.close()
    print("\n\nbyebye")
atexit.register(exit_handler)

class NoGet(logging.Filter):
    def filter(self, record):
        return 'GET' not in record.getMessage() # will filter out any logs that include "GET"
class NoPost(logging.Filter):
    def filter(self, record):
        return 'POST' not in record.getMessage() # will filter out any logs that include "GET"

app = Flask(__name__)
log = logging.getLogger('werkzeug')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
app.secret_key = 'THERE IS NO WAY YOU COULD GUESS THIS IN A MILLION YEARS!!! 6490'
log.setLevel(logging.INFO)
log.addFilter(NoGet())
log.addFilter(NoPost())

# funny file functions
def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))

def get_file(filename):
    try:
        src = os.path.join(root_dir(), filename)
        return open(src).read()
    except IOError as exc:
        return str(exc)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# route functions (assets n stuff)
@app.route('/assets/<path:path>')
def send_report(path):
    return send_from_directory('assets', path)

@app.route('/style.css')
def style_css():
    return send_from_directory(".", "style.css")
@app.route('/mobile.css')
def mobile_css():
    return send_from_directory(".", "mobile.css")
@app.route('/scanner.js')
def scanner_js():
    return send_from_directory(".", "scanner.js")
@app.route('/styles/<path:path>')
def styles(path):
    return send_from_directory('styles', path)


#route functions (not assets)

@app.route("/", methods=['GET', 'POST'])
def route_groceries():
    return Response(get_file('scanner.html'))

# @app.route('/upload_image' , methods=['POST'])
# def upload_image():
# 	# print(request.files , file=sys.stderr)
# 	file = request.files['image'].read() ## byte file
# 	npimg = np.fromstring(file, np.uint8)
# 	img = cv2.imdecode(npimg,cv2.IMREAD_COLOR)
# 	######### Do preprocessing here ################
# 	# img[img > 150] = 0
# 	## any random stuff do here
# 	################################################
# 	img = Image.fromarray(img.astype("uint8"))
#     img.show()
# 	rawBytes = io.BytesIO()
# 	img.save(rawBytes, "JPEG")
# 	rawBytes.seek(0)
# 	img_base64 = base64.b64encode(rawBytes.read())
# 	return jsonify({'status':str(img_base64)})

@app.route('/upload_image', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        print("hi")
        # check if the post request has the file part
        if 'imagefile' not in request.files:
            flash('No file part')
            print("no file part")
            return redirect(request.url)
        file = request.files['imagefile']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_image', name=filename))
    return Response(get_file('scanner.html'))


# IMAGE UPLOADER WORKING (but it saves it to disk)
# figure out how to make it so that it saves the image to memory as a variable instead, so that way nobody can exploit it to save things to my computer
# and because it would use a lot of space to store all the images and yeah you get it




# TEMPLATE GET AND POST ROUTE
#
# @app.route('/get_groceries', methods=['GET', 'POST'])
# def getgroceries():
#     return_json = {}
#     request_json = request.get_json()
#     auth_username = request_json['auth_username']
#     auth_password = request_json['auth_password']
#     auth_authkey = request_json['auth_authkey']
#     print(bc.CYAN + "user \"" + bc.GREEN + auth_username + bc.CYAN + "\" is requesting ..." + bc.END)
#     user_authorised = account.auth(auth_username, auth_password, auth_authkey)
#     if user_authorised["authorised"] == True:
#         print(bc.GREEN + "user authorised!" + bc.END)
#     else:
#         print(bc.WARNING + "user not authorised! error code: " + bc.FAIL + account.error_code(user_authorised) + bc.END)
#         return_json["error"] = account.error_code(user_authorised)
#     return jsonify(return_json)