#include <Arduino.h>

const uint8_t INCREMENT_BUTTON_PIN = 2;
const uint8_t DECREMENT_BUTTON_PIN = 3;
const uint8_t PORTB_LED_MASK = 0b00111111;
const unsigned long DEBOUNCE_DELAY_MS = 50;

uint8_t counterValue = 0;

bool lastIncrementReading = HIGH;
bool incrementStableState = HIGH;
unsigned long incrementDebounceTime = 0;

bool lastDecrementReading = HIGH;
bool decrementStableState = HIGH;
unsigned long decrementDebounceTime = 0;

void outputValueToPortB(uint8_t value) {
  PORTB = (PORTB & 0b11000000) | (value & PORTB_LED_MASK);
}

void handleIncrementButton() {
  bool reading = digitalRead(INCREMENT_BUTTON_PIN);

  if (reading != lastIncrementReading) {
    incrementDebounceTime = millis();
    lastIncrementReading = reading;
  }

  if ((millis() - incrementDebounceTime) > DEBOUNCE_DELAY_MS && reading != incrementStableState) {
    incrementStableState = reading;

    if (incrementStableState == LOW) {
      counterValue = (counterValue + 1) & PORTB_LED_MASK;
      outputValueToPortB(counterValue);
    }
  }
}

void handleDecrementButton() {
  bool reading = digitalRead(DECREMENT_BUTTON_PIN);

  if (reading != lastDecrementReading) {
    decrementDebounceTime = millis();
    lastDecrementReading = reading;
  }

  if ((millis() - decrementDebounceTime) > DEBOUNCE_DELAY_MS && reading != decrementStableState) {
    decrementStableState = reading;

    if (decrementStableState == LOW) {
      counterValue = (counterValue - 1) & PORTB_LED_MASK;
      outputValueToPortB(counterValue);
    }
  }
}

void setup() {
  DDRB |= PORTB_LED_MASK;
  outputValueToPortB(counterValue);

  pinMode(INCREMENT_BUTTON_PIN, INPUT_PULLUP);
  pinMode(DECREMENT_BUTTON_PIN, INPUT_PULLUP);
}

void loop() {
  handleIncrementButton();
  handleDecrementButton();
}
