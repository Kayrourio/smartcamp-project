#include <WiFi.h>
#include <esp_now.h>

#define CPD_UID "CPD-CAMPUS-01"

// Must match EPDPacket in epd/src/main.cpp
struct __attribute__((packed)) EPDPacket {
    char    uuid[16];
    float   temperature;
    float   humidity;
    int16_t soilMoisture;
    float   angleX;
    float   angleY;
    float   angleZ;
};

static void onReceive(const uint8_t *mac, const uint8_t *data, int len) {
    if (len != sizeof(EPDPacket)) return;

    EPDPacket pkt;
    memcpy(&pkt, data, sizeof(pkt));
    pkt.uuid[sizeof(pkt.uuid) - 1] = '\0';

    Serial.print(F("{\"cpd_uid\":\"" CPD_UID "\",\"readings\":[{"));
    Serial.print(F("\"epd_uid\":\""));        Serial.print(pkt.uuid);
    Serial.print(F("\",\"soil_moisture\":")); Serial.print(pkt.soilMoisture);
    Serial.print(F(",\"temperature\":"));     Serial.print(pkt.temperature, 2);
    Serial.print(F(",\"rainfall\":null"));
    Serial.print(F(",\"angle_x\":"));         Serial.print(pkt.angleX, 2);
    Serial.print(F(",\"angle_y\":"));         Serial.print(pkt.angleY, 2);
    Serial.print(F(",\"angle_z\":"));         Serial.print(pkt.angleZ, 2);
    Serial.println(F("}]}"));
}

void setup() {
    Serial.begin(9600);
    delay(3000);

    WiFi.mode(WIFI_STA);
    Serial.print(F("CPD MAC: "));
    Serial.println(WiFi.macAddress());

    if (esp_now_init() != ESP_OK) {
        Serial.println(F("[ESP-NOW] Init failed!"));
        return;
    }

    esp_now_register_recv_cb(onReceive);
    Serial.println(F("SmartCamp CPD ready."));
}

void loop() {}
