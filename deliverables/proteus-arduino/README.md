# Proteus 8.13 + Arduino IDE Package

Здесь собран готовый комплект для показа и загрузки.

## Что открывать в Arduino IDE

- `arduino-ide/lab1_variant1`
- `arduino-ide/lab1_variant2`
- `arduino-ide/lab2_variant1`
- `arduino-ide/lab2_variant2`
- `arduino-ide/lab3_crc8_reset`
- `arduino-ide/lab3_crc8_accumulate`
- `arduino-ide/lab4_variant2`

## Что загружать в Proteus 8.13

Для Arduino Uno в Proteus используйте файл `*.hex` из соответствующей папки в `proteus/`.

- `proteus/lab1_variant1/lab1_variant1.hex`
- `proteus/lab1_variant2/lab1_variant2.hex`
- `proteus/lab2_variant1/lab2_variant1.hex`
- `proteus/lab2_variant2/lab2_variant2.hex`
- `proteus/lab3_crc8_reset/lab3_crc8_reset.hex`
- `proteus/lab3_crc8_accumulate/lab3_crc8_accumulate.hex`
- `proteus/lab4_variant2/lab4_variant2.hex`

## Готовые схемы для сборки в Proteus

- `schemes/lab1_variant1.md`
- `schemes/lab1_variant2.md`
- `schemes/lab2_variant1.md`
- `schemes/lab2_variant2.md`
- `schemes/lab3_crc8_reset.md`
- `schemes/lab3_crc8_accumulate.md`
- `schemes/lab4_variant2.md`

## Как использовать в Proteus

1. Добавьте на схему `Arduino UNO R3`.
2. Откройте свойства платы.
3. В поле `Program File` укажите нужный `*.hex`.
4. Соберите схему по файлу `pins.txt` в той же папке.
5. Запустите симуляцию.

## Важно

- HEX-файлы собраны под `Arduino Uno`.
- Для кнопок в проектах используется `INPUT_PULLUP`, поэтому кнопки замыкаются на `GND`.
- Для ЛР3 в Serial Monitor/Virtual Terminal используйте `9600 бод`.
