#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include "environment.h"

// WiFi
const char *ssid = WIFI_SSID;
const char *password = WIFI_PASSWORD;

// MQTT Broker
const char *mqtt_broker = MQTT_BROKER;
char cannonTopic[] = "cannon/commands";
char thunderTopic[] = "thunder/commands";
const int mqtt_port = 1883;

WiFiClient espClient;
PubSubClient client(espClient);
char *topic;

void setup()
{
  pinMode(D5, INPUT_PULLUP);
  pinMode(D1, INPUT_PULLUP);
  pinMode(D2, INPUT_PULLUP);
  pinMode(D3, INPUT_PULLUP);
  pinMode(D6, INPUT_PULLUP);
  pinMode(D7, INPUT_PULLUP);

  pinMode(LED_BUILTIN, OUTPUT);

  Serial.begin(9600);
  // connect to a WiFi network
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(250);
    digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
    Serial.println("Connecting to WiFi..");
  }
  Serial.println("Connected to the WiFi network");

  // connecting to a mqtt broker
  client.setServer(mqtt_broker, mqtt_port);
  while (!client.connected())
  {
    if (WiFi.status() != WL_CONNECTED) {
      Serial.println("Disconnected from WiFi while connecting to MQTT Broker. Resetting.");
      ESP.restart();
    }
    String client_id = "cannon-client-";
    client_id += String(WiFi.macAddress());
    Serial.println("Connecting to mqtt broker.....");
    if (client.connect(client_id.c_str()))
    {
      Serial.println("Connected to broker");
    }
    else
    {
      Serial.print("failed with state ");
      Serial.println(client.state());
      delay(2000);
    }
  }
}
void loop()
{
  // Keeps connection to MQTT Broker happy
  client.loop();

  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Disconnected from WiFi. Resetting.");
    ESP.restart();
  } 
  if (!client.connected()){
    Serial.println("Disconnected from MQTT Broker. Resetting.");
    ESP.restart();
  }

  topic = cannonTopic;
  if (digitalRead(D7) == LOW) {
    topic = thunderTopic;
  }

  if (digitalRead(D5) == LOW) {
    client.publish(topic, "{\"cmd\":\"up\",\"duration\":200}");
    digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
    Serial.println("UP");
  } else if (digitalRead(D1) == LOW) {
    client.publish(topic, "{\"cmd\":\"down\",\"duration\":200}");
    digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
    Serial.println("DOWN");
  } else if (digitalRead(D2) == LOW) {
    client.publish(topic, "{\"cmd\":\"left\",\"duration\":200}");
    digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
    Serial.println("LEFT");
  } else if (digitalRead(D3) == LOW) {
    client.publish(topic, "{\"cmd\":\"right\",\"duration\":200}");
    digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
    Serial.println("RIGHT");
  } else if (digitalRead(D6) == LOW) {
    client.publish(topic, "{\"cmd\":\"fire\",\"duration\":200}");
    digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
    Serial.println("FIRE");
  }
}