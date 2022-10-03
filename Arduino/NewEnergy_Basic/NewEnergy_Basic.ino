/******************************************************************************************
 * FileName     : NewEnergy_Basic
 * Description  : 신재생에너지 코딩 키트 (기본)
 * Author       :
 * CopyRight    : (주)한국공학기술연구원(www.ketri.re.kr)
 * Warning      : Arduino IDE에서 u8g2 라이브러리를 추가해서 컴파일 해야힘
 * Created Date :
 * Modified     : 2022.01.12 : SCS : 소스 크린징
 * Modified     : 2022.07.11 : SCS : change baud rate 9600 -> 115200 and c_Value
 * Modified     : 2022.10.03 : SCS : support arduino uno with ET-Upboard
******************************************************************************************/

//==========================================================================================
// Include & definition
//==========================================================================================

// OLED 제어를 위한 라이브러리 불러오기
#include "oled_u8g2.h"
OLED_U8G2 oled;

// 전압 보정 변수 선언
const double c_Value = 0.000806;  // (3.3v / 4096)

//==========================================================================================
void setup()
//==========================================================================================
{
  Serial.begin(115200);
  oled.setup();
}

//==========================================================================================
void loop()
//==========================================================================================
{
  display_oled();
  delay(1000);
}

//==========================================================================================
void display_oled()
//==========================================================================================
{
  // 태양광 발전량 측정 센서
  int solar_voltage_Value = analogRead(A3);
  Serial.print("태양광 센서 : ");
  Serial.println(solar_voltage_Value);

  // OLED 텍스트 표시
  float float_value = solar_voltage_Value * c_Value;
  String str_value = "S: " + String(float_value, 2) + " V";
  char char_value1[16];  
  str_value.toCharArray(char_value1,11);

  // 풍력 발전량 측정 센서
  int windturbine_voltage_Value = analogRead(A5);
  Serial.print("  풍력 센서 : ");
  Serial.println(windturbine_voltage_Value);
  Serial.println("---------------------");

  // OLED 텍스트 표시
  float_value = windturbine_voltage_Value * c_Value;
  str_value = "W: " + String(float_value, 2) + " V";
  char char_value2[16];  
  str_value.toCharArray(char_value2,11);

  oled.setLine(1,"* ECO Energy *");    // OLED 첫 번째 줄 : 시스템 이름
  oled.setLine(2,char_value1);         // OLED 두 번째 줄 : 태양광 발전 전압
  oled.setLine(3,char_value2);         // OLED 세 번째 줄 : 풍력   발전 전압
  oled.display();
}

//=========================================================================================
//
// (주)한국공학기술연구원 http://et.ketri.re.kr
//
//=========================================================================================
