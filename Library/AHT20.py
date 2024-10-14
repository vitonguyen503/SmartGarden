import random
import time

# Read atmosphere's temperature and humidity
class AHT20:
    def __init__(self, SDA_pin, SCL_pin):
        self.SDA_pin = SDA_pin
        self.SCL_pin = SCL_pin

    def read(self):
        temperature = random.uniform(20.0, 40.0)  
        humidity = random.uniform(60.0, 95.0)
        
        time.sleep(1)
        
        return temperature, humidity

def readSensor(SDA_pin, SCL_pin):
    sensor = AHT20(SDA_pin, SCL_pin)
    return sensor.read()

# # Hàm chính để chạy giả lập
# def main():
    
#     # Đọc dữ liệu từ cảm biến giả lập mỗi 2 giây
#     while True:
#         # Đọc nhiệt độ và độ ẩm từ cảm biến giả lập
#         temp, hum = readSensor(3, 5)
        
#         # Hiển thị kết quả
#         print(f"Nhiệt độ: {temp:.2f} °C, Độ ẩm: {hum:.2f} %")
        

# # Chạy chương trình giả lập
# if __name__ == "__main__":
#     main()
