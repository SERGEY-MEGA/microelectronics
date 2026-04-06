#include <Arduino.h>

const uint8_t LDR_PIN = A0;
const uint8_t LED_PINS[] = {6, 7, 8, 9, 10, 11, 12, 13};
const uint8_t LED_COUNT = sizeof(LED_PINS) / sizeof(LED_PINS[0]);

uint16_t filteredLightLevel = 0;
bool filterInitialized = false;

void setup() {
  for (uint8_t i = 0; i < LED_COUNT; i++) {
    pinMode(LED_PINS[i], OUTPUT);
    digitalWrite(LED_PINS[i], LOW);
  }
}

void updateLedBar(uint8_t ledsToLight) {
  for (uint8_t i = 0; i < LED_COUNT; i++) {
    digitalWrite(LED_PINS[i], i < ledsToLight ? HIGH : LOW);
  }
}

void loop() {
  uint16_t rawLightLevel = analogRead(LDR_PIN);

  if (!filterInitialized) {
    filteredLightLevel = rawLightLevel;
    filterInitialized = true;
  } else {
    filteredLightLevel = (filteredLightLevel * 3 + rawLightLevel) / 4;
  }

  uint8_t ledsToLight = constrain(map(filteredLightLevel, 0, 1023, 0, LED_COUNT), 0, LED_COUNT);
  updateLedBar(ledsToLight);

  delay(50);
}
