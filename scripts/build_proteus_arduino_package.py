from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_DIR = ROOT / "deliverables" / "proteus-arduino"
ARDUINO_DIR = PACKAGE_DIR / "arduino-ide"
PROTEUS_DIR = PACKAGE_DIR / "proteus"

ARDUINO_CLI = Path("/Applications/Arduino IDE.app/Contents/Resources/app/lib/backend/resources/arduino-cli")
FQBN = "arduino:avr:uno"


SKETCHES = [
    {
        "id": "lab1_variant1",
        "label": "ЛР1 вариант 1",
        "path": ROOT / "labs/lab1/variant1/lab1_variant1",
        "pins": [
            "LED0-LED5 -> D8-D13 через 220 Ом",
            "INC -> D2, кнопка на GND",
            "DEC -> D3, кнопка на GND",
        ],
    },
    {
        "id": "lab1_variant2",
        "label": "ЛР1 вариант 2",
        "path": ROOT / "labs/lab1/variant2/lab1_variant2",
        "pins": [
            "LED0-LED5 -> D8-D13 через 220 Ом",
            "SLOW -> D2, кнопка на GND",
            "FAST -> D3, кнопка на GND",
        ],
    },
    {
        "id": "lab2_variant1",
        "label": "ЛР2 вариант 1",
        "path": ROOT / "labs/lab2/variant1/lab2_variant1",
        "pins": [
            "LM35 VCC -> 5V",
            "LM35 VOUT -> A0",
            "LM35 GND -> GND",
            "START -> D2, кнопка на GND",
        ],
    },
    {
        "id": "lab2_variant2",
        "label": "ЛР2 вариант 2",
        "path": ROOT / "labs/lab2/variant2/lab2_variant2",
        "pins": [
            "Потенциометр крайние выводы -> 5V и GND",
            "Потенциометр средний вывод -> A0",
            "BUTTON -> D2, кнопка на GND",
        ],
    },
    {
        "id": "lab3_crc8_reset",
        "label": "ЛР3 CRC-8 reset",
        "path": ROOT / "labs/lab3/erofeev/lab3_crc8_reset",
        "pins": [
            "BUTTON -> D2, кнопка на GND",
            "UART -> USB/Serial",
            "Serial Monitor -> 9600, No line ending",
        ],
    },
    {
        "id": "lab3_crc8_accumulate",
        "label": "ЛР3 CRC-8 accumulate",
        "path": ROOT / "labs/lab3/erofeev/lab3_crc8_accumulate",
        "pins": [
            "BUTTON -> D2, кнопка на GND",
            "UART -> USB/Serial",
            "Serial Monitor -> 9600, No line ending",
        ],
    },
    {
        "id": "lab4_variant2",
        "label": "ЛР4 вариант 2",
        "path": ROOT / "labs/lab4/variant2/lab4_variant2",
        "pins": [
            "LDR -> 5V и A0",
            "10 кОм -> A0 и GND",
            "LED1-LED8 -> D6-D13 через 220 Ом",
        ],
    },
]


def reset_dirs() -> None:
    if PACKAGE_DIR.exists():
        shutil.rmtree(PACKAGE_DIR)
    ARDUINO_DIR.mkdir(parents=True, exist_ok=True)
    PROTEUS_DIR.mkdir(parents=True, exist_ok=True)


def copy_sketches() -> None:
    for sketch in SKETCHES:
        target = ARDUINO_DIR / sketch["id"]
        shutil.copytree(sketch["path"], target)


def compile_hex() -> None:
    for sketch in SKETCHES:
        target = PROTEUS_DIR / sketch["id"]
        target.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            [
                str(ARDUINO_CLI),
                "compile",
                "--fqbn",
                FQBN,
                "--output-dir",
                str(target),
                str(sketch["path"]),
            ],
            check=True,
        )

        produced_hex = next(target.glob("*.hex"))
        final_hex = target / f"{sketch['id']}.hex"
        if produced_hex != final_hex:
            if final_hex.exists():
                final_hex.unlink()
            produced_hex.rename(final_hex)

        for extra in target.iterdir():
            if extra.name in {final_hex.name, "pins.txt"}:
                continue
            if extra.suffix.lower() in {".eep", ".elf", ".bin", ".hex"}:
                extra.unlink(missing_ok=True)

        pins_file = target / "pins.txt"
        pins_file.write_text("\n".join(sketch["pins"]) + "\n", encoding="utf-8")


def build_readme() -> None:
    lines = [
        "# Proteus 8.13 + Arduino IDE Package",
        "",
        "Здесь собран готовый комплект для показа и загрузки.",
        "",
        "## Что открывать в Arduino IDE",
        "",
    ]
    for sketch in SKETCHES:
        lines.append(f"- `arduino-ide/{sketch['id']}`")

    lines.extend(
        [
            "",
            "## Что загружать в Proteus 8.13",
            "",
            "Для Arduino Uno в Proteus используйте файл `*.hex` из соответствующей папки в `proteus/`.",
            "",
        ]
    )

    for sketch in SKETCHES:
        lines.append(f"- `proteus/{sketch['id']}/{sketch['id']}.hex`")

    lines.extend(
        [
            "",
            "## Как использовать в Proteus",
            "",
            "1. Добавьте на схему `Arduino UNO R3`.",
            "2. Откройте свойства платы.",
            "3. В поле `Program File` укажите нужный `*.hex`.",
            "4. Соберите схему по файлу `pins.txt` в той же папке.",
            "5. Запустите симуляцию.",
            "",
            "## Важно",
            "",
            "- HEX-файлы собраны под `Arduino Uno`.",
            "- Для кнопок в проектах используется `INPUT_PULLUP`, поэтому кнопки замыкаются на `GND`.",
            "- Для ЛР3 в Serial Monitor/Virtual Terminal используйте `9600 бод`.",
        ]
    )

    (PACKAGE_DIR / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    reset_dirs()
    copy_sketches()
    compile_hex()
    build_readme()
    print("deliverables/proteus-arduino")


if __name__ == "__main__":
    main()
