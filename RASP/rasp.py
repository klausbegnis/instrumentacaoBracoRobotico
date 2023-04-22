#Define Libraries
import RPi.GPIO as gpio
import time

#Configuring don’t show warnings 
gpio.setwarnings(False)

x_pin = 27
y_pin = 22

#Configuring GPIO
gpio.setmode(gpio.BCM)
gpio.setup(x_pin,gpio.OUT)
gpio.setup(y_pin,gpio.OUT)

#Configure the pwm objects and initialize its value
pwmBlue = gpio.PWM(x_pin,100)
pwmBlue.start(0)

pwmRed = gpio.PWM(y_pin,100)
pwmRed.start(100)
 
#Create the dutycycle variables
dcBlue = 0
dcRed  = 100

#Loop infinite
while True:
    try:
        #increment gradually the luminosity
        pwmBlue.ChangeDutyCycle(dcBlue)
        time.sleep(0.05)
        dcBlue = dcBlue + 1
        if dcBlue == 100:
            dcBlue = 0

        #decrement gradually the luminosity
        pwmRed.ChangeDutyCycle(dcRed)
        time.sleep(0.05)
        dcRed = dcRed - 1
        if dcRed == 0:
            dcRed = 100
    except Exception as e:
        print(e)
        #End code
        gpio.cleanup()
        exit()