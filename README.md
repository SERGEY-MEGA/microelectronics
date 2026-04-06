# Microelectronics Labs

Этот репозиторий содержит комплект материалов по лабораторным работам на Arduino Uno:

- код для каждого варианта;
- схемы подключения в текстовом виде;
- пошаговые инструкции по сборке;
- отчеты в формате Markdown;
- готовые отчеты в форматах DOCX и PDF.

## Где что лежит

### Готовые отчеты

- `deliverables/word-reports/docx` - готовые отчеты в формате Word
- `deliverables/word-reports/pdf` - готовые отчеты в формате PDF
- `deliverables/word-reports/assets` - изображения, схемы и иллюстрации для отчетов
- `deliverables/word-reports/README.md` - краткая памятка по готовому комплекту

### Готовый пакет для Proteus 8.13 и Arduino IDE

- `deliverables/proteus-arduino/arduino-ide` - готовые папки скетчей для открытия в Arduino IDE
- `deliverables/proteus-arduino/proteus` - готовые `HEX`-файлы для загрузки в Proteus 8.13
- `deliverables/proteus-arduino/README.md` - инструкция, какой файл куда загружать

### Исходные материалы лабораторных

- `labs/lab1` - ЛР1, оба варианта
- `labs/lab2` - ЛР2, оба варианта
- `labs/lab3/erofeev` - ЛР3, вариант Ерофеева
- `labs/lab4/variant2` - ЛР4, вариант 2

### Что лежит внутри лабораторной папки

Обычно структура такая:

- `README.md` - подключение, пошаговая проверка и пояснения
- `report.md` - текст отчета в Markdown
- отдельная папка скетча - файл `.ino`, который нужно открывать в Arduino IDE

## Быстрый старт

1. Откройте нужную папку скетча в Arduino IDE.
2. Соберите схему по `README.md` внутри нужной лабораторной.
3. Выберите плату `Arduino Uno`.
4. Загрузите скетч.
5. Проверьте работу по инструкции из `README.md` и `report.md`.

## Карта репозитория по работам

### ЛР1. Ввод-вывод дискретных сигналов

- `labs/lab1/variant1` - вариант 1, вывод 6-битного числа через `Port B`
- `labs/lab1/variant1/lab1_variant1` - папка скетча для Arduino IDE
- `labs/lab1/variant1/report.md` - Markdown-отчет
- `labs/lab1/variant2` - вариант 2, бегущий огонь
- `labs/lab1/variant2/lab1_variant2` - папка скетча для Arduino IDE
- `labs/lab1/variant2/report.md` - Markdown-отчет

### ЛР2. Регистрация показаний аналоговых датчиков

- `labs/lab2/variant1` - вариант 1, датчик температуры `LM35`
- `labs/lab2/variant1/lab2_variant1` - папка скетча для Arduino IDE
- `labs/lab2/variant1/report.md` - Markdown-отчет
- `labs/lab2/variant2` - вариант 2, потенциометр и статистика
- `labs/lab2/variant2/lab2_variant2` - папка скетча для Arduino IDE
- `labs/lab2/variant2/report.md` - Markdown-отчет

### ЛР3. CRC-8 сервер по UART

- `labs/lab3/erofeev` - описание работы, подключение и отчет
- `labs/lab3/erofeev/lab3_crc8_reset` - базовая версия со сбросом CRC после выдачи
- `labs/lab3/erofeev/lab3_crc8_accumulate` - версия без сброса CRC
- `labs/lab3/erofeev/report.md` - Markdown-отчет

### ЛР4. Система управления с обратной связью

- `labs/lab4/variant2` - вариант 2, индикатор уровня освещенности
- `labs/lab4/variant2/lab4_variant2` - папка скетча для Arduino IDE
- `labs/lab4/variant2/report.md` - Markdown-отчет

## Структура

- `labs/lab3/erofeev` - ЛР3, вариант Ерофеева: CRC-8 сервер по UART
- `labs/lab2/variant1` - ЛР2, вариант 1
- `labs/lab2/variant2` - ЛР2, вариант 2
- `labs/lab4/variant2` - ЛР4, вариант 2
- `labs/lab1/variant1` - ЛР1, вариант 1
- `labs/lab1/variant2` - ЛР1, вариант 2
- `docs/requirements-summary.md` - краткая выжимка требований и принятые допущения

## Порядок выполнения

Материалы разложены в приоритетном порядке, который обсуждался:

1. Лабораторная работа 2
2. Лабораторная работа 3
3. Лабораторная работа 4
4. Лабораторная работа 1

## Важные допущения

- Для ЛР2, вариант 1 в исходном задании не указаны конкретные значения частоты и объема выборки.
- В реализации по умолчанию приняты `10 Гц` и `64 отсчета`.
- При необходимости эти параметры меняются прямо в файле `labs/lab2/variant1/lab2_variant1/lab2_variant1.ino` через константы `SAMPLE_FREQUENCY_HZ` и `SAMPLE_COUNT`.
- Для ЛР3 выбран стандартный порождающий полином CRC-8 `0x07`, соответствующий полиному `x^8 + x^2 + x + 1`.
- Если преподаватель требует другой полином, он меняется константой `CRC_POLYNOMIAL`.
