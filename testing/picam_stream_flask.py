from flask import Flask, render_template, Response, request
import time
import threading
import os
import cv2

try:
    import picamerax
except ModuleNotFoundError as e:
    import fake_picamera as picamerax

picamera = picamerax.PiCamera()
picamera.start_preview()


# App Globals (do not edit)
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html') #you can customze index.html here

def gen(camera):
    #get camera frame
    while True:
        frame = camera.capture()
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame =  jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(picamera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)