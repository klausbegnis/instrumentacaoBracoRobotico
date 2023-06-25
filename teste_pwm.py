import cv2
import numpy as np
from RASP.rasp import GPIOmanager
import time
GPIO = GPIOmanager(100,100)
GPIO.update_dc(55,23)

time.sleep(5000000)