import cv2
import numpy as np
from RASP.rasp import GPIOmanager
import time
GPIO = GPIOmanager(196,160)
GPIO.update_dc(32,155)

time.sleep(5000000)