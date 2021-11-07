import requests
import json
from PIL import Image
from io import BytesIO
import numpy as np


class restpicamera():
    def __init__(self, host, port=80):
        self. base_uri = f"{host}:{port}"
        
    def get_json(self, path, payload=None):
        """Perform an HTTP GET request and return the JSON response"""
        if not path.startswith("http"):
            path = self.base_uri + path
        if payload is not None:
            r = requests.get(path, payload)
        else:
            r = requests.get(path)
            
        r.raise_for_status()
        return r.json()

    def post_json(self, path, payload={}):
        """Make an HTTP POST request and return the JSON response"""
        if not path.startswith("http"):
            path = self.base_uri + path
        r = requests.post(path, json=payload)
        r.raise_for_status()
        r = r.json()
        return r


    def get_iso(self):
        # do homing of the robot
        path = '/picamera/iso'
        return_message = self.get_json(path)
        print(return_message)


    def get_snap(self):
        path = '/picamera/singleframe'
        r = requests.get(self.base_uri + path)
        r.raise_for_status()
        image = Image.open(BytesIO(r.content))
        return np.asarray(image)


if __name__ == "__main__":
    host = "http://0.0.0.0"
    port = "5000"

    rc = restpicamera(host, port)
    print(rc.get_iso())
    print(rc.get_snap())
