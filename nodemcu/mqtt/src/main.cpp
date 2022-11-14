#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include "environment.h"

// WiFi
const char *ssid = WIFI_SSID;
const char *password = WIFI_PASSWORD;

// MQTT Broker
const char *mqtt_broker = MQTT_BROKER;
const char *topic = "cannon/commands";
const int mqtt_port = 1883;

WiFiClient espClient;
PubSubClient client(espClient);

void setup()
{
  pinMode(LED_BUILTIN, OUTPUT);

  // Set software serial baud to 115200;
  Serial.begin(115200);
  // connecting to a WiFi network
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
  Serial.println("Connected to the WiFi network");

  // connecting to a mqtt broker
  client.setServer(mqtt_broker, mqtt_port);
  while (!client.connected())
  {
    if (WiFi.status() != WL_CONNECTED) {
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
  if (WiFi.status() != WL_CONNECTED || !client.connected()){
    ESP.restart();
  }

  client.publish(topic, "{\"cmd\":\"up\",\"duration\":400}");
  digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
  delay(1000);

  client.publish(topic, "{\"cmd\":\"down\",\"duration\":400}");
  digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
  delay(1000);

  client.publish(topic, "{\"cmd\":\"left\",\"duration\":400}");
  digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
  delay(1000);

  client.publish(topic, "{\"cmd\":\"right\",\"duration\":400}");
  digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
  delay(1000);
}