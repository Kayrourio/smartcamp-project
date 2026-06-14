#include <WiFi.h>
#include <esp_now.h>

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

static void onReceive(const esp_now_recv_info_t *info, const uint8_t *data, int len) {
    if (len != sizeof(EPDPacket)) return;

    EPDPacket pkt;
    memcpy(&pkt, data, sizeof(pkt));
    pkt.uuid[sizeof(pkt.uuid) - 1] = '\0';

    Serial.print(F("["));
    Serial.print(pkt.uuid);
    Serial.println(F("]"));
    Serial.print(F("Temperature:   ")); Serial.print(pkt.temperature);  Serial.println(F(" C"));
    Serial.print(F("Air Humidity:  ")); Serial.print(pkt.humidity);     Serial.println(F("%"));
    Serial.print(F("Soil Moisture: ")); Serial.print(pkt.soilMoisture); Serial.println(F("%"));
    Serial.print(F("Angle X: "));      Serial.print(pkt.angleX);        Serial.println(F(" deg"));
    Serial.print(F("Angle Y: "));      Serial.print(pkt.angleY);        Serial.println(F(" deg"));
    Serial.print(F("Angle Z: "));      Serial.print(pkt.angleZ);        Serial.println(F(" deg"));
    Serial.println(F("---"));
}

void setup() {
    Serial.begin(9600);

    WiFi.mode(WIFI_STA);
    Serial.print(F("CPD MAC: "));
    Serial.println(WiFi.macAddress());

    if (esp_now_init() != ESP_OK) {
        Serial.println(F("[ESP-NOW] Init failed!"));
        return;
    }

    esp_now_register_recv_cb(onReceive);
    Serial.println(F("SmartCamp CPD ready. Waiting for EPD packets..."));
}

void loop() {}
