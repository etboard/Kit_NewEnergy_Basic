# ******************************************************************************************
# FileName     : 03._variable_resistance_sensor_led_fade
# Description  : 가변저항 값에 따라 빨강 LED의 밝기 조절 해보기
#                가변저항 값을 쉘에 출력
# Author       : 이승찬
# Created Date : 2021.08.13
# Reference    :
# Modified     : 2022 : SJI : 헤더 수정, 주석 수정
# Modified     : 2023.10.25 : PEJ : PWM 함수 사용 방법 수정
# ******************************************************************************************


# import
import time
from machine import ADC, Pin, PWM
from ETboard.lib.pin_define import *


# global variable
sensor = ADC(Pin(A0))                       # 가변저항 핀 지정
led_red = Pin(D4)                           # 빨강 LED 핀 지정
pwm2 = PWM(led_red)                         # PWM 생성
pwm2.freq(5000)

# setup
def setup():
    sensor.atten(ADC.ATTN_11DB)             # 가변저항 입력 모드 설정
    led_red.init(Pin.OUT)                   # 빨강 LED 출력 모드 설정
    pwm2.deinit()                           # 기존 PWM 재설정
    pwm2.init()                           # 기존 PWM 재설정


# main loop
def loop():
    sensor_result = int(sensor.read()/2.5 )       # 가변저항 센서 값 저장
    print(sensor_result)

    # 가변저항값을 이용하여 빨강 LED의 밝기를 조절
    #pwm2 = PWM(led_red, 500, duty = int(sensor_result))
    pwm2.duty(sensor_result)
    #time.sleep_ms(20)
    #time.sleep(0.1)                         # 0.1초 기다리기


if __name__ == "__main__":
    setup()
    while True:
        loop()


# ==========================================================================================
#
#  (주)한국공학기술연구원 http://et.ketri.re.kr
#
# ==========================================================================================
