/*********
  Rui Santos
  Complete project details at https://randomnerdtutorials.com  
*********/

// Load Wi-Fi library
#include <WiFi.h>
#include <ESP32Servo.h>
#include <SPIFFS.h>
#include <FS.h>
#include "ESPAsyncWebServer.h"

// FILE SYSTEM NOT MOUNTED RIGHT NOW

/* You only need to format SPIFFS the first time you run a
   test or else use the SPIFFS plugin to create a partition
   https://github.com/me−no−dev/arduino−esp32fs−plugin */
#define FORMAT_SPIFFS_IF_FAILED true

Servo myservo;
String ssid = "";
String password = "";

// Set web server port number to 80
AsyncWebServer server(80);
AsyncWebSocket ws("/test"); // js sends msg to IP/test

// Variable to store the HTTP request
String header;

int servoPin = 5;
int ADC_Max = 4096;
int servoOn = 1;
int servoOff = 100;
 
// Current time
unsigned long currentTime = millis();
// Previous time
unsigned long previousTime = 0; 
// Define timeout time in milliseconds (example: 2000ms = 2s)
const long timeoutTime = 2000;

void setup() {
  Serial.begin(115200);
  SPIFFS.begin(true);

  // Set up Servo motor
  ESP32PWM::allocateTimer(0);
  ESP32PWM::allocateTimer(1);
  ESP32PWM::allocateTimer(2);
  ESP32PWM::allocateTimer(3);
  myservo.setPeriodHertz(50);// Standard 50hz servo
  myservo.attach(servoPin, 500, 2400);   // attaches the servo on pin 18 to the servo object
  myservo.write(servoOff); // Start with servo Off

  
  // Connect to Wi-Fi network with SSID and password
  Serial.print("Connecting to ");
  File file = SPIFFS.open("/wifi.txt");
  char c;
  while (file.available()) {
    c = file.read();
    if (c == '\n') {
      break;
    }
    ssid += c;
  }
  Serial.println(ssid);
  while (file.available()) {
    c = file.read();
    if (c == '\n') {
      break;
    }
    password += c;
  }
  Serial.println(password);
  const char* myssid = ssid.c_str();
  const char* mypassword = password.c_str();
  WiFi.begin(myssid, mypassword);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());



  ws.onEvent(onWsEvent);
  server.addHandler(&ws);
  server.on("/printIp", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(200, "text/plain", "ok");
    Serial.print("Received request from client with IP: ");
    Serial.println(request->client()->remoteIP());
  });
  server.begin();
}


void onWsEvent(
  AsyncWebSocket* server,
  AsyncWebSocketClient* client,
  AwsEventType type,
  void* arg,
  uint8_t *data,
  size_t len) {
    if (type == WS_EVT_CONNECT) {
      Serial.print("Websocket client connection received.");
    } else if (type == WS_EVT_DISCONNECT) {
      Serial.println("Client disconnected");
      Serial.println("---------------");
    } else if (type == WS_EVT_DATA) {
      Serial.print("Data received: ");
      for (int i=0; i < len; i++) {
        Serial.print((char) data[i]);
      }

      Serial.println();
    }
  }

void loop(){}
