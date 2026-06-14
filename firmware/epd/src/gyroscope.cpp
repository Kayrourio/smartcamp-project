#include "gyroscope.h"
#include <MPU6050_light.h>
#include <Wire.h>

static MPU6050 _mpu(Wire);
static bool _ready = false;

bool Gyroscope::init(uint8_t sda, uint8_t scl) {
    Wire.begin(sda, scl);
    Wire.setTimeOut(50);  // 50 ms — prevents I2C bus hang from starving the WDT
    byte err = _mpu.begin();
    if (err != 0) {
        Serial.print(F("[Gyroscope] MPU6050 not found (err="));
        Serial.print(err);
        Serial.println(F("). Check wiring and I2C address."));
        return false;
    }
    Serial.println(F("[Gyroscope] Calibrating... keep sensor still."));
    _mpu.calcOffsets();
    Serial.println(F("[Gyroscope] Ready."));
    _ready = true;
    return true;
}

void Gyroscope::update() {
    if (_ready) _mpu.update();
}

float Gyroscope::getAngleX() { return _ready ? _mpu.getAngleX() : 0.0f; }
float Gyroscope::getAngleY() { return _ready ? _mpu.getAngleY() : 0.0f; }
float Gyroscope::getAngleZ() { return _ready ? _mpu.getAngleZ() : 0.0f; }
