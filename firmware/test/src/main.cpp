#include "dht11.h"
#include "soil_moisture.h"

#define DHTPIN   4
#define SOILPIN  34

void setup() {
    Serial.begin(9600);
    DHT11::init(DHTPIN);
    SoilMoisture::init(SOILPIN);
    Serial.println("SmartCamp ready.");
}

void loop() {
    delay(2000);

    float h    = DHT11::readHumidity();
    float t    = DHT11::readTemperature();
    int   soil = SoilMoisture::readPercent();

    if (isnan(h) || isnan(t)) {
        Serial.println(F("Failed to read from DHT11!"));
    } else {
        Serial.print(F("Air Humidity: "));  Serial.print(h); Serial.println(F("%"));
        Serial.print(F("Temperature:  "));  Serial.print(t); Serial.println(F(" °C"));
    }

    Serial.print(F("Soil Moisture: ")); Serial.print(soil); Serial.println(F("%"));
    Serial.println("---");
}
