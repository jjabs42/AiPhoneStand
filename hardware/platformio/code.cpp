#include <Arduino.h>
#include <WiFiS3.h> 

const char* ssid = "";
const char* pw = "";

//connects to wifi
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  delay(1000);

  WiFi.begin(ssid, pw);
  Serial.println("\nConnecting...");

  while(WiFi.status() != WL_CONNECTED)
  {
    Serial.println(".");
    delay(1000);
  }


  delay(10000);
  Serial.println("\n Connected to network");
  Serial.println("\n NetworkIP is");
  Serial.println(WiFi.localIP());
  
}

void loop() {
  // put your main code here, to run repeatedly:
}
