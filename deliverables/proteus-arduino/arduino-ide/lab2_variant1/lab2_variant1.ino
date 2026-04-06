#include <Arduino.h>

const uint8_t LM35_PIN = A0;
const uint8_t TRIGGER_PIN = 2;
const uint8_t STATUS_LED_PIN = LED_BUILTIN;

const uint16_t SAMPLE_FREQUENCY_HZ = 10;
const uint8_t SAMPLE_COUNT = 64;
const uint8_t MMA_WINDOW = 5;
const unsigned long SAMPLE_INTERVAL_MS = 1000UL / SAMPLE_FREQUENCY_HZ;

volatile bool startSignalReceived = false;

uint16_t rawAdcSamples[SAMPLE_COUNT];
float rawTemperatureSamplesC[SAMPLE_COUNT];
float filteredTemperatureSamplesC[SAMPLE_COUNT];

bool acquisitionInProgress = false;
bool acquisitionFinished = false;
uint8_t currentSampleIndex = 0;
unsigned long lastSampleTimestamp = 0;

void onStartSignal() {
  startSignalReceived = true;
}

float adcToTemperatureC(uint16_t adcValue) {
  float voltage = (adcValue * 5.0f) / 1023.0f;
  return voltage * 100.0f;
}

float applyModifiedMovingAverage(float newValue, float previousFilteredValue, bool isFirstSample) {
  if (isFirstSample) {
    return newValue;
  }

  return previousFilteredValue + (newValue - previousFilteredValue) / MMA_WINDOW;
}

void resetCaptureState() {
  acquisitionInProgress = true;
  acquisitionFinished = false;
  currentSampleIndex = 0;
  lastSampleTimestamp = millis();
  digitalWrite(STATUS_LED_PIN, HIGH);
}

void finalizeCapture() {
  acquisitionInProgress = false;
  acquisitionFinished = true;
  digitalWrite(STATUS_LED_PIN, LOW);
}

void sampleOnce() {
  uint16_t rawAdc = analogRead(LM35_PIN);
  float rawTemperature = adcToTemperatureC(rawAdc);
  float previousFiltered = currentSampleIndex == 0 ? rawTemperature : filteredTemperatureSamplesC[currentSampleIndex - 1];
  float filteredTemperature = applyModifiedMovingAverage(rawTemperature, previousFiltered, currentSampleIndex == 0);

  rawAdcSamples[currentSampleIndex] = rawAdc;
  rawTemperatureSamplesC[currentSampleIndex] = rawTemperature;
  filteredTemperatureSamplesC[currentSampleIndex] = filteredTemperature;

  currentSampleIndex++;

  if (currentSampleIndex >= SAMPLE_COUNT) {
    finalizeCapture();
  }
}

void setup() {
  pinMode(TRIGGER_PIN, INPUT_PULLUP);
  pinMode(STATUS_LED_PIN, OUTPUT);
  digitalWrite(STATUS_LED_PIN, LOW);

  attachInterrupt(digitalPinToInterrupt(TRIGGER_PIN), onStartSignal, FALLING);

  Serial.begin(9600);
  Serial.println(F("Lab 2 / Variant 1 ready."));
  Serial.println(F("Waiting for external start signal on D2."));
}

void loop() {
  if (startSignalReceived && !acquisitionInProgress) {
    noInterrupts();
    startSignalReceived = false;
    interrupts();

    resetCaptureState();
    Serial.println(F("Capture started."));
  }

  if (acquisitionInProgress) {
    unsigned long now = millis();

    if (now - lastSampleTimestamp >= SAMPLE_INTERVAL_MS) {
      lastSampleTimestamp += SAMPLE_INTERVAL_MS;
      sampleOnce();

      if (acquisitionFinished) {
        Serial.println(F("Capture finished. Inspect arrays in debugger:"));
        Serial.println(F("rawAdcSamples, rawTemperatureSamplesC, filteredTemperatureSamplesC"));
      }
    }
  }
}
