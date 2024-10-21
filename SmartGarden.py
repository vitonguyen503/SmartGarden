from Library.EmulatorGUI import GPIO
from Library.LCD import LCD1602
from Library.SoilMoistureSensor import SoilMoistureSensor
from Library.SoilNPKSensor import SoilNPKSensor
from Library.AHT20 import AHT20
import time 
import traceback
import threading

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
        BTN_UP = 16
        BTN_DOWN = 19
        BTN_RESET = 20
        BTN_OK = 26

        gpioPin = [AHT20_1, AHT20_2, SOIL_MOI, LED, BUZZER, PUMP, BTN_UP, BTN_DOWN, BTN_RESET, BTN_OK]
        vegetables = ["Rau muống", "Rau cải", "Bắp cải", "Xà lách", "Rau mùng tơi", "Rau dền", "Bí đỏ", "Rau khoai lang", "Khoai tây"]
        vegetablesInfo = {
            "atmosphereTemperature": [10, 30],
            "0": {
                "humidity": [65, 75],
                "N": [0.4, 0.6],
                "P": [0.2, 0.3],
                "K": [0.2, 0.3]
            },
            "1": {
                "humidity": [60, 70],
                "N": [0.4, 0.6],
                "P": [0.2, 0.3],
                "K": [0.2, 0.3]
            },
            "2": {
                "humidity": [60, 80],
                "N": [0.6, 1],
                "P": [0.3, 0.5],
                "K": [0.3, 0.5]
            },
            "3": {
                "humidity": [60, 70],
                "N": [0.4, 0.6],
                "P": [0.2, 0.3],
                "K": [0.2, 0.3]
            },
            "4": {
                "humidity": [65, 75],
                "N": [0.4, 0.6],
                "P": [0.2, 0.3],
                "K": [0.2, 0.3]
            },
            "5": {
                "humidity": [60, 70],
                "N": [0.4, 0.6],
                "P": [0.2, 0.3],
                "K": [0.2, 0.3]
            },
            "6": {
                "humidity": [60, 70],
                "N": [0.6, 1],
                "P": [0.3, 0.5],
                "K": [0.3, 0.5]
            },
            "7": {
                "humidity": [65, 75],
                "N": [0.6, 1],
                "P": [0.3, 0.5],
                "K": [0.3, 0.5]
            },
            "8": {
                "humidity": [60, 80],
                "N": [0.6, 1],
                "P": [0.3, 0.5],
                "K": [0.3, 0.5]
            },
        }
        
        lcd = LCD1602()
        AHT20Reader = AHT20(AHT20_1, AHT20_2)
        soilMoiReader = SoilMoistureSensor(SOIL_MOI)
        soilNPKReader = SoilNPKSensor()
        
        global current_selection, startCountFlag, soilMoi, atmTem, N, P, K, measuring, pumping, buzzing, ledON  
        current_selection = 0
        measuring, pumping, buzzing, ledON = False, False, False, False
        soilMoi, atmTem, N, P, K = 0, 0, 0, 0, 0
        measuringFlag = threading.Event()

        for pin in gpioPin:
            if pin == LED or pin == BUZZER or pin == PUMP:
                GPIO.setup(pin, GPIO.OUT)
            else:
                GPIO.setup(pin, GPIO.IN) 

        def move_selection_up():
            global current_selection            
            current_selection = (current_selection + 1) % len(vegetables)
            display_current_selection()  

        def move_selection_down():
            global current_selection
            current_selection = (current_selection - 1) % len(vegetables)
            display_current_selection()  

        def select_vegetable(lcd):
            global startCountFlag, measuring
            measuring = True 
            threading.Thread(target=startMeasure, args=(lcd,)).start()
        
        def display_current_selection():
            global measuring
            lcd.clear()
            lcd.set_cursor(0, 0)
            lcd.write_string("CHON LOAI RAU:")
            lcd.set_cursor(1, 0)
            lcd.write_string(f"> {vegetables[current_selection % len(vegetables)]}")

        def getDataFromAHT22():
            global atmTem, pumping
            while not measuringFlag.is_set() and not pumping:
                tem, hum = AHT20Reader.read()
                atmTem = tem
                time.sleep(5)
            print("stop getting atm tem")
        
        def getDataFromSoilMoistureSensor():
            global soilMoi, pumping, buzzing
            while not measuringFlag.is_set() and not pumping and not buzzing:
                soilMoi = soilMoiReader.read()
                time.sleep(5)
            print("stop getting soil moisture")
        
        def getDataFromNPKSensor():
            global N, P, K, ledON
            while not measuringFlag.is_set() and not ledON:
                N, P, K = SoilNPKSensor.read()
                time.sleep(10)
            print("stop getting NPK")
        
        def displayMeasuringState(lcd):
            global soilMoi, atmTem, N, P, K, buzzing, ledON
            while not measuringFlag.is_set() and not buzzing and not ledON:
                lcd.clear()
                lcd.set_cursor(0, 0)
                lcd.write_string(f"Hum: {soilMoi:.1f}%, Tem: {atmTem:.1f}°C")
                lcd.set_cursor(1, 0)
                lcd.write_string(f"N: {N:.2f}, P: {P:.2f}, K: {K:.2f} (g/kg)")
                time.sleep(1)
            print("Stop displaying sensors' data")

        def startPump():
            # Logic: when moisture is low, start pumping until the moisture is okay
            # When pumping, stop read random data from sensors

            global soilMoi, atmTem, pumping
            pumping = True
            moiLim = vegetablesInfo[str(current_selection)]["humidity"]
            temLim = vegetablesInfo["atmosphereTemperature"]
            GPIO.output(PUMP, GPIO.HIGH)

            # 1s +1 % moisture instead of reading from random data
            while soilMoi < moiLim[0] and pumping:
                soilMoi += 1
                print(f"Pumping, current moisture: {soilMoi}")
                time.sleep(1)       

            pumping = False
            GPIO.output(PUMP, GPIO.LOW)
            # Break before continuing reading random data
            time.sleep(1)
            threading.Thread(target=getDataFromAHT22).start()
            threading.Thread(target=getDataFromSoilMoistureSensor).start()

        def startBuzzer(lcd):
            # Logic: when moisture is high, start buzzing, draining water and displaying noti on LCD
            # If when buzzing, user push the OK button, all the above action will be terminated

            global buzzing, soilMoi
            buzzing = True
            print("Hi, im startbuzzing")
            moiLim = vegetablesInfo[str(current_selection)]["humidity"]
            threading.Thread(target=drainWater).start()

            # Start displaying the notification
            lcd.clear()
            lcd.set_cursor(0, 0)
            lcd.write_string("Độ ẩm cao! Xin hãy rút nước")

            # Turn on the buzzer
            GPIO.output(BUZZER, GPIO.HIGH)            

            while soilMoi > moiLim[1]:
                # Listen whether OK button is pushed or not
                if GPIO.input(BTN_OK) == GPIO.HIGH:
                    buzzing = False
                    break
            
            buzzing = False
            GPIO.output(BUZZER, GPIO.LOW)
            # Break before reading sensors' data
            time.sleep(1)
            threading.Thread(target=getDataFromSoilMoistureSensor).start()
            threading.Thread(target=displayMeasuringState, args=(lcd,)).start()
        
        def drainWater():
            global buzzing, soilMoi
            moiLim = vegetablesInfo[str(current_selection)]["humidity"]
            while soilMoi > moiLim[1] and buzzing:
                soilMoi -= 1
                print(f"Draining water, current moisture: {soilMoi}")
                time.sleep(1)
            print("Completed draining!")
            
        def startLED(lcd):
            # Logic: when N or P or K's amount is low, activate LED and display noti to LCD
            global N, P, K, ledON, buzzing, pumping
                
            ledON = True
            print(f"Hi, im {threading.current_thread().name}")
            NLim = vegetablesInfo[str(current_selection)]["N"]
            PLim = vegetablesInfo[str(current_selection)]["P"]
            KLim = vegetablesInfo[str(current_selection)]["K"]

            # threading.Thread(target=activateLED).start()
            GPIO.output(LED, GPIO.HIGH)

            # Start displaying the notification
            lcd.clear()
            lcd.set_cursor(0, 0)
            lcd.write_string("Cần bón thêm: ")
            lcd.set_cursor(1, 0)
            lcd.write_string(f"N: {(NLim[0] - N if NLim[0] > N else 0):.2f}, P: {(PLim[0] - P  if PLim[0] > P else 0):.2f}, K: {(KLim[0] - K  if KLim[0] > K else 0):.2f} (g/kg)")           

            while ledON and not pumping and not buzzing:
                # Listen whether OK button is pushed or not
                if GPIO.input(BTN_OK) == GPIO.HIGH:
                    ledON = False
                    break
            
            ledON = False
            GPIO.output(LED, GPIO.LOW)

            # Break before reading sensors' data
            time.sleep(1)
            threading.Thread(target=getDataFromNPKSensor).start()
            threading.Thread(target=displayMeasuringState, args=(lcd,)).start()

        def activateLED():
            global ledON, buzzing, pumping
            # print(f"Hi, im {threading.current_thread().name}")

            while ledON and not buzzing and not pumping:
                GPIO.output(LED, GPIO.HIGH)
                time.sleep(0.5)
                GPIO.output(LED, GPIO.LOW)
                time.sleep(0.5)

        def startMeasure(lcd):
            global measuring, N, P, K, soilMoi, atmTem, buzzing, pumping, ledON
            moiLim = vegetablesInfo[str(current_selection)]["humidity"]
            temLim = vegetablesInfo["atmosphereTemperature"]
            NLim = vegetablesInfo[str(current_selection)]["N"]
            PLim = vegetablesInfo[str(current_selection)]["P"]
            KLim = vegetablesInfo[str(current_selection)]["K"]

            print(vegetablesInfo[str(current_selection)])
            print(vegetablesInfo["atmosphereTemperature"])

            threading.Thread(target=getDataFromAHT22).start()
            threading.Thread(target=getDataFromSoilMoistureSensor).start()
            threading.Thread(target=getDataFromNPKSensor).start()
            threading.Thread(target=displayMeasuringState, args=(lcd,)).start()

            while measuring:
                # If there's not enough humidity, activate pump
                if soilMoi < moiLim[0] and atmTem >= temLim[0] and atmTem <= temLim[1]:
                    if not pumping:
                        threading.Thread(target=startPump).start()

                # If too much humidity, activate buzzer
                elif soilMoi > moiLim[1]:
                    if not buzzing:
                        time.sleep(1)
                        threading.Thread(target=startBuzzer, args=(lcd, )).start()
                
                # If there's not enough NPK, activate LED + display noti to LCD
                elif N < NLim[0] or P < PLim[0] or K < KLim[0]:
                    if not buzzing and not pumping and not ledON:
                        threading.Thread(target=startLED, args=(lcd,)).start()
        
        display_current_selection()

        # Main flow of the program
        while True:  
            if GPIO.input(BTN_RESET) == GPIO.HIGH:  
                current_selection = 0  
                if not measuringFlag.is_set():
                    measuringFlag.set()
                if measuring:
                    measuring = False
                pumping, buzzing, ledON = False, False, False
                soilMoi, atmTem, N, P, K = 0, 0, 0, 0, 0
                display_current_selection()  
                time.sleep(0.3)  
            
            if not measuring and GPIO.input(BTN_UP) == GPIO.HIGH:  
                move_selection_up()
                time.sleep(0.3)  
            elif not measuring and GPIO.input(BTN_DOWN) == GPIO.HIGH:  
                move_selection_down()
                time.sleep(0.3)  
            elif not measuring and GPIO.input(BTN_OK) == GPIO.HIGH:
                if measuringFlag.is_set():
                    measuringFlag.clear()
                select_vegetable(lcd)
                time.sleep(0.3)  

    except Exception as ex:
        traceback.print_exc()
    finally:
        GPIO.cleanup() 
   
Main()