#include <Arduino.h>
#include <WiFiS3.h> 
#include <Servo.h>
#include <WebSocketsClient.h>
#include <stdarg.h>
#include <stdio.h>
#include <ArduinoJson.h>
#include <list>



WebSocketsClient webSocket;


//constants
const char* ssid = "";
const char* pw = "";
const int pin3 = 3;
const int pin5 = 5;

//GLOBALS
//___________________________________________________________________________________________________________//


//servo inits
Servo myservo1;
Servo myservo2;

//___________________________________________________________________________________________________________//











//basically a function that each determines the state of the socket
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
    
    
    //if text is received  
    case WStype_TEXT:{
    
    //json conversion
    JsonDocument doc;
    DeserializationError error = deserializeJson(doc, payload, length);
    if (error) {
        Serial.println("JSON parsing failed");
        break;
    }

    if (doc["xMotor"] && doc["yMotor"]){
      myservo1.write((int)doc["xMotor"]);
      myservo2.write((int)doc["xMotor"]);
    }


      // send message to server
      break;
  }
}
}


//when arduino is turned on
void setup() {

  myservo1.attach(pin3);
  myservo2.attach(pin5);
 

  //wifi connection stuff
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


//sets the two to match the position
void loop() {
webSocket.loop();


}
