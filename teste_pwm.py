import cv2
import numpy as np
from RASP.rasp import GPIOmanager
import time
GPIO = GPIOmanager(196,160)
GPIO.update_dc(98,80)

time.sleep(5000000)