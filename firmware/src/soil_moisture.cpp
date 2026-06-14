#include "soil_moisture.h"

static const int ADC_MAX   = 4095;
static const int MAX_VALID = 4090;

static uint8_t _pin;

void SoilMoisture::init(uint8_t pin) {
    _pin = pin;
}

int SoilMoisture::readPercent() {
    int raw = analogRead(_pin);
    if (raw >= MAX_VALID) return 0;
    return constrain(map(raw, 0, ADC_MAX, 100, 0), 0, 100);
}
