#pragma once

#include <Arduino.h>

namespace Gyroscope {
    bool init(uint8_t sda, uint8_t scl);
    void update();
    float getAngleX();
    float getAngleY();
    float getAngleZ();
}
