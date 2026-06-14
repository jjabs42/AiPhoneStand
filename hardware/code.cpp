#include <Arduino.h>

void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);      
}

void dot(){
  digitalWrite(LED_BUILTIN, HIGH);
  delay(500);
  digitalWrite(LED_BUILTIN, LOW);
  delay(500);
}

void dash(){
  digitalWrite(LED_BUILTIN, HIGH);
  delay(1500);
  digitalWrite(LED_BUILTIN, LOW);
  delay(500);
}

void space(){
  digitalWrite(LED_BUILTIN, LOW);
  delay(2000);
}

void loop(){
  dot();
  dot();
  dot();
  dash();
  space();
  dot(); dash(); dot(); space();
}