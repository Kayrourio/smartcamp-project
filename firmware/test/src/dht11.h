#pragma once

#include <Arduino.h>

namespace DHT11 {
    void init(uint8_t pin);
    float readHumidity();
    float readTemperature();
}
