#include <Arduino.h>
#include <WiFiS3.h> 
#include <Servo.h>
#include <WebSocketsClient.h>
#include <stdarg.h>
#include <stdio.h>
#include <ArduinoJson.h>



WebSocketsClient webSocket;


//constants
const char* ssid = "";
const char* pw = "";
const int pin3 = 3;
const int pin5 = 5;


Servo myservo1;
Servo myservo2;

float lastCommand[2];
volatile bool messAv = false;
String previous = "";

void webSocketEvent(WStype_t type, uint8_t *payload, size_t length) {

  switch (type) {
    case WStype_DISCONNECTED:
      Serial.println("[WSc] Disconnected!");
      break;
    case WStype_CONNECTED:
      Serial.println("[WSc] Connected!");
      

      // send message to server when Connected
      webSocket.sendTXT("Connected");
      break;
    case WStype_TEXT:{
    
    //json conversion
    JsonDocument doc;

    DeserializationError error = deserializeJson(doc, payload, length);

    if (error) {
        Serial.println("JSON parsing failed");
        break;
    }



      Serial.print("[WSc] get text:");
      float motors[2];
      
      motors[0] = doc[0];
      motors[1] = doc[1];

      lastCommand[0] = motors[0];
      lastCommand[1] = motors[1];
      
      messAv = true;
      // send message to server
      // webSocket.sendTXT("message here");
      break;
       }
    case WStype_BIN:
      // send data to server
      // webSocket.sendBIN(payload, length);
      break;
    case WStype_ERROR:
    case WStype_FRAGMENT_TEXT_START:
    case WStype_FRAGMENT_BIN_START:
    case WStype_FRAGMENT:
    
      break;
  }
}


void setup() {

  myservo1.attach(pin3);
  myservo2.attach(pin5);
 

  Serial.begin(115200);
  delay(1000);

  WiFi.begin(ssid, pw);
  Serial.println("\nConnecting...");

  while(WiFi.status() != WL_CONNECTED)
  {
    Serial.println(".");
    delay(1000);
  }


  delay(5000);
  Serial.println("\n Connected to network");
  Serial.println("\n NetworkIP is ");
  Serial.println(WiFi.localIP());

  webSocket.begin("192.168.68.62", 5556, "/stream");
  

  webSocket.onEvent(webSocketEvent);
  

  // try ever 5000 again if connection has failed
  webSocket.setReconnectInterval(5000);
  myservo1.write(90);
  myservo2.write(90);
}

int bott = 90;
int top = 90;

void loop() {
webSocket.loop();

if (messAv == true){
  

  
bott -= lastCommand[0];
top -= lastCommand[1];
bott = constrain(bott, 0, 180);
top = constrain(top, 0, 180);
Serial.println(bott);
Serial.println(top);
messAv = false;
  
  
}

myservo1.write((int) bott);
myservo2.write((int) top);

}
