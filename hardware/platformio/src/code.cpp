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

//GLOBALS
//___________________________________________________________________________________________________________//



//determines if a message is available
volatile bool messAv = false;


//servo inits
Servo myservo1;
Servo myservo2;


//x motor moves left to right, y moves up and down
int currentXMotor;
int currentYMotor;

//___________________________________________________________________________________________________________//


//calibration config
void calibrate_selfie(JsonDocument& direction) {
  int degrees = (int)direction["degrees"];
  Serial.println(degrees);
  Serial.println((String) direction["calibrationLR"]);

  //conditionals to check where to move
  if ((String)direction["calibrationLR"] == "l"){
    for(int i=1; i < degrees; i++){
    myservo1.write(currentXMotor - i);
    
    delay(10);
    }
    currentXMotor -= degrees;
  }

  else if (direction["calibrationLR"] == "r"){
    for(int i=1; i < degrees; i++){
    myservo1.write(currentXMotor + i);
    
    delay(10);
    }
    currentXMotor += degrees;

  }

  if (direction["calibrationUD"] == "u"){
   for(int i=1; i < degrees; i++){
    myservo2.write(currentYMotor + i);
    
    delay(10);
    }
    currentYMotor += degrees;

  }

  else if (direction["calibrationUD"] == "d"){
    for(int i=1; i < degrees; i++){
    myservo2.write(currentYMotor - i);
    
    delay(10);
    }
    currentYMotor -= degrees;

        }
      }

void calibrate_environment(JsonDocument& direction){

  int degrees = (int)direction["degrees"];
  Serial.println(degrees);
  Serial.println((String) direction["calibrationLR"]);

  //conditionals to check where to move
  if ((String)direction["calibrationLR"] == "l"){
    for(int i=1; i < degrees; i++){
    myservo1.write(currentXMotor + i);
    
    delay(10);
    
    }
    currentXMotor += degrees;


  }

  else if (direction["calibrationLR"] == "r"){
    for(int i=1; i < degrees; i++){
    myservo1.write(currentXMotor - i);
    
    delay(10);
    }
    currentXMotor -= degrees;

  }

  if (direction["calibrationUD"] == "u"){
   for(int i=1; i < degrees; i++){
    myservo2.write(currentYMotor - i);
    
    delay(10);
    }
    currentYMotor -= degrees;

  }

  else if (direction["calibrationUD"] == "d"){
    for(int i=1; i < degrees; i++){
    myservo2.write(currentYMotor + i);
    
    delay(10);
    }
    currentYMotor += degrees;
        }

}










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

      

      if(doc["move"]){
        int i = doc["move"];
        myservo1.write(i);
        myservo2.write(i);
        currentXMotor = i;
        currentYMotor = i;
      }
  

      //starts calibration
      if (doc["type"] == "calibration")
      {
        Serial.println((String)doc["type"]);
        myservo1.write(90);
        myservo2.write(90);
        currentXMotor = 90;
        currentYMotor = 90;
        delay(1000);

        if (doc["facingMode"] == "user"){
          calibrate_selfie(doc);
        }

        else if(doc["facingMode"] == "environment"){
          calibrate_environment(doc);
        }
      }



      
      
      if (doc["type"] == "tracking")
    {
      Serial.print("Received Tracking Info:");
      myservo1.write(currentXMotor + (int)doc["xMotor"]);
      myservo2.write(currentYMotor + (int)doc["yMotor"]);
      currentXMotor += (int)doc["xMotor"];
      currentYMotor += (int)doc["yMotor"];
      delay(2000);
      
     
      messAv = true;
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
  currentXMotor = 90;
  currentYMotor = 90;
}


//sets the two to match the position
void loop() {
webSocket.loop();


}
