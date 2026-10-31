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

//we need to store the current command on here
int currentMotorX = 90;
int currentMotorY = 90;


//___________________________________________________________________________________________________________//



void sendMotorX(int x)
{
x = std::clamp(x, 0, 180);
Serial.print("SEND: ");
Serial.println(x);
myservo1.write(x);
currentMotorX = x;
}

void sendMotorY(int y)
{
//limit the motor movements here because this is the only place its moving
y = std::clamp(y, 0, 180);
Serial.print("SEND: ");
Serial.println(y);
myservo2.write(y);
currentMotorY = y;
}







//basically a function that each determines the state of the socket
void webSocketEvent(WStype_t type, uint8_t *payload, size_t length) 
{

  switch (type) 
 {
    case WStype_DISCONNECTED:
      Serial.println("[WSc] Disconnected!");
      break;
    case WStype_CONNECTED:
      Serial.println("[WSc] Connected!");
      

      // send message to server when Connected
      
      break;
    
    
    //if text is received  
    case WStype_TEXT:{
    Serial.println("Received");
    
    //json conversion
    JsonDocument doc;
    DeserializationError error = deserializeJson(doc, payload, length);
    if (error) {
        Serial.println("JSON parsing failed");
        break;
    }

    if (doc.containsKey("xMotor") && doc.containsKey("yMotor"))
    {

      // new commands: where do you wanna move to?
      int xNew = doc["xMotor"];
      int yNew = doc["yMotor"];
      

      // previous angle
      int xPrev = currentMotorX;
      int yPrev = currentMotorY;


    // sets direction of movement
     int xDirection = 0;

      if (xNew != xPrev) {
          xDirection = abs(xNew - xPrev) / (xNew - xPrev);
      }

      int yDirection = 0;

      if (yNew != yPrev) {
          yDirection = abs(yNew - yPrev) / (yNew - yPrev);
      }
      
      



      //finds the max distance either x motor or y motor will have to move
      int maximum = max(abs(xNew-xPrev), abs(yNew-yPrev));

      //moves until completion
      for (int i = 0; i<=maximum; i+=2){

       

        // moves until passes target. Send motor updates the current angle
        if(abs(xNew-xPrev)>=i){
          sendMotorX(xPrev+(i)*xDirection);
        }

        // moves until passes target
        if(abs(yNew-yPrev)>=i){
          sendMotorY(yPrev+(i)*yDirection);
        }

        delay(10);
      

        //sends position every ten degrees, we will then predict every time its not sent
        if((i%10 == 0 && i>0) || i>=maximum){
        webSocket.sendTXT((String)currentMotorX + "," + (String)currentMotorY);
        }

      
     }


      
      break;
   }
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

  webSocket.begin("ADD CURRENT HOST IP(COMPUTER ITS RUNNING ON", 5556, "/stream");
  

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
