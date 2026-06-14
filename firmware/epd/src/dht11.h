#pragma once

#include <Arduino.h>

namespace TempSensor {
    void init(uint8_t pin);
    float readHumidity();
    float readTemperature();
}
