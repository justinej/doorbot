// Load Wi-Fi library
#include <WiFi.h>
#include <SPIFFS.h>
#include <ESP32Servo.h>
#include <FS.h>

// FILE SYSTEM NOT MOUNTED RIGHT NOW

/* You only need to format SPIFFS the first time you run a
   test or else use the SPIFFS plugin to create a partition
   https://github.com/me−no−dev/arduino−esp32fs−plugin */
#define FORMAT_SPIFFS_IF_FAILED true

String ssid = "";
String password = "";

// Set web server port number to 80
WiFiServer server(80);

// Variable to store the HTTP request
String header;
int digital_val = 0;
int val;
int relayOutputPin = 5;

// Current time
unsigned long currentTime = millis();
// Previous time
unsigned long previousTime = 0; 
// Define timeout time in milliseconds (example: 2000ms = 2s)
const long timeoutTime = 2000;

void setup() {
  Serial.begin(115200);
  SPIFFS.begin(true);
  pinMode(relayOutputPin, OUTPUT);
  digitalWrite(relayOutputPin, LOW);

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
  
  // Print local IP address and start web server
  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  server.begin();
}

void loop(){
  WiFiClient client = server.available();   // Listen for incoming clients
  if (client) {                             // If a new client connects,
    currentTime = millis();
    previousTime = currentTime;
    Serial.println("New Client.");          // print a message out in the serial port
    String currentLine = "";                // make a String to hold incoming data from the client
    while (client.connected() && currentTime - previousTime <= timeoutTime) {  // loop while the client's connected
      currentTime = millis();
      if (client.available()) {             // if there's bytes to read from the client,
        char c = client.read();             // read a byte, then
        Serial.write(c);                    // print it out the serial monitor
        if (c == '\n') {
          if (currentLine.length() == 0) {
            Serial.write("Buzzing door open");
            // Sending messages to client (web server)
            client.println("HTTP/1.1 200 OK");
            client.println("Content-type:text/html");
            client.println("Connection: close");
            client.println();

            digitalWrite(relayOutputPin, HIGH);
            delay(10000);
            digitalWrite(relayOutputPin, LOW);
            delay(1000);
            
            break;
          } else {
            currentLine = "";
          }
        } else if (c != '\r') {
            currentLine += c;
        }
      }
    }
    Serial.println(client.remoteIP());
    // Close the connection
    client.stop();
    Serial.println("Client disconnected.");
    Serial.println("");
  }
}
