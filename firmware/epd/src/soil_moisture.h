#pragma once

#include <Arduino.h>

namespace SoilMoisture {
    void init(uint8_t pin);
    int readPercent();
}
