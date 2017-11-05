from PIL import Image
import flask
from flask import Flask, request
import os
import subprocess
import json
application = Flask(__name__)

UPLOAD_FOLDER = '.'


@application.route('/upload', methods=['POST'])
def result():
    open('out.txt', 'w').close()
    image = request.files['upload_image']
    image.save(os.path.join('.', 'alpr.jpg'))
    cmd = "alpr -n 1 -j alpr.jpg >> out.txt"
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    out_dict = {}
    with open('out.txt') as json_file:
        data = json.load(json_file)
        for r in data['results']:
            out_dict['platenumber'] = r['plate']
            out_dict['spot'] = 1
    payload1 = json.dumps(out_dict)
    print(payload1)
    result = {"success":True}
    return flask.jsonify(result=result)
    
if __name__ == "__main__":
    application.run(host="0.0.0.0",port=8080)
