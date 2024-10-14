from Library.EmulatorGUI import GPIO
# from Simulator.DHT22 import DHT22 
from Library.LCD import LCD1602 
from Library.AHT20 import AHT20
import pygame
import time
import traceback
import random
import threading

# This is the Mid-term exam's code. Just use for watching how we can handle thread in python

temp, hum = 0, 0
count_70, count_50 = 0, 0

def Main():
    try:
        GPIO.setmode(GPIO.BCM)

        GPIO.setwarnings(False)

        WEIGHT_70 = 27
        WEIGHT_50 = 17
        ROLE_70 = 26
        ROLE_50 = 22
        LCD1 = 2
        LCD2 = 3
        START = 24
        STOP = 23
        LED = 16
        DHT22_INPUT = 4

        gpioPin = [WEIGHT_70, WEIGHT_50, ROLE_70, ROLE_50, LCD1, LCD2, START, STOP, LED, DHT22_INPUT]
      
        # Setup GPIO pin
        for pin in gpioPin:
            if pin == START or pin == STOP:
                GPIO.setup(pin, GPIO.IN, initial=GPIO.HIGH, pull_up_down=GPIO.PUD_UP)
            elif pin == DHT22_INPUT:
                GPIO.setup(pin, GPIO.IN)
            else:
                GPIO.setup(pin, GPIO.OUT)

        # Read data from sensor
        lcd = LCD1602(300, 100)
        dht22Value = DHT22(DHT22_INPUT)

        def getItemWeight():
            weight = random.uniform(30.0, 100.0)
            return weight

        def getDataFromDHT22(dht22Value):
            global temp, hum
            while not stopCountFlag.is_set():
                t, h = dht22Value.read()
                temp, hum = t, h
                time.sleep(2)
        
        def displayLCDBeforeStart(lcd):
            global temp, hum
            while not startCountFlag.is_set():
                lcd.clear()
                lcd.set_cursor(0, 0)  
                lcd.write_string("DEM SAN PHAM B")
                lcd.set_cursor(1, 0)
                lcd.write_string(f"T: {round(temp, 1)}, H: {round(hum, 1)}")
                time.sleep(1)

        def onOffLED():
            while not stopCountFlag.is_set():
                GPIO.output(LED, GPIO.HIGH)
                time.sleep(0.5)
                GPIO.output(LED, GPIO.LOW)
                time.sleep(0.5)

        def startCount():
            global count_70, count_50
            while not stopCountFlag.is_set():
                weight = getItemWeight()
                if weight > 70:
                    count_70 += 1
                    GPIO.output(WEIGHT_70, GPIO.HIGH)
                    GPIO.output(ROLE_70, GPIO.HIGH)
                elif weight > 50:
                    count_50 += 1
                    GPIO.output(WEIGHT_50, GPIO.HIGH)
                    GPIO.output(ROLE_50, GPIO.HIGH)
                time.sleep(1)
                GPIO.output(WEIGHT_70, GPIO.LOW)
                GPIO.output(WEIGHT_50, GPIO.LOW)
                GPIO.output(ROLE_70, GPIO.LOW)
                GPIO.output(ROLE_50, GPIO.LOW)

        def displayLCDAfterStart(lcd):
            global count_70, count_50, temp, hum
            while not stopCountFlag.is_set():
                lcd.clear()
                lcd.set_cursor(0, 0)  
                lcd.write_string(f"T: {round(temp, 1)}, H: {round(hum, 1)}")
                lcd.set_cursor(1, 0)
                lcd.write_string(f"70: {count_70}, 50: {count_50}")
                time.sleep(1)

        startCountFlag = threading.Event()
        stopCountFlag = threading.Event()

        getDHT22Thread = threading.Thread(target=getDataFromDHT22, args=(dht22Value,))
        LCDBeforeStartThread = threading.Thread(target=displayLCDBeforeStart, args=(lcd,))
        controlLEDThread = threading.Thread(target=onOffLED)
        countThread = threading.Thread(target=startCount)
        LCDAfterStartThread = threading.Thread(target=displayLCDAfterStart, args=(lcd,))

        getDHT22Thread.start()
        LCDBeforeStartThread.start()

        while(True):
            if GPIO.input(START) == False:
                startCountFlag.set()
                if stopCountFlag.is_set():
                    startCountFlag.clear()
                if not controlLEDThread.is_alive() and not countThread.is_alive() and not LCDAfterStartThread.is_alive():
                    controlLEDThread.start()
                    countThread.start()
                    LCDAfterStartThread.start()

            if GPIO.input(STOP) == False:
                stopCountFlag.set()
                if startCountFlag.is_set():
                    startCountFlag.clear()
                
                
 
    except Exception as ex:
        traceback.print_exc()
    finally:
        GPIO.cleanup() 
    
Main()