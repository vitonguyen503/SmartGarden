# Viết chương trình bằng Python giám sát thông số môi trường:

# Mỗi thông số cung cấp bao gồm: nhiệt độ, độ ẩm, hướng gió, tốc độ gió
# Lưu trữ các mục thông số thành danh sách
# Hiển thị giá trị hiện tại, cao nhất, thấp nhất, trung bình của nhiệt độ, độ ẩm, tốc độ gió
# Đưa ra cảnh báo ngay khi nhiệt độ, độ ẩm, tốc độ gió có thay đổi vượt ngưỡng đặt trước (ngưỡng cảnh báo)
# Vẽ biểu đồ cho thấy biến thiên các thông số (dùng đồ họa hoặc ký tự đại diện điểm đồ thị)
# Lưu trữ dữ liệu ra tệp tin khi được yêu cầu hoặc tự động trước khi dừng chương trình
# Nạp lại dữ liệu mỗi khi chương trình chạy

import matplotlib.pyplot as plt
import csv
import math
import time
import statistics

def displayInfo(dataList, statistic):
    print(f"Temperature:    {dataList[0][len(dataList[0]) - 1]}, max: {statistic[0][0]}, min: {statistic[0][1]}, mid: {statistic[0][2] * 1.0 / len(dataList[0])}")
    print(f"Humidity:       {dataList[1][len(dataList[0]) - 1]}, max: {statistic[1][0]}, min: {statistic[1][1]}, mid: {statistic[1][2] * 1.0 / len(dataList[0])}")
    print(f"Wind direction: {dataList[2][len(dataList[0]) - 1]}, max: {statistic[2][0]}, min: {statistic[2][1]}, mid: {statistic[2][2] * 1.0 / len(dataList[0])}")
    print(f"Wind speed:     {dataList[3][len(dataList[0]) - 1]}, max: {statistic[3][0]}, min: {statistic[3][1]}, mid: {statistic[3][2] * 1.0 / len(dataList[0])}")
    print()

def showAlert(row):
    if int(row[0]) >= limTemperature:
        print("High temperature!")
    if int(row[1]) >= limHumidity:
        print("High humidity!")
    if int(row[3]) >= limWindSpeed:
        print("High wind speed!")
    
def getMinMaxMean(data):
    return [max(data), min(data), statistics.mean(data)]

def getDataFromFile(fileName):
    data_list = []
    statistic = [[], [], [], []]

    with open(fileName, 'r') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader) 
        
        for row in csv_reader:
            data_list.append([int(value) for value in row])

        for i in range(4):
            statistic[i] = getMinMaxMean(data_list[i])

    return data_list, statistic

def getNewInput(filename, data_list, statistic):
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader) 
        
        for row in csv_reader:
            showAlert(row)
            for i in range(len(row)):
                data_list[i].append(int(row[i]))

            for i in range(4):
                statistic[i] = getMinMaxMean(data_list[i])

            displayInfo(data_list, statistic)
            time.sleep(1)
    return data_list, statistic

def drawDiagram(data):
    plt.plot(data[0], label='Temperature')
    plt.plot(data[1], label='Humidity')
    plt.plot(data[2], label='Wind Direction')
    plt.plot(data[3], label='Wind Speed')

    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.legend()
    plt.show()

def saveData(data, fileName):
    with open(fileName, 'w', newline='') as file:
        file.write('Temperature,Humidity,Wind_Direction,Wind_Speed\n')
        writer = csv.writer(file)
        writer.writerows(data)

limTemperature, limHumidity, limWindSpeed = 50, 50, 50

data, statistic = getDataFromFile("data.csv")

data, statistic = getNewInput("input.csv", data, statistic)

print()

drawDiagram(data)

saveData(data, "data.csv")
print("Save data successfully!")