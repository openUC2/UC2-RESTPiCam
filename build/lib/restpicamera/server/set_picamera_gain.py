# copyright: openflexure from set_picamera_gain.py
from __future__ import print_function

import logging
import time
from typing import Union

try:
    import picamerax
    from picamerax import exc, mmal
    from picamerax.mmalobj import to_rational
    MMAL_PARAMETER_ANALOG_GAIN: int = mmal.MMAL_PARAMETER_GROUP_CAMERA + 0x59
    MMAL_PARAMETER_DIGITAL_GAIN: int = mmal.MMAL_PARAMETER_GROUP_CAMERA + 0x5A


except:
    import fake_picamera as picamerax
    MMAL_PARAMETER_ANALOG_GAIN = 0
    MMAL_PARAMETER_DIGITAL_GAIN = 0





def set_gain(camera: picamerax.PiCamera, gain: int, value: Union[int, float]):
    """Set the analog gain of a PiCamera.

    camera: the picamerax.PiCamera() instance you are configuring
    gain: either MMAL_PARAMETER_ANALOG_GAIN or MMAL_PARAMETER_DIGITAL_GAIN
    value: a numeric value that can be converted to a rational number.
    """
    if gain not in [MMAL_PARAMETER_ANALOG_GAIN, MMAL_PARAMETER_DIGITAL_GAIN]:
        raise ValueError("The gain parameter was not valid")
    ret = mmal.mmal_port_parameter_set_rational(
        camera._camera.control._port, gain, to_rational(value)  # pylint: disable=W0212
    )
    if ret == 4:
        raise exc.PiCameraMMALError(
            ret,
            "Are you running the latest version of the userland libraries? Gain setting was introduced in late 2017.",
        )
    elif ret != 0:
        raise exc.PiCameraMMALError(ret)


def set_analog_gain(camera: picamerax.PiCamera, value: Union[int, float]):
    """Set the gain of a PiCamera object to a given value."""
    set_gain(camera, MMAL_PARAMETER_ANALOG_GAIN, value)


def set_digital_gain(camera: picamerax.PiCamera, value: Union[int, float]):
    """Set the digital gain of a PiCamera object to a given value."""
    set_gain(camera, MMAL_PARAMETER_DIGITAL_GAIN, value)


if __name__ == "__main__":
    with picamerax.PiCamera() as cam:
        cam.start_preview(fullscreen=False, window=(0, 50, 640, 480))
        time.sleep(2)

        # fix the auto white balance gains at their current values
        g = cam.awb_gains
        cam.awb_mode = "off"
        cam.awb_gains = g

        # fix the shutter speed
        cam.shutter_speed = cam.exposure_speed

        logging.info("Current a/d gains: %s, %s", cam.analog_gain, cam.digital_gain)

        logging.info("Attempting to set analogue gain to 1")
        set_analog_gain(cam, 1)
        logging.info("Attempting to set digital gain to 1")
        set_digital_gain(cam, 1)

        try:
            while True:
                logging.info(
                    "Current a/d gains: %s, %s", cam.analog_gain, cam.digital_gain
                )
                time.sleep(1)
        except KeyboardInterrupt:
            logging.info("Stopping...")
