from Simulator.EmulatorGUI import GPIO
import time
import traceback

def Main():

    try:
        output = [10, 9, 11, 5, 6, 13, 19, 26]

        GPIO.setmode(GPIO.BCM)

        GPIO.setwarnings(False)

        for i in output:
            GPIO.setup(i, GPIO.OUT)
                
        def printByte(num):
            status = bin(num)[2:].zfill(8)
            for i in range(len(status)):
                print(status[i])
                if status[i] == "1":
                    GPIO.output(output[i], GPIO.HIGH)
                else:
                    GPIO.output(output[i], GPIO.LOW)
            time.sleep(1)

        num = 0b00000000
        inverse34 = 0b00011000
        inverse25 = 0b00111100
        inverse16 = 0b01100110
        inverse07 = 0b11000011
        inverse_special = 0b10000001
        zero = 0b11111111
        left, right = 3, 4
        while True:
            printByte(num)
            num = num ^ inverse34
            printByte(num)
            num = num ^ inverse25
            printByte(num)
            num = num ^ inverse16
            printByte(num)
            num = num ^ inverse07
            printByte(num)

            num = 0b00000000
            printByte(num)

            num = num ^ inverse_special
            printByte(num)
            num = num ^ inverse07
            printByte(num)
            num = num ^ inverse16
            printByte(num)
            num = num ^ inverse25
            printByte(num)
            num = num ^ inverse34

        # while(True):
        #     if (GPIO.input(23) == False):
        #         GPIO.output(4,GPIO.HIGH)
        #         GPIO.output(17,GPIO.HIGH)
        #         time.sleep(1)

        #     if (GPIO.input(15) == True):
        #         GPIO.output(18,GPIO.HIGH)
        #         GPIO.output(21,GPIO.HIGH)
        #         time.sleep(1)

        #     if (GPIO.input(24) == True):
        #         GPIO.output(18,GPIO.LOW)
        #         GPIO.output(21,GPIO.LOW)
        #         time.sleep(1)

        #     if (GPIO.input(26) == True):
        #         GPIO.output(4,GPIO.LOW)
        #         GPIO.output(17,GPIO.LOW)
        #         time.sleep(1)



    except Exception as ex:
        traceback.print_exc()
    finally:
        GPIO.cleanup() #this ensures a clean exit



Main()