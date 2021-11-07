import numpy as np  # type: ignore
from fractions import Fraction
import threading
import matplotlib.pyplot as plt
import time

class PiCamera():
    """Fake class"""
    resolution = (640, 480)
    exposuretime = 10000 # ms
    framerate = Fraction(1, 6)
    shutter_speed = 6000000
    exposure_mode = 'off'
    frame = np.zeros((*resolution,3))
    iso = 800
    is_stop = False
    framerate = 24

    def __init__(self, resolution=(640, 480), framerate=24):
        # empty constructor
        # print('WARNING: Fake_RPi PiCamera on {}'.format(platform.system().lower()))
        self.resolution = resolution
        self.framerate = framerate


    def __framegenerator__(self):
        while not self.is_stop:
            self.frame = np.uint8(255*np.random.rand(*self.resolution))
            time.sleep(.05)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def close(self):
        # this does nothing
        pass

    def capture(self, output=None, format=None, use_video_port=False, resize=None, splitter_port=0, **options):
        # this does nothing
        if type(output)==str:
            current_frame = self.frame
            plt.imsave(output, current_frame)
        return self.frame

    def start_preview(self):
        self.imagingtask = threading.Thread(target=self.__framegenerator__)
        self.imagingtask.start()
        self.is_stop = False
        print("Camera started")

    def stop_preview(self):
        print("Camera stopped")
        self.is_stop = True
        self.imagingtask.join()

    def start_recording(self, output, format):
        print(output)
        pass

    def stop_recording(self, output, format):
        pass



if __name__ == "__main__":
    import time
    # import fake_picamera as fp
    camera = fp.PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 24
    camera.start_preview()
    camera.annotate_text = 'Hello world!'
    time.sleep(2)
    # Take a picture including the annotation
    camera.capture('foo.jpg')
    print(camera.capture().shape)
    #plt.imshow(np.mean(camera.capture(),-1))
    #plt.show()
    camera.stop_preview()