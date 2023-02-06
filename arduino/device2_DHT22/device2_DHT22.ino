#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include "DHT.h"

// Board: NodeMCCU 0.9 (ESP-12 Module)


const char* ssid = "Lolek";
const char* password = "pecnamspadla";

// MQTT Broker
const char broker[] = "broker.emqx.io";
int port = 1883;
const char* setUpTopic = "SETUP/ZA/01008/SUB/DD/6/008";  // SETUP / city / ZIP code / SUB vs PUB / building / floor / room
const char* topic  = "ZA/01008/SUB/DD/6/008/temperature-humidity";

WiFiClient espClient;
PubSubClient client(espClient);

String macAddress = String(WiFi.macAddress());

const int DHTPIN = 2;
DHT dht(DHTPIN, DHT22); //Sensor initiation

unsigned long lastTime = 0;
// Timer set to a minute (60000)
unsigned long timerDelay = 60000;

void setup() {
  Serial.begin(9600);
  Serial.println("Connecting");
  dht.begin();

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
  location["floor"] = "4";
  location["room"] = "015";
  JsonArray sensors = doc.createNestedArray("sensors");  
  JsonObject sensor1  = sensors.createNestedObject();
  sensor1["order"] = 1;
  sensor1["type"] = "temperature";
  sensor1["unit"] = "°C";
  JsonObject sensor2  = sensors.createNestedObject();
  sensor2["order"] = 2;
  sensor2["type"] = "humidity";
  sensor2["unit"] = "%";
  
  char setUpData[400];
  serializeJson(doc, setUpData);
  client.publish(setUpTopic, setUpData);
}

void loop() {
  client.loop();
  if ((millis() - lastTime) > timerDelay) {
    float humidity = dht.readHumidity(); 
    float temperature = dht.readTemperature(); 
    //Check. If the reading fails, then "Read error" is displayed and the program exits
    if (isnan(humidity) || isnan(temperature)) { 
      Serial.println("Reading error");
      return;
    }

    String tempData = getJsonData(1, temperature);
    Serial.print("Sending temperature message to topic: ");
    Serial.println(topic);
    Serial.println(tempData);
    client.publish(topic, tempData.c_str());

    String humiData = getJsonData(2, humidity);
    Serial.print("Sending humidity message to topic: ");
    Serial.println(topic);
    Serial.println(humiData);
    client.publish(topic, humiData.c_str());
    lastTime = millis();
  }
}

String getJsonData(int order, float data) {
  StaticJsonDocument<300> doc;
  doc["mac"] = macAddress;
  doc["order"] = order;
  doc["data"] = data;
  String jsonData;
  serializeJson(doc, jsonData);  
  return jsonData;        
}
