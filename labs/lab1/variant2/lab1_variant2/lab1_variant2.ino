#include <Arduino.h>

const uint8_t FASTER_BUTTON_PIN = 2;
const uint8_t SLOWER_BUTTON_PIN = 3;
const uint8_t PORTB_LED_MASK = 0b00111111;
const unsigned long DEBOUNCE_DELAY_MS = 50;
const unsigned long MIN_STEP_DELAY_MS = 50;
const unsigned long MAX_STEP_DELAY_MS = 1000;
const unsigned long STEP_DELAY_DELTA_MS = 50;

bool lastFasterReading = HIGH;
bool fasterStableState = HIGH;
unsigned long fasterDebounceTime = 0;

bool lastSlowerReading = HIGH;
bool slowerStableState = HIGH;
unsigned long slowerDebounceTime = 0;

uint8_t currentLedIndex = 0;
unsigned long stepDelayMs = 250;
unsigned long lastStepTime = 0;

void outputRunningLight(uint8_t ledIndex) {
  PORTB = (PORTB & 0b11000000) | (1 << ledIndex);
}

void handleFasterButton() {
  bool reading = digitalRead(FASTER_BUTTON_PIN);

  if (reading != lastFasterReading) {
    fasterDebounceTime = millis();
    lastFasterReading = reading;
  }

  if ((millis() - fasterDebounceTime) > DEBOUNCE_DELAY_MS && reading != fasterStableState) {
    fasterStableState = reading;

    if (fasterStableState == LOW && stepDelayMs > MIN_STEP_DELAY_MS) {
      stepDelayMs -= STEP_DELAY_DELTA_MS;
      if (stepDelayMs < MIN_STEP_DELAY_MS) {
        stepDelayMs = MIN_STEP_DELAY_MS;
      }
    }
  }
}

void handleSlowerButton() {
  bool reading = digitalRead(SLOWER_BUTTON_PIN);

  if (reading != lastSlowerReading) {
    slowerDebounceTime = millis();
    lastSlowerReading = reading;
  }

  if ((millis() - slowerDebounceTime) > DEBOUNCE_DELAY_MS && reading != slowerStableState) {
    slowerStableState = reading;

    if (slowerStableState == LOW && stepDelayMs < MAX_STEP_DELAY_MS) {
      stepDelayMs += STEP_DELAY_DELTA_MS;
      if (stepDelayMs > MAX_STEP_DELAY_MS) {
        stepDelayMs = MAX_STEP_DELAY_MS;
      }
    }
  }
}

void setup() {
  DDRB |= PORTB_LED_MASK;
  outputRunningLight(currentLedIndex);

  pinMode(FASTER_BUTTON_PIN, INPUT_PULLUP);
  pinMode(SLOWER_BUTTON_PIN, INPUT_PULLUP);
}

void loop() {
  handleFasterButton();
  handleSlowerButton();

  unsigned long now = millis();
  if (now - lastStepTime >= stepDelayMs) {
    lastStepTime = now;
    currentLedIndex = (currentLedIndex + 1) % 6;
    outputRunningLight(currentLedIndex);
  }
}
