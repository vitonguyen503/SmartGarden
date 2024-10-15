from Simulator.pnhLCD1602 import LCD1602
import pygame
import time 
if __name__ == "__main__":
    lcd = LCD1602()
    
    try:
        while True:
            lcd.clear()
            lcd.write_string("TIEU DE VAN BAN")
            lcd.set_cursor(1, 0)  # Đặt con trỏ ở dòng thứ 2
            lcd.write_string("9999999999999989")
            time.sleep(1)

        # Hiển thị cả hai dòng cùng lúc
            # pygame.time.delay(3000)  # Hiển thị trong 3 giây
            lcd.backlight_off()
            # pygame.time.delay(1000)
            lcd.backlight_on()
            # pygame.time.delay(1000)
            lcd.home()
            # pygame.time.delay(2000)
    finally:
        lcd.close()