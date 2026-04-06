#include <Arduino.h>

const uint8_t REPORT_BUTTON_PIN = 2;
const uint8_t CRC_POLYNOMIAL = 0x07;  // x^8 + x^2 + x + 1
const unsigned long SERIAL_BAUDRATE = 9600;
const unsigned long DEBOUNCE_DELAY_MS = 50;

uint8_t currentCrc = 0x00;
unsigned long bytesReceived = 0;

bool lastButtonReading = HIGH;
bool stableButtonState = HIGH;
unsigned long lastDebounceTime = 0;

uint8_t updateCrc8(uint8_t crc, uint8_t dataByte) {
  crc ^= dataByte;

  for (uint8_t bit = 0; bit < 8; bit++) {
    if (crc & 0x80) {
      crc = static_cast<uint8_t>((crc << 1) ^ CRC_POLYNOMIAL);
    } else {
      crc <<= 1;
    }
  }

  return crc;
}

void printHexByte(uint8_t value) {
  if (value < 0x10) {
    Serial.print('0');
  }
  Serial.print(value, HEX);
}

void printByteDescription(uint8_t value) {
  if (value >= 32 && value <= 126) {
    Serial.print('\'');
    Serial.print(static_cast<char>(value));
    Serial.print('\'');
  } else {
    Serial.print(F("non-printable"));
  }
}

void handleIncomingUart() {
  while (Serial.available() > 0) {
    uint8_t receivedByte = static_cast<uint8_t>(Serial.read());
    currentCrc = updateCrc8(currentCrc, receivedByte);
    bytesReceived++;

    Serial.print(F("RX "));
    printByteDescription(receivedByte);
    Serial.print(F(" (0x"));
    printHexByte(receivedByte);
    Serial.print(F("), CRC=0x"));
    printHexByte(currentCrc);
    Serial.println();
  }
}

void printAndResetCrc() {
  Serial.println(F("----- CRC report -----"));
  Serial.print(F("Bytes received: "));
  Serial.println(bytesReceived);
  Serial.print(F("CRC-8 = 0x"));
  printHexByte(currentCrc);
  Serial.println();
  Serial.println(F("Accumulator reset to 0x00."));
  Serial.println(F("----------------------"));

  currentCrc = 0x00;
  bytesReceived = 0;
}

void handleReportButton() {
  bool reading = digitalRead(REPORT_BUTTON_PIN);

  if (reading != lastButtonReading) {
    lastDebounceTime = millis();
    lastButtonReading = reading;
  }

  if ((millis() - lastDebounceTime) > DEBOUNCE_DELAY_MS && reading != stableButtonState) {
    stableButtonState = reading;

    if (stableButtonState == LOW) {
      printAndResetCrc();
    }
  }
}

void setup() {
  pinMode(REPORT_BUTTON_PIN, INPUT_PULLUP);
  Serial.begin(SERIAL_BAUDRATE);

  Serial.println(F("Lab 3 / CRC-8 UART server / reset mode"));
  Serial.println(F("Polynomial: 0x07 (x^8 + x^2 + x + 1)"));
  Serial.println(F("UART speed: 9600"));
  Serial.println(F("Serial Monitor setting: No line ending"));
  Serial.println(F("Press the button on D2 to print CRC and reset the accumulator."));
}

void loop() {
  handleIncomingUart();
  handleReportButton();
}
