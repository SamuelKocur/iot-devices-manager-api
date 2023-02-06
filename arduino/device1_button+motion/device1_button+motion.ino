#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

// Board: NodeMCCU 0.9 (ESP-12 Module)


const char* ssid = "Lolek";
const char* password = "pecnamspadla";

// MQTT Broker
const char broker[] = "broker.emqx.io";
int port = 1883;
const char* setUpTopic = "SETUP/ZA/01008/SUB/DD/6/008";  // SETUP / city / ZIP code / SUB vs PUB / building / floor / room
const char* buttonTopic  = "ZA/01008/SUB/DD/6/008/led_button";
const char* pirTopic  = "ZA/01008/SUB/DD/6/008/motion_detector";

WiFiClient espClient;
PubSubClient client(espClient);

String macAddress = String(WiFi.macAddress());

const int buttonPin = D3;
const int pirPin = D4;

int buttonState = HIGH;
int currentButtonState = HIGH;
int pirState = HIGH;
int currentPirState = HIGH;

void setup() {
  pinMode(buttonPin, INPUT);
  pinMode(pirPin, INPUT);
  Serial.begin(9600);

  // connecting to a WiFi network
  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());

  //connecting to a mqtt broker
  Serial.print("Attempting to connect to the MQTT broker: ");
  Serial.println(broker);

  client.setServer(broker, port);

  while (!client.connected()) {
      Serial.printf("Connecting to the public mqtt broker\n");
      if (client.connect(macAddress.c_str(), "", "")) {
          Serial.println("Public emqx mqtt broker connected");
      } else {
          Serial.print("failed with state ");
          Serial.print(client.state());
          delay(2000);
      }
  }


  // create setup message
  StaticJsonDocument<400> doc;

  doc["mac"] = macAddress;
  JsonObject location  = doc.createNestedObject("location");
  location["building"] = "DD";
  location["floor"] = "6";
  location["room"] = "008";
  JsonArray sensors = doc.createNestedArray("sensors");  
  JsonObject sensor1  = sensors.createNestedObject();
  sensor1["order"] = 1;
  sensor1["type"] = "button";
  sensor1["unit"] = "bool";
  JsonObject sensor2  = sensors.createNestedObject();
  sensor2["order"] = 2;
  sensor2["type"] = "motion";
  sensor2["unit"] = "bool";
  
  char setUpData[400];
  serializeJson(doc, setUpData);
  client.publish(setUpTopic, setUpData);
}

void loop() {
  client.loop();
  // button
  currentButtonState = digitalRead(buttonPin);

  if (currentButtonState == LOW && buttonState == HIGH) {
    //Check WiFi connection status
    if(WiFi.status()== WL_CONNECTED){
      String data = getJsonData(1, "1");       
      Serial.print("Sending message to topic: ");
      Serial.println(buttonTopic);
      Serial.println(data);

      // Send message to button topic
      client.publish(buttonTopic, data.c_str());
    }
    else {
      Serial.println("WiFi Disconnected");
    }
  }
  buttonState = currentButtonState;

  // motion sensor
  currentPirState = digitalRead(pirPin);

  if (currentPirState == LOW && pirState == HIGH) {
    String data = getJsonData(2, "1");       
    Serial.print("Sending message to topic: ");
    Serial.println(pirTopic);
    Serial.println(data);

    // Send message to button topic
    client.publish(pirTopic, data.c_str());
    currentButtonState = HIGH;
  }  
  pirState = currentPirState;
}

String getJsonData(int order, String data) {
  StaticJsonDocument<300> doc;
  doc["mac"] = macAddress;
  doc["order"] = order;
  doc["data"] = data;
  String jsonData;
  serializeJson(doc, jsonData);  
  return jsonData;        
}
