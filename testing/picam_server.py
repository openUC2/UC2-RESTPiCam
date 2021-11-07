# Import FastAPI
from fastapi import FastAPI
from fastapi_utils.cbv import cbv
from fastapi import APIRouter
from fastapi_utils.inferring_router import InferringRouter
from fastapi.responses import StreamingResponse

import cv2
from pydantic import BaseModel
from typing import List
import logging
import time
import uvicorn
import io

try:
    import picamerax
except ModuleNotFoundError as e:
    import fake_picamera as picamerax

# Richard's fix gain 
from set_picamera_gain import set_analog_gain, set_digital_gain

# init logging
logger = logging.getLogger('picamera')
logger.setLevel(logging.DEBUG)



# Initialize the app
app = FastAPI()
router = APIRouter(tags=['camera'])

'''
get settings
'''
@router.get('/picamera/iso')
async def get_iso():
    iso = camera.iso
    logger.debug('get iso value: %i',iso)
    return {"iso" : iso}

@router.post('/picamera/iso')
async def set_iso(iso=200):
    camera.iso = iso
    logger.debug('set iso value: %i',iso)
    return {"iso" : iso}

@router.post('/picamera/exposuretime')
async def set_exposuretime(exposuretime=10000):
    camera.iso = exposuretime
    logger.debug('set exposuretime value: %i',exposuretime)
    return {"exposuretime" : exposuretime}

@router.post('/picamera/singleframe')
async def getframe(format: str = "png"):
    myframe = camera.capture()  
    if format == "png":
        file_format = ".png"
        media_type = "image/png"
    if format == "jpeg":
        file_format = ".jpg"
        media_type = "image/jpeg"
    res, im_png = cv2.imencode(file_format, myframe)
    return StreamingResponse(io.BytesIO(im_png.tobytes()), media_type=media_type)


def framegenerator():
    while True:
        frame = camera.capture()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@router.post('/picamera/stream')
def video_feed():
    return StreamingResponse(framegenerator(),
                    media_type='multipart/x-mixed-replace; boundary=frame')

@router.post('/picamera/startstream')
async def startstream(format: str = "png"):
    if format == "png":
        file_format = ".png"
        media_type = "image/png"
    elif format == "jpeg":
        file_format = ".jpg"
        media_type = "image/jpeg"

    while is_stream:
        myframe = camera.capture()  
        res, image = cv2.imencode(file_format, myframe)
        StreamingResponse(io.BytesIO(image.tobytes()), media_type=media_type)



camera = picamerax.PiCamera()
camera.start_preview()

if __name__ == "__main__":
    is_stream = False

    app.include_router(router)
    uvicorn.run(app, host="0.0.0.0", port=8888)


'''

    interesting settings to read
            conf_dict: dict = {
                "stream_resolution": self.stream_resolution,
                "image_resolution": self.image_resolution,
                "numpy_resolution": self.numpy_resolution,
                "jpeg_quality": self.jpeg_quality,
                "mjpeg_quality": self.mjpeg_quality,
                "mjpeg_bitrate": self.mjpeg_bitrate,
                "picamera": {},
            }
            


    def update_settings(self, config: dict):
        # copyright: from openflexure server picamera.py
        paused_stream = False
        logging.debug("PiCameraStreamer: applying config:")
        logging.debug(config)

        # Pause stream while changing settings
        if self.stream_active:  # If stream is active
            logging.info("Pausing stream to update config.")
            self.stop_stream()  # Pause stream
            paused_stream = True  # Remember to unpause stream when done

        # PiCamera parameters
        if "picamera" in config:  # If new settings are given
            self.apply_picamera_settings(
                config["picamera"], pause_for_effect=True
            )

        # PiCameraStreamer parameters
        for key, value in config.items():  # For each provided setting
            if (key != "picamera") and hasattr(self, key):
                setattr(self, key, value)

        # If stream was paused to update config, unpause
        if paused_stream:
            logging.info("Resuming stream.")
            self.start_stream()

        else:
            raise Exception(
                "Cannot update camera config while recording is active."
            )

    def apply_picamera_settings(
        self, settings_dict: dict, pause_for_effect: bool = True
    ):
        """

        Args:
            settings_dict (dict): Dictionary of properties to apply to the :py:class:`picamerax.PiCamera`: object
            pause_for_effect (bool): Pause tactically to reduce risk of timing issues
        """
        # Set exposure mode
        if "exposure_mode" in settings_dict:
            logging.debug(
                "applying exposure_mode: %s", (settings_dict["exposure_mode"])
            )
            self.picamera.exposure_mode = settings_dict["exposure_mode"]

        # apply gains and let them settle
        if "analog_gain" in settings_dict:
            logging.debug("applying analog_gain: %s", (settings_dict["analog_gain"]))
            set_analog_gain(self.picamera, float(settings_dict["analog_gain"]))
        if "digital_gain" in settings_dict:
            logging.debug("applying digital_gain: %s", (settings_dict["digital_gain"]))
            set_digital_gain(self.picamera, float(settings_dict["digital_gain"]))

        # apply shutter speed
        if "shutter_speed" in settings_dict:
            logging.debug(
                "applying shutter_speed: %s", (settings_dict["shutter_speed"])
            )
            self.picamera.shutter_speed = int(settings_dict["shutter_speed"])

        time.sleep(0.2)  # Let gains settle

        # Handle AWB in a half-smart way
        if "awb_gains" in settings_dict:
            logging.debug("applying awb_mode: off")
            self.picamera.awb_mode = "off"
            logging.debug("applying awb_gains: %s", (settings_dict["awb_gains"]))
            self.picamera.awb_gains = settings_dict["awb_gains"]
        elif "awb_mode" in settings_dict:
            logging.debug("applying awb_mode: %s", (settings_dict["awb_mode"]))
            self.picamera.awb_mode = settings_dict["awb_mode"]

        # Handle some properties that can be quickly applied
        batched_keys = ["framerate", "saturation"]
        for key in batched_keys:
            if (key in settings_dict) and hasattr(self.picamera, key):
                logging.debug("applying %s: %s", key, settings_dict[key])
                setattr(self.picamera, key, settings_dict[key])

        # Final optional pause to settle
        if pause_for_effect:
            time.sleep(0.2)
'''
