import random
import time

class SoilNPKSensor:
    def __init__(self):
        pass

    def read():
        # Giả lập giá trị Nitơ, Phốt pho, Kali
        nitrogen = random.uniform(0.2, 1)  # Nồng độ Nitơ (g/kg)
        phosphorus = random.uniform(0.2, 0.5)  # Nồng độ Phốt pho (g/kg)
        potassium = random.uniform(0.2, 0.5)  # Nồng độ Kali (g/kg)
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
