#include <WiFi.h>
#include <HTTPClient.h>

// Wi-Fi credentials
const char* ssid = "TECNO-TR109-CDBB";
const char* password = "30585069";

// Sensor and server configuration
const int smokeSensorPin = 34;   // GPIO34 (ADC input only)
const int smokeThreshold = 300;  // Calibrate as needed
const char* serverName = "https://fantastic-space-meme-695gw657g4625qrg-5000.app.github.dev/log";
WiFiServer server(80);  // Web server on port 80

void setup() {
  Serial.begin(115200);
  pinMode(smokeSensorPin, INPUT);

  Serial.println("\n Booting ESP32...");
  WiFi.begin(ssid, password);

  Serial.print("Connecting to WiFi");
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n Connected to WiFi!");
    Serial.print("📡 IP Address: ");
    Serial.println(WiFi.localIP());
    server.begin();
  } else {
    Serial.println("\n Failed to connect to WiFi.");
  }
}

unsigned long lastPostTime = 0;
const unsigned long postInterval = 10000;  // Send to server every 10s

void loop() {
  // Send data to Flask server every 10 seconds
  if (millis() - lastPostTime > postInterval && WiFi.status() == WL_CONNECTED) {
    int sensorValue = analogRead(smokeSensorPin);
    Serial.print("Sensor: ");
    Serial.println(sensorValue);

    HTTPClient http;
    http.begin(serverName);
    http.addHeader("Content-Type", "application/json");

    // Manually create JSON string
    String requestBody = "{\"smoke\":" + String(sensorValue) + "}";

    int httpResponseCode = http.POST(requestBody);
    Serial.println("Status Code: " + String(httpResponseCode));
    http.end();

    lastPostTime = millis();
  }

  // Handle browser requests for web monitoring
  WiFiClient client = server.available();
  if (client) {
    Serial.println(" Client connected.");
    String request = client.readStringUntil('\r');
    client.flush();

    int sensorValue = analogRead(smokeSensorPin);
    bool smokeDetected = sensorValue > smokeThreshold;

    String html = "<!DOCTYPE html><html><head><meta http-equiv='refresh' content='5'>";
    html += "<title>ESP32 Smoke Monitor</title>";
    html += "<style>body{font-family:Arial;text-align:center;} .alert{color:red;font-size:24px;}</style></head><body>";
    html += "<h1> MQ-2 Smoke Monitor</h1>";
    html += "<p>Sensor Value: <strong>" + String(sensorValue) + "</strong></p>";

    if (smokeDetected) {
      html += "<p class='alert'> Smoke Detected!</p>";
    } else {
      html += "<p style='color:green;'> Normal</p>";
    }

    html += "<p>Auto-refreshes every 5 seconds.</p></body></html>";

    client.println("HTTP/1.1 200 OK");
    client.println("Content-Type: text/html");
    client.println("Connection: close");
    client.println();
    client.println(html);

    delay(1);
    client.stop();
    Serial.println("Client disconnected.");
  }
}
