#!/usr/bin/env python
# Import FastAPI
# https://github.com/EbenKouao/pi-camera-stream-flask/blob/master/camera.py
import cv2
from pydantic import BaseModel
from typing import List
import logging
import time
import uvicorn
import io
import base64

try:
    import picamerax
except ModuleNotFoundError as e:
    import fake_picamera as picamerax

# Richard's fix gain 
from set_picamera_gain import set_analog_gain, set_digital_gain

# init logging
logger = logging.getLogger('picamera')
logger.setLevel(logging.DEBUG)
from flask import Flask, render_template, Response, send_file

app = Flask(__name__)

@app.route("/picamera/iso", methods=['GET'])
def get_iso():
    iso = camera.iso
    logger.debug('get iso value: %i',iso)
    return {"iso" : iso}

@app.route("/picamera/iso", methods=['GET'])
def set_iso(iso=200):
    camera.iso = iso
    logger.debug('set iso value: %i',iso)
    return {"iso" : iso}

@app.route("/picamera/exposuretime", methods=['GET'])
def set_exposuretime(exposuretime=10000):
    camera.iso = exposuretime
    logger.debug('set exposuretime value: %i',exposuretime)
    return {"exposuretime" : exposuretime}

#https://gist.github.com/kylehounslow/767fb72fde2ebdd010a0bf4242371594
@app.route('/picamera/singleframe') #,methods=['POST'])
def getframe(format: str="jpeg"):
    # Create an in-memory stream
    camera.capture()
    myframe = camera.capture()  
    if format == "png":
        file_format = ".png"
        media_type = "image/png"
    if format == "jpeg":
        file_format = ".jpg"
        media_type = "image/jpeg"
    image = cv2.imencode(file_format, myframe)[1].tobytes()
    return Response(response=image, content_type=media_type)
    #return send_file(image, mimetype='image/jpeg')

def framegenerator():
    while True:
        frame = cv2.imencode('.jpg', camera.capture())[1].tobytes()
        try:
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except Exception as e:
            print(e)
            print("Yield Exception")
            return

@app.route("/picamera/stream", methods=['GET']) # todo authentication
def start_stream():
    return Response(framegenerator(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

camera = picamerax.PiCamera()
camera.start_preview()

if __name__ == "__main__":
    is_stream = False
    app.run(host='0.0.0.0', debug=True)


