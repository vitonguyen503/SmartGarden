from Library.EmulatorGUI import GPIO
# from Simulator.DHT22 import DHT22 
from Library.LCD import LCD1602 
from Library.AHT20 import AHT20
import pygame
import time
import traceback
import random
import threading

asTem, soilMoi = 0, 0
n, p, k = 0, 0, 0

def Main():
    try:
        GPIO.setmode(GPIO.BCM)

        GPIO.setwarnings(False)

        AHT20_1 = 2
        AHT20_2 = 3
        SOIL_MOI = 17
        LED = 23
        BUZZER = 22
        PUMP = 24
        UP = 16
        DOWN = 19
        RESET = 20
        OK = 26

        gpioPin = [AHT20_1, AHT20_2, SOIL_MOI, LED, BUZZER, PUMP, UP, DOWN, RESET, OK]
      
        # Setup GPIO pin
        for pin in gpioPin:
            if pin == LED or pin == BUZZER:
                GPIO.setup(pin, GPIO.OUT)
            else:
                GPIO.setup(pin, GPIO.IN)

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