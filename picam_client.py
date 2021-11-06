import requests
import json

host = 'http://127.0.0.1'
port = 8888
base_uri = f"{host}:{port}"

def get_json(path, payload=None):
    """Perform an HTTP GET request and return the JSON response"""
    if not path.startswith("http"):
        path = base_uri + path
    if payload is not None:
        r = requests.get(path, payload)
    else:
        r = requests.get(path)
        
    r.raise_for_status()
    return r.json()

def post_json(path, payload={}):
    """Make an HTTP POST request and return the JSON response"""
    if not path.startswith("http"):
        path = base_uri + path
    r = requests.post(path, json=payload)
    r.raise_for_status()
    r = r.json()
    return r


def get_iso():
    # do homing of the robot
    path = '/picamera/iso'
    return_message = get_json(path)
    print(return_message)

get_iso()