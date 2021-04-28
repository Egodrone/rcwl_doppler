#!/usr/bin/env python3


from picamera import PiCamera
import RPi.GPIO as GPIO
from time import sleep
import datetime
import pathlib


GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)

camera = PiCamera()
camera.resolution = (1024, 768)


def set_proc_name(newname):
    ''' Change process name '''
    from ctypes import cdll, byref, create_string_buffer
    libc = cdll.LoadLibrary('libc.so.6')
    buff = create_string_buffer(len(newname)+1)
    newname = newname.encode("utf-8")
    buff.value = newname
    libc.prctl(15, byref(buff), 0, 0, 0)


def get_proc_name():
    ''' Display current process name '''
    from ctypes import cdll, byref, create_string_buffer
    libc = cdll.LoadLibrary('libc.so.6')
    buff = create_string_buffer(128)
    libc.prctl(16, byref(buff), 0, 0, 0)
    return buff.value


def display():
    print("Changing process name from: " + str(get_proc_name()))
    set_proc_name('Doppler Camera')
    print("To: " + str(get_proc_name()))


def detector():
    timestamp = str((datetime.datetime.now()))
    timestamp = timestamp[0:19]
    tlisted = list(timestamp)
    tlisted[10] = tlisted[13] = tlisted[16] = "-"
    timestamp = "".join(tlisted)
    print("Video captured at: ", timestamp)

    camera.start_preview()
    camera.start_recording(str(pathlib.Path(__file__).parent.absolute()) + "/records/" + str(timestamp) + ".h264")
    sleep(10)
    camera.stop_recording()
    camera.stop_preview()


if __name__ == "__main__":
    display()

    while True:
        if(GPIO.input(17) == 1):
            detector()
        else:
            pass
        sleep(0.2)
