#include <Arduino.h>
#include <WiFiS3.h> 
#include <Servo.h>
#include <ArduinoWebsockets.h>

const char* ssid = "";
const char* pw = "";
const char* websockets_server_host = "serverip_or_name"; //Enter server adress
const uint16_t websockets_server_port = 8080; // Enter server port

websockets websocket = websockets(90)

Servo myservo1;
Servo myservo2;
int pin3 = 3;
int pin5 = 5;



//connects to wifi
void setup() {

  myservo1.attach(pin3);
  myservo2.attach(pin5);
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
myservo1.write(0);
myservo2.write(0);
delay(1500);
myservo1.write(180);
myservo2.write(180);
delay(1500);
myservo1.write(90);
myservo2.write(70);
delay(1500);
myservo1.write(46);
myservo2.write(40);
delay(1500);
}
