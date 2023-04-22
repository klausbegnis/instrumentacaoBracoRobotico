#Define Libraries
import RPi.GPIO as gpio
import time

#Configuring don’t show warnings 
gpio.setwarnings(False)

# definitions
x_pin = 27
y_pin = 22

xi = 50 # value readed
yi = 25 # value readed

x_max = 100 #mm
y_max = 100 #mm

period = 0.01 #s
frequency = 1/period # Hz

#Configuring GPIO
gpio.setmode(gpio.BCM)
gpio.setup(x_pin,gpio.OUT)
gpio.setup(y_pin,gpio.OUT)

#Configure the pwm objects and initialize its value
pwmX = gpio.PWM(x_pin,frequency)
pwmX.start(0)

pwmY = gpio.PWM(y_pin,frequency)
pwmY.start(100)
 
#Create the dutycycle variables
dcX = (xi/x_max)*100
dcY  = (yi/y_max)*100
print(dcX)
print(dcY)
#Loop infinite
while True:
    try:
        #increment gradually the luminosity
        pwmX.ChangeDutyCycle(dcX)

        time.sleep(0.05)
        dcX = dcX + 1
        print(dcX)

        if dcX == 100:
            dcX = 0

        #decrement gradually the luminosity
        pwmY.ChangeDutyCycle(dcY)
        time.sleep(0.05)
        dcY = dcY - 1
        print(dcY)
        if dcY == 0:
            dcY = 100
            
    except Exception as e:
        print(e)
        #End code
        gpio.cleanup()
        exit()