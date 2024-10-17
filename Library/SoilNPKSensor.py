import random
import time

class SoilNPKSensor:
    def __init__(self):
        pass

    def read(self):
        # Giả lập giá trị Nitơ, Phốt pho, Kali
        nitrogen = random.uniform(0.0, 200.0)  # Nồng độ Nitơ (mg/kg)
        phosphorus = random.uniform(0.0, 100.0)  # Nồng độ Phốt pho (mg/kg)
        potassium = random.uniform(0.0, 150.0)  # Nồng độ Kali (mg/kg)
        
        time.sleep(1)
        
        return nitrogen, phosphorus, potassium

def read_sensor():
    sensor = SoilNPKSensor()
    nitrogen, phosphorus, potassium = sensor.read()
    
    return {
        "Nitrogen (N)": nitrogen,
        "Phosphorus (P)": phosphorus,
        "Potassium (K)": potassium
    }

# Ví dụ sử dụng
# if __name__ == "__main__":
#     for _ in range(5):  # Đọc 5 lần
#         data = read_sensor()
#         print(f"Data: {data}")
