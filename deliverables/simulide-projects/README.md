# Готовые проекты SimulIDE

Здесь лежат готовые схемы `SimulIDE`, которые можно открыть напрямую.

## Что открывать

- `lab1_variant1/lab1_variant1.sim1`
- `lab1_variant2/lab1_variant2.sim1`
- `lab2_variant1/lab2_variant1.sim1`
- `lab2_variant2/lab2_variant2.sim1`
- `lab3_crc8_reset/lab3_crc8_reset.sim1`
- `lab3_crc8_accumulate/lab3_crc8_accumulate.sim1`
- `lab4_variant2/lab4_variant2.sim1`

## Что лежит в каждой папке

- `*.sim1` — схема SimulIDE
- `*.hex` — уже подключенная прошивка для Arduino Uno
- `*.ino` — исходный скетч

## Как запускать

1. Откройте нужный файл `*.sim1` в `SimulIDE`.
2. Нажмите `Play`.
3. Для лабораторных с UART откройте компонент `SerialPort` на схеме.

## Подсказки

- `ЛР2 вариант 1`: в SimulIDE нет готового `LM35`, поэтому использован потенциометр-эмулятор `LM35 emu` на диапазон `0..1.5 В`.
- `ЛР2 вариант 2`: нажимайте кнопку `SAMPLE D2`, затем отправляйте в `SerialPort` команду `d`.
- `ЛР3`: отправляйте символы в `SerialPort`, затем нажимайте кнопку `CRC D2`.
- `ЛР4`: меняйте освещенность компонента `LDR`.
