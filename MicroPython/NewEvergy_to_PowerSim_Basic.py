# *****************************************************************************************
# FileName     : NewEnergy_to_PowerSim_Basic
# Description  : 신재생에너지 코딩 키트 (기본)
# Author       : 손정인
# CopyRight    : (주)한국공학기술연구원(www.ketri.re.kr)
# Created Date : 2022.02.08
# Reference    :
# Modified     : 2022.07.11 : Add 전압 보정 변수
# Modified     : 2022.12.21 : YSY : 변수 명명법 통일
# Modified     : 2023.03.14 : PEJ : 주석 및 코드 길이 수정
# Modified     : 2024.10.06 : SCS : 에너지 변환
# Modified     : 2024.10.13 : SCS : Clean Code
# *****************************************************************************************

# import
import time
from machine import Pin, ADC, PWM
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

pwm1 = PWM(Pin(D2))                              # PWM 생성
pwm2 = PWM(Pin(D4))                              # PWM 생성

#==========================================================================================
# setup
#========================================================================================== 
def setup() :
    solar_pin.atten(ADC.ATTN_11DB)               # 태양광 발전량 측정 센서 입력 모드 설정
    wind_pin.atten(ADC.ATTN_11DB)                # 풍력 발전량 측정 센서  입력 모드 설정
    
    pwm1.deinit()                                # 기존 PWM 재설정
    pwm2.deinit()                                # 기존 PWM 재설정
    pwm1.init()
    pwm2.init()
    pwm1.freq(5000)
    pwm1.duty(0)
    pwm2.freq(5000)
    pwm2.duty(0)
    pass

def solar_convert(value):    
    value = int(value/1.5)
    if (value >= 1023):
        value = 1023
    pwm1.duty(value)
    
def wind_convert(value):    
    value = int(value/4)
    if (value >= 1023):
        value = 1023
    pwm2.duty(value)    
    
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
    solar_convert(solar_value)    

    #--------------------------------------------------------------------------------------
    # 풍력 발전량 측정 센서로 풍력 발전 전압 구하기
    #--------------------------------------------------------------------------------------
    wind_value = wind_pin.read()                 # 풍력 발전량 측정값 저장
    wind_power = wind_value * c_value            # 풍력 발전량 전압 계산

    print(" 풍력  센서 : ", wind_power, "V")    
    wind_convert(wind_value)    
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
    
    #time.sleep(0.05)
    

if __name__ == "__main__" :
    setup()
    while True :
        loop()

# =========================================================================================
#
#  (주)한국공학기술연구원 http://et.ketri.re.kr
#
# =========================================================================================