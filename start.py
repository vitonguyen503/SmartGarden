from Simulator.EmulatorGUI import GPIO
from Simulator.pnhLCD1602 import LCD1602
import time
import traceback
import threading

def Main():
    try:
        BTN_UP = 16
        BTN_DOWN = 19
        BTN_OK = 26
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        GPIO.setup(BTN_UP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(BTN_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(BTN_OK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        vegetables = ["rau muống", "rau cải", "bắp cải", "xà lách", "rau mùng tơi", "rau dền", "bí đỏ", "rau khoai lang", "khoai tây"]
        global current_selection  
        current_selection = 0  
        lcd = LCD1602(320, 150)
        
        global startCountFlag
        startCountFlag = threading.Event()
        
        global visible_offset
        visible_offset = 0  
        
        def move_selection_up():
            global current_selection, visible_offset
            if current_selection > 0:
                current_selection -= 1
                if current_selection < visible_offset:
                    visible_offset -= 1  
            else:  
                current_selection = len(vegetables) - 1
                visible_offset = max(0, len(vegetables) - 3)
                
            display_current_selection()  

        def move_selection_down():
            global current_selection, visible_offset
            if current_selection < len(vegetables) - 1:
                current_selection += 1
                if current_selection > visible_offset + 2:  
                    visible_offset += 1  
            else: 
                current_selection = 0
                visible_offset = 0  
                
            display_current_selection()  

        def select_vegetable():
            global startCountFlag
            startCountFlag.set()  
            threading.Thread(target=showMessage).start()
        
        def display_current_selection():
            lcd.clear()
            lcd.set_cursor(0, 0)
            lcd.write_string("LUA CHON LOAI RAU")
            
            for i in range(3):
                if visible_offset + i < len(vegetables):
                    lcd.set_cursor(0, i + 1)
                    if current_selection == visible_offset + i:
                        lcd.write_string(f"> {vegetables[visible_offset + i]}")
                    else:
                        lcd.write_string(f"  {vegetables[visible_offset + i]}")  
        
        def showMessage():
            lcd.clear()  
            lcd.set_cursor(0, 0)
            lcd.write_string("Hello iemquynh")  
            

        display_current_selection()

        while not startCountFlag.is_set():
            if GPIO.input(BTN_UP) == GPIO.LOW:  
                move_selection_up()
                time.sleep(0.3)  
            elif GPIO.input(BTN_DOWN) == GPIO.LOW:  
                move_selection_down()
                time.sleep(0.3)  
            elif GPIO.input(BTN_OK) == GPIO.LOW:  
                select_vegetable()
                time.sleep(0.3)  

    except Exception as ex:
        traceback.print_exc()
    finally:
        GPIO.cleanup() 
   
Main()
