#include "dht11.h"
#include "soil_moisture.h"
#include "gyroscope.h"

#include <WiFi.h>
#include <esp_now.h>

#define DHTPIN         4
#define SOILPIN        34
#define SDA_PIN        21
#define SCL_PIN        22
#define SEND_INTERVAL  2000

#define EPD_UUID  "EPD-001"

// Run the CPD firmware first and copy the MAC printed on its Serial monitor here
static uint8_t CPD_MAC[6] = {0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF};

struct __attribute__((packed)) EPDPacket {
    char    uuid[16];
    float   temperature;
    float   humidity;
    int16_t soilMoisture;
    float   angleX;
    float   angleY;
    float   angleZ;
};

static void onSent(const uint8_t *mac, esp_now_send_status_t status) {
    Serial.print(F("[ESP-NOW] Send "));
    Serial.println(status == ESP_NOW_SEND_SUCCESS ? F("OK") : F("FAIL"));
}

void setup() {
    Serial.begin(9600);

    WiFi.mode(WIFI_STA);
    if (esp_now_init() != ESP_OK) {
        Serial.println(F("[ESP-NOW] Init failed!"));
        return;
    }
    esp_now_register_send_cb(onSent);

    esp_now_peer_info_t peer = {};
    memcpy(peer.peer_addr, CPD_MAC, 6);
    peer.channel = 0;
    peer.encrypt = false;
    esp_now_add_peer(&peer);

    TempSensor::init(DHTPIN);
    SoilMoisture::init(SOILPIN);
    if (!Gyroscope::init(SDA_PIN, SCL_PIN)) {
        Serial.println(F("WARNING: Gyroscope disabled."));
    }

    Serial.println(F("SmartCamp EPD ready."));
}

void loop() {
    Gyroscope::update();

    static unsigned long lastSend = 0;
    unsigned long now = millis();
    if (now - lastSend < SEND_INTERVAL) return;
    lastSend = now;

    float h    = TempSensor::readHumidity();
    float t    = TempSensor::readTemperature();
    int   soil = SoilMoisture::readPercent();

    if (isnan(h) || isnan(t)) {
        Serial.println(F("Failed to read from DHT11!"));
    } else {
        Serial.print(F("Air Humidity: "));  Serial.print(h); Serial.println(F("%"));
        Serial.print(F("Temperature:  "));  Serial.print(t); Serial.println(F(" °C"));
    }

    Serial.print(F("Soil Moisture: ")); Serial.print(soil); Serial.println(F("%"));

    Serial.print(F("Angle X: ")); Serial.print(Gyroscope::getAngleX()); Serial.println(F(" °"));
    Serial.print(F("Angle Y: ")); Serial.print(Gyroscope::getAngleY()); Serial.println(F(" °"));
    Serial.print(F("Angle Z: ")); Serial.print(Gyroscope::getAngleZ()); Serial.println(F(" °"));

    Serial.println(F("---"));

    EPDPacket pkt;
    strncpy(pkt.uuid, EPD_UUID, sizeof(pkt.uuid));
    pkt.temperature  = isnan(t) ? 0.0f : t;
    pkt.humidity     = isnan(h) ? 0.0f : h;
    pkt.soilMoisture = (int16_t)soil;
    pkt.angleX       = Gyroscope::getAngleX();
    pkt.angleY       = Gyroscope::getAngleY();
    pkt.angleZ       = Gyroscope::getAngleZ();

    esp_now_send(CPD_MAC, (uint8_t *)&pkt, sizeof(pkt));
}
