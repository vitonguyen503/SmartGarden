import random
import time

class SoilMoistureSensor:
    def __init__(self, digital_pin):
        self.digital_pin = digital_pin

    def read(self):
        moisture = 40 # random.uniform(40.0, 95.0)
        return moisture

def readMoistureSensor(digital_pin):
    sensor = SoilMoistureSensor(digital_pin)
    return sensor.read()

# # Sử dụng mã giả lập
# digital_pin = 17  # Ví dụ GPIO 17 trên Raspberry Pi
# moisture, digital_signal = readMoistureSensor(digital_pin)

# # In kết quả
# print(f"Độ ẩm đất: {moisture:.2f} %")
# print(f"Tín hiệu số (Digital Signal): {'HIGH' if digital_signal else 'LOW'}")
