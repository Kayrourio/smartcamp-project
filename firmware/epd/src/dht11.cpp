#include "dht11.h"
#include <DHT.h>

static DHT _dht(0, ::DHT11);
static uint8_t _pin;

void TempSensor::init(uint8_t pin) {
    _pin = pin;
    _dht = DHT(pin, ::DHT11);
    _dht.begin();
}

float TempSensor::readHumidity() {
    return _dht.readHumidity();
}

float TempSensor::readTemperature() {
    return _dht.readTemperature();
}
