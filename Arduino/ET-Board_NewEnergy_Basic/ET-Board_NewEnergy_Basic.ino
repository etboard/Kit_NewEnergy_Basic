/******************************************************************************************
 * Author      : (주)한국공학기술연구원
 * Program ID  : eco_energy
 * Description : 신재생에너지 코딩
******************************************************************************************/

//=================================================================================
// Include & definition
//=================================================================================

// OLED 제어를 위한 라이브러리 불러오기
#include "oled_u8g2.h"
OLED_U8G2 oled;

// 전압 보정 변수 선언
const double c_Value = 0.001221245421;

//================================================================
void setup() 
//================================================================
{ 
  Serial.begin(9600);
  oled.setup();
}

//================================================================
void loop() 
//================================================================
{  
  display_oled();  
  delay(1000);
}


//================================================================
void setup_oled()
//================================================================
{
// OLED 통신핀 기능 설정
  pinMode(SDA, INPUT);  
  pinMode(SCL, INPUT);  
}


//================================================================
void display_oled()
//================================================================
{
  // 태양광 발전량 측정 센서
  int solar_voltage_Value = analogRead(A3);
  Serial.print("태양광 센서 : ");
  Serial.println(solar_voltage_Value);

  // OLED 텍스트 표시
  char text1[32] = "S: ";
  char value1[32];   
  String str = String(solar_voltage_Value*c_Value, DEC);
  str.toCharArray(value1,6);
  strcat(text1,value1);
  strcat(text1," V");

  // 풍력 발전량 측정 센서
  int windturbine_voltage_Value = analogRead(A5);
  Serial.print(" 풍력 센서 : ");
  Serial.println(windturbine_voltage_Value);
  Serial.println("---------------------");

  // OLED 텍스트 표시
  char text2[32] = "W: ";
  char value2[32];    
  String str2 = String(windturbine_voltage_Value*c_Value, DEC);
  str2.toCharArray(value2,6);
  strcat(text2,value2);
  strcat(text2," V");

  oled.setLine(1,"* ECO Energy *");    // OLED 첫 번째 줄 : 시스템 이름
  oled.setLine(2,text1);               // OLED 두 번째 줄 : 태양광 발전량
  oled.setLine(3,text2);               // OLED 세 번째 줄 : 풍력 발전량
  oled.display();
}

//=========================================================================================
//                                                    
// (주)한국공학기술연구원 http://et.ketri.re.kr       
//                                                    
//=========================================================================================
