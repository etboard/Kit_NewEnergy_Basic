# *****************************************************************************************
# FileName     : NewEnergy_Basic
# Description  : 신재생에너지 코딩 키트 (기본)
# Author       : 손정인
# CopyRight    : (주)한국공학기술연구원(www.ketri.re.kr)
# Created Date : 2022.02.08
# Reference    :
# Modified     : 2022.07.11 : Add 전압 보정 변수
# Modified     : 2022.12.21 : YSY : 변수 명명법 통일
# Modified     : 2023.03.14 : PEJ : 주석 및 코드 길이 수정

# *****************************************************************************************

# import
import time
from machine import Pin, ADC
from ETboard.lib.pin_define import *
from ETboard.lib.OLED_U8G2 import *              # OLED 제어를 위한 라이브러리 불러오기

#------------------------------------------------------------------------------------------
# ETBoard 핀번호 설정
#------------------------------------------------------------------------------------------
# global variable
oled = oled_u8g2()

solar_pin = ADC(Pin(A3))                         # 태양광 발전량 측정 센서
wind_pin  = ADC(Pin(A5))                         # 풍력 발전량 측정 센서

text1 = [0] * 31
text2 = [0] * 31

c_value = 0.00806;                               # 전압 보정 변수 선언 (3.3v / 4096)


#==========================================================================================
# setup
#========================================================================================== 
def setup() :
    solar_pin.atten(ADC.ATTN_11DB)               # 태양광 발전량 측정 센서 입력 모드 설정
    wind_pin.atten(ADC.ATTN_11DB)                # 풍력 발전량 측정 센서  입력 모드 설정


#==========================================================================================
# main loop
#==========================================================================================
def loop() :
    #--------------------------------------------------------------------------------------
    # 태양광 발전량 측정 센서로 태양광 발전 전압 구하기
    #--------------------------------------------------------------------------------------  
    solar_value = solar_pin.read()               # 태양광 발전량 측정값 저장
    solar_power = solar_value * c_value          # 태양광 발전량 전압 계산
    
    print("태양광 센서 : ", solar_power, "V")

    #--------------------------------------------------------------------------------------
    # 풍력 발전량 측정 센서로 풍력 발전 전압 구하기
    #--------------------------------------------------------------------------------------
    wind_value = wind_pin.read()                 # 풍력 발전량 측정값 저장
    wind_power = wind_value * c_value            # 풍력 발전량 전압 계산

    print(" 풍력  센서 : ", wind_power, "V")
    print("---------------------");
    
    #--------------------------------------------------------------------------------------
    # OLED 텍스트 표시
    #--------------------------------------------------------------------------------------
    text1 = "Solar: %d" %(solar_power) + "V"         
    text2 = "Wind: %d" %(wind_power) + "V"

    oled.clear()
    oled.setLine(1, "* ECO Energy *")            # OLED 첫 번째 줄 : 시스템 이름
    oled.setLine(2, text1)                       # OLED 두 번째 줄 : 태양광 발전 전압
    oled.setLine(3, text2)                       # OLED 세 번째 줄 : 풍력 발전 전압
    oled.display()
    
    time.sleep(0.5)
    

if __name__ == "__main__" :
    setup()
    while True :
        loop()

# =========================================================================================
#
#  (주)한국공학기술연구원 http://et.ketri.re.kr
#
# =========================================================================================