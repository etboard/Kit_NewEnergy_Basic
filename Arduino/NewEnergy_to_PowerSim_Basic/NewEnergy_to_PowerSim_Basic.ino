/******************************************************************************************
 * FileName     : NewEnergy_to_PowerSim_Basic
 * Description  : 신재생에너지 코딩 키트, 가상 전력 변환(기본)
 * Author       :
 * CopyRight    : (주)한국공학기술연구원(www.ketri.re.kr)
 * Warning      : Arduino IDE에서 u8g2 라이브러리를 추가해서 컴파일 해야힘
 * Created Date :
 * Modified     : 2022.01.12 : SCS : 소스 크린징
 * Modified     : 2022.07.11 : SCS : change baud rate 9600 -> 115200 and c_Value
 * Modified     : 2022.10.03 : SCS : support arduino uno with ET-Upboard
 * Modified     : 2022.12.19 : YSY : char_value -> text,
 * Modified     : 2023.03.14 : PEJ : 주석 및 코드 길이 수정
 * Modified     : 2024.10.06 : SCS : 에너지 변환
******************************************************************************************/

// OLED 제어를 위한 라이브러리 불러오기
#include "oled_u8g2.h"
OLED_U8G2 oled;

//-----------------------------------------------------------------------------------------
// ETBoard 핀번호 설정
//-----------------------------------------------------------------------------------------
#include "pins_arduino.h"                            // support arduino uno with ET-Upboard

const int solar_pin = A3;                            // 태양광 발전량 측정 센서
const int wind_pin  = A5;                            // 풍력 발전량 측정 센서

const double c_value = 0.00806;                      // 전압 보정 변수 선언 (3.3v / 4096)

int led_red = D2;                                    // PWM용 Motor-L
int led_blue = D4;                                   // PWM용 Motor-R

//=========================================================================================
void setup()
//=========================================================================================
{
    Serial.begin(115200);                            // 시리얼통신 준비
    oled.setup();                                    // OLED 셋업

    pinMode(solar_pin, INPUT);                       // 태양광 발전량 측정 센서 입력모드 설정
    pinMode(wind_pin, INPUT);                        // 풍력 발전량 측정 센서  입력모드 설정

    ledcAttachPin(led_red, 0);                       // PWM 채널 0번 설정
    ledcSetup(0, 5000, 8);
    ledcAttachPin(led_blue, 1);                      // PWM 채널 1번 설정
    ledcSetup(1, 5000, 8);
} 

//=========================================================================================
void solar_convert(int value) 
//=========================================================================================
{
  value = value / 1.5;
  if (value >= 1023) {
    value = 1023;
  }
  if (value >= 30) {
    value = 1023;
  }
  ledcWrite(0, value);  // Solar PWM 출력
}

//=========================================================================================
void wind_convert(int value) 
//=========================================================================================
{
  value = value / 4;
  if (value >= 1023) {
    value = 1023;
  }
  ledcWrite(1, value);  // Wind PWM 출력
}

//=========================================================================================
void loop()
//=========================================================================================
{    
    //-------------------------------------------------------------------------------------  
    // 태양광 발전량 측정 센서로 태양광 발전 전압 구하기
    //-------------------------------------------------------------------------------------
    int solar_value = analogRead(solar_pin);         // 태양광 발전량 측정값 저장
    int solar_power = solar_value * c_value;         // 태양광 발전량 전압 계산
    
    Serial.print("태양광 센서 : ");
    Serial.print(solar_power);
    Serial.println("V");
    solar_convert(solar_value);

    
    //-------------------------------------------------------------------------------------
    // 풍력 발전량 측정 센서로 풍력 발전 전압 구하기
    //-------------------------------------------------------------------------------------
    int wind_value = analogRead(wind_pin);           // 풍력 발전량 측정값 저장
    int wind_power = wind_value * c_value;           // 풍력 발전량 전압 계산
    
    Serial.print("  풍력 센서 : ");
    Serial.print(wind_power);
    Serial.println("V");
    wind_convert(wind_value);
    Serial.println("---------------------");

    //-------------------------------------------------------------------------------------
    // OLED 텍스트 표시
    //-------------------------------------------------------------------------------------
    char text1[32] = "Solar: ";                      // text1 태양광 발전 전압 표시
    char value1[32];
    String str1 = String(solar_power, DEC);
    str1.toCharArray(value1,6);
    strcat(text1, value1);
    strcat(text1, " V ");

    char text2[32] = "Wind: ";                       // text2 풍력 발전 전압 표시
    char value2[32];
    String str2 = String(wind_power, DEC);
    str2.toCharArray(value2, 6);
    strcat(text2, value2);
    strcat(text2, " V ");

    oled.setLine(1,"* ECO Energy *");                // OLED 첫 번째 줄 : 시스템 이름
    oled.setLine(2,text1);                           // OLED 두 번째 줄 : 태양광 발전 전압
    oled.setLine(3,text2);                           // OLED 세 번째 줄 : 풍력 발전 전압
    oled.display(); 

    delay(500);
}

//=========================================================================================
//
// (주)한국공학기술연구원 http://et.ketri.re.kr
//
//=========================================================================================
