#include <WiFi.h>
#include <WebServer.h>
#include <ESP32Servo.h>  // Include the ESP32Servo library

const char* ssid = "Prashant";         // Replace with your WiFi SSID
const char* password = "15241524"; // Replace with your WiFi Password

WebServer server(80); // Create a web server object that listens on port 80

#define BUZZER 12
#define SERVO_PIN 14

Servo myServo;  // Create servo object to control a servo

void handleOn() {
  myServo.write(0); // Move servo to 90 degrees
  delay(5000);
  myServo.write(180); // Move servo back to 0 degrees
  server.send(200, "text/plain", "LED, BUZZER, and SERVO are ON");
}

void handleOff() {
  digitalWrite(BUZZER, HIGH);
  myServo.write(0); // Move servo to 0 degrees
  delay(5000);
  digitalWrite(BUZZER, LOW);
  server.send(200, "text/plain", "LED, BUZZER, and SERVO are OFF");
}

void setup() {
  Serial.begin(115200);
  pinMode(BUZZER, OUTPUT);

  myServo.attach(SERVO_PIN);  // Attach the servo on pin 14 to the servo object

  // Connect to WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // Print the IP address
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  // Define the endpoints and their respective handler functions
  server.on("/on", HTTP_GET, handleOn);
  server.on("/off", HTTP_GET, handleOff);

  server.begin(); // Start the server
  Serial.println("HTTP server started");
}

void loop() {
  server.handleClient(); // Handle client requests
}
