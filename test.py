import re
import time

# # 1, 2
# def get_8_byte_number():
#     while True:
#         value = input("Enter a 8 byte number: ")
#         if(re.match(r"^[01]{8}$", value) is not None):
#             return value
#         print("Please enter a valid 8 byte number!")

# print("1, 2: ")
# input = get_8_byte_number()
# print(input)

# # 3
# def replace_at_index(string, index, replacement):
#     if index < 0 or index >= len(string):
#         raise ValueError("Index out of range")
#     return string[:index] + replacement + string[index + 1:]

# print("3: ")
# while True:
#     pos = input.find("1")
#     if pos == -1:
#         break
#     input = replace_at_index(input, pos, "0")
#     print(input)
#     time.sleep(1)

# 4
print("4: ")

def printByte(num):
    print(bin(num)[2:].zfill(8))
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