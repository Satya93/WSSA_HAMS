#include <PubSubClient.h>
#include <ESP8266WiFi.h>
// Wifi configuration
const char* ssid = "CMU";
const char* password = "serhansatya";
// mqtt configuration
const char* server = "iot.eclipse.org";
const char* topic = "tuple/value";
const char* clientName = "com.swagle.nodemcu";
int value;
int percent;
String payload;
WiFiClient wifiClient;
PubSubClient client(wifiClient);
void wifiConnect() {
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(ssid);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("");
    Serial.print("WiFi connected.");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
    if (client.connect(clientName)) {
        Serial.print("Connected to MQTT broker at ");
        Serial.print(server);
        Serial.print(" as ");
        Serial.println(clientName);
        Serial.print("Topic is: ");
        Serial.println(topic);
    }
    else {
        Serial.println("MQTT connect failed");
        Serial.println("Will reset and try again...");
        abort();
    }
}
void mqttReConnect() {
    while (!client.connected()) {
        Serial.print("Attempting MQTT connection...");
        // Attempt to connect
        if (client.connect(clientName)) {
            Serial.println("connected");
            client.subscribe(topic);
        } else {
            Serial.print("failed, rc=");
            Serial.print(client.state());
            Serial.println(" try again in 5 seconds");
            delay(5000);
        }
    }
}
void setup() {
    Serial.begin(9600);
    client.setServer(server, 1883);
    wifiConnect();
    delay(10);
}
void loop() {
    value = analogRead(A0);
    //percent = (int) ((value * 100) / 1010);
    payload = (String) value;
    if (client.connected()) {
        if (client.publish(topic, (char*) payload.c_str())) {
            Serial.print("Publish ok (");
            Serial.print(payload);
            Serial.println(")");
        } else {
            Serial.println("Publish failed");
        }
    } else {
        mqttReConnect();
    }
    delay(200);
}
