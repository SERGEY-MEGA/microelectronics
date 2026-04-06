# ЛР3, CRC-8, версия без сброса

## Задача

Подсчет CRC-8 по UART, выдача результата кнопкой, CRC продолжает накапливаться.

## Компоненты Proteus

- `ARDUINO UNO R3`
- `BUTTON`
- `VIRTUAL TERMINAL`
- `GROUND`

## HEX

- `../proteus/lab3_crc8_accumulate/lab3_crc8_accumulate.hex`

## Соединения

| Компонент | Подключение |
|---|---|
| Кнопка | D2 -> кнопка -> GND |
| Virtual Terminal RX | TX Arduino (D1) |
| Virtual Terminal TX | RX Arduino (D0) |
| Скорость | 9600 бод |

## Mermaid-схема

```mermaid
graph LR
    A["Arduino UNO R3"]
    B["D2 -> BUTTON -> GND"]
    V["Virtual Terminal (9600)"]
    A --- B
    A --- V
```

## Что делать в Proteus

1. Добавьте Arduino Uno, кнопку и `Virtual Terminal`.
2. Соедините `D0/D1` Arduino с терминалом.
3. Подключите кнопку к `D2`.
4. Укажите `lab3_crc8_accumulate.hex`.
5. В терминале поставьте `9600`.
6. Запустите симуляцию и отправляйте символы.

## Что проверять

- После выдачи CRC нажатием кнопки накопление не должно сбрасываться.
- Последующие байты продолжают менять текущую CRC.
