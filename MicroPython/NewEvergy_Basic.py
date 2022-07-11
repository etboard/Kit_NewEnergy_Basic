# ******************************************************************************************
# FileName     : NewEnergy_Basic
# Description  : 신재생에너지 코딩 키트 (기본)
# Author       : 손정인
# CopyRight    : (주)한국공학기술연구원(www.ketri.re.kr)
# Created Date : 2022.02.08
# Reference    :
# Modified     : 2022.07.11 : Add 전압 보정 변수
# ******************************************************************************************

# import
import time
from machine import Pin, ADC
from ETboard.lib.pin_define import *
from ETboard.lib.OLED_U8G2 import *                  # OLED 제어를 위한 라이브러리 불러오기

C_VALUE = 0.000806;                                  # 전압 보정 변수 선언 (3.3v / 4096)

# global variable
oled = oled_u8g2()
solar = ADC(Pin(A3))                                 # 태양광 발전량 측정 센서
windturbine = ADC(Pin(A5))                           # 풍력 발전량 측정 센서
text1 = [0] * 31
text2 = [0] * 31

# setup
def setup() :
    solar.atten(ADC.ATTN_11DB)                       # 태양광 발전량 측정 센서 입력 모드 설정
    windturbine.atten(ADC.ATTN_11DB)                 # 풍력 발전량 측정 센서  입력 모드 설정

#main loop
def loop() :
    display_oled()
    time.sleep(1)

def display_oled() :
    solar_voltage_value = solar.read()               # 태양광 발전량 측정값 저장
    windturbine_voltage_value = windturbine.read()   # 풍력 발전량 측정값 저장

    print("태양광 센서 : ", solar_voltage_value)
    print("풍력   센서 : ", windturbine_voltage_value)
    print("-------------------");
    
    text1 = "S : {:.2f} V".format(solar_voltage_value*C_VALUE)
    text2 = "W : {:.2f} V".format(windturbine_voltage_value*C_VALUE)

    oled.clear()
    oled.setLine(1, "* ECO Energy *")                # OLED 첫 번째 줄 : 시스템 이름
    oled.setLine(2, text1)                           # OLED 두 번째 줄 : 태양광 발전 전압
    oled.setLine(3, text2)                           # OLED 세 번째 줄 : 풍력   발전 전압
    oled.display()

if __name__ == "__main__" :
    setup()
    while True :
        loop()

# ==========================================================================================
#
#  (주)한국공학기술연구원 http://et.ketri.re.kr
#
# ==========================================================================================
