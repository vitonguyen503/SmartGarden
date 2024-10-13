from Simulator.EmulatorGUI import GPIO
from Simulator.DHT22 import DHT22
from Simulator.pnhLCD1602 import LCD1602
import pygame
import time
import traceback


def Main():
    try:
        GPIO.setmode(GPIO.BCM)

        GPIO.setwarnings(False)

        MAX_TEMP_UP = 14
        MAX_TEMP_DOWN = 4
        INPUT = 3
        ALERT = 2
      
        # Setup GPIO pin
        GPIO.setup(ALERT, GPIO.OUT) 
        GPIO.setup(INPUT, GPIO.IN) 
        GPIO.setup(MAX_TEMP_UP, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) 
        GPIO.setup(MAX_TEMP_DOWN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) 

        # Read data from sensor
        lcd = LCD1602(300, 100)
        input = DHT22(INPUT)
        print(input.read())
        allow_temp = 25

        # Display to LCD
        while(True):
            lcd.clear()
            temp, humidity = input.read()

            lcd.set_cursor(0, 0)  # Đặt con trỏ ở dòng thứ 2
            lcd.write_string(f"Temp: {round(temp, 1)}")
            lcd.set_cursor(1, 0)
            lcd.write_string(f"Limit: {allow_temp}")

            time.sleep(1)
            if temp > allow_temp:
                lcd.clear()
                lcd.set_cursor(0, 0)
                lcd.write_string("High temp!")
                GPIO.output(ALERT, GPIO.HIGH)
            
            while GPIO.input(MAX_TEMP_UP) == True:
                lcd.clear()
                lcd.set_cursor(0, 0)
                allow_temp += 1
                lcd.write_string(f"Allow temp: {allow_temp}")
                time.sleep(1)
            while GPIO.input(MAX_TEMP_DOWN) == True:
                lcd.clear()
                lcd.set_cursor(0, 0)                    
                allow_temp -= 1
                lcd.write_string(f"Allow temp: {allow_temp}")
                time.sleep(1)

            time.sleep(1)
            
 
    except Exception as ex:
        traceback.print_exc()
    finally:
        GPIO.cleanup() #this ensures a clean exit
    
Main()
    












