#!/usr/bin/env python3
"""Generate ready-to-open SimulIDE projects for all lab variants."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables" / "simulide-projects"
LABS = ROOT / "labs"
HEX_ROOT = ROOT / "deliverables" / "proteus-arduino" / "proteus"


PROJECTS = {
    "lab1_variant1": {
        "sketch": LABS / "lab1" / "variant1" / "lab1_variant1" / "lab1_variant1.ino",
        "hex": HEX_ROOT / "lab1_variant1" / "lab1_variant1.hex",
        "title": "ЛР1 вариант 1",
    },
    "lab1_variant2": {
        "sketch": LABS / "lab1" / "variant2" / "lab1_variant2" / "lab1_variant2.ino",
        "hex": HEX_ROOT / "lab1_variant2" / "lab1_variant2.hex",
        "title": "ЛР1 вариант 2",
    },
    "lab2_variant1": {
        "sketch": LABS / "lab2" / "variant1" / "lab2_variant1" / "lab2_variant1.ino",
        "hex": HEX_ROOT / "lab2_variant1" / "lab2_variant1.hex",
        "title": "ЛР2 вариант 1",
    },
    "lab2_variant2": {
        "sketch": LABS / "lab2" / "variant2" / "lab2_variant2" / "lab2_variant2.ino",
        "hex": HEX_ROOT / "lab2_variant2" / "lab2_variant2.hex",
        "title": "ЛР2 вариант 2",
    },
    "lab3_crc8_reset": {
        "sketch": LABS / "lab3" / "erofeev" / "lab3_crc8_reset" / "lab3_crc8_reset.ino",
        "hex": HEX_ROOT / "lab3_crc8_reset" / "lab3_crc8_reset.hex",
        "title": "ЛР3 CRC-8 reset",
    },
    "lab3_crc8_accumulate": {
        "sketch": LABS / "lab3" / "erofeev" / "lab3_crc8_accumulate" / "lab3_crc8_accumulate.ino",
        "hex": HEX_ROOT / "lab3_crc8_accumulate" / "lab3_crc8_accumulate.hex",
        "title": "ЛР3 CRC-8 accumulate",
    },
    "lab4_variant2": {
        "sketch": LABS / "lab4" / "variant2" / "lab4_variant2" / "lab4_variant2.ino",
        "hex": HEX_ROOT / "lab4_variant2" / "lab4_variant2.hex",
        "title": "ЛР4 вариант 2",
    },
}


def circuit_header(animate: int = 1) -> str:
    return (
        f'<circuit version="1.0.0" rev="1199" stepSize="1000000" '
        f'stepsPS="1000000" NLsteps="100000" reaStep="1000000" animate="{animate}" >\n\n'
    )


def circuit_footer() -> str:
    return "\n</circuit>\n"


def item(line: str) -> str:
    return line + "\n\n"


def uno(program: str, pos: str = "-620,-420", label: str = "Arduino Uno-1") -> str:
    return item(
        f'<item itemtype="Subcircuit" CircId="Uno-1" mainComp="false" Show_id="true" '
        f'Show_Val="false" Pos="{pos}" rotation="0" hflip="1" vflip="1" '
        f'label="{label}" idLabPos="58,-9" labelrot="0" valLabPos="0,0" '
        f'valLabRot="0" Logic_Symbol="false">\n'
        f'<mainCompProps itemtype="MCU" CircId="1_mega328-109" mainComp="true" '
        f'Show_id="false" Show_Val="false" Pos="20,20" rotation="0" hflip="1" '
        f'vflip="1" label="1_mega328-109" idLabPos="0,-20" labelrot="0" '
        f'valLabPos="-16,20" valLabRot="0" Frequency="16 MHz" Program="{program}" '
        f'Auto_Load="false" Rst_enabled="true" Ext_Osc="true" Wdt_enabled="false" />\n'
        f'</item>'
    )


def serial_port(pos: str = "-820,-500") -> str:
    return item(
        f'<item itemtype="SerialPort" CircId="SerialPort-1" mainComp="false" Show_id="false" '
        f'Show_Val="false" Pos="{pos}" rotation="0" hflip="1" vflip="1" label="SerialPort-1" '
        f'idLabPos="-34,-20" labelrot="0" valLabPos="-16,20" valLabRot="0" '
        f'Baudrate="9600 _Bauds" DataBits="8 _Bits" StopBits="1 _Bits" />'
    )


def ground(circ_id: str, pos: str) -> str:
    return item(
        f'<item itemtype="Ground" CircId="{circ_id}" mainComp="false" Show_id="false" '
        f'Show_Val="false" Pos="{pos}" rotation="0" hflip="1" vflip="1" label="{circ_id}" '
        f'idLabPos="-16,-24" labelrot="0" valLabPos="0,0" valLabRot="0" />'
    )


def rail(circ_id: str, pos: str, voltage: str) -> str:
    return item(
        f'<item itemtype="Rail" CircId="{circ_id}" mainComp="false" ShowProp="Voltage" '
        f'Show_id="false" Show_Val="true" Pos="{pos}" rotation="90" hflip="1" vflip="1" '
        f'label="{circ_id}" idLabPos="-64,-24" labelrot="0" valLabPos="-24,4" '
        f'valLabRot="-90" Voltage="{voltage}" />'
    )


def push(circ_id: str, pos: str, label: str, key: str) -> str:
    return item(
        f'<item itemtype="Push" CircId="{circ_id}" mainComp="false" Show_id="true" '
        f'Show_Val="false" Pos="{pos}" rotation="0" hflip="1" vflip="1" label="{label}" '
        f'idLabPos="-14,-24" labelrot="0" valLabPos="0,0" valLabRot="0" '
        f'Norm_Close="false" Poles="1 _Poles" Key="{key}" />'
    )


def resistor(circ_id: str, pos: str, resistance: str = "220 Ω", rotation: int = 0) -> str:
    return item(
        f'<item itemtype="Resistor" CircId="{circ_id}" mainComp="false" ShowProp="Resistance" '
        f'Show_id="false" Show_Val="true" Pos="{pos}" rotation="{rotation}" hflip="1" '
        f'vflip="1" label="{circ_id}" idLabPos="-16,-24" labelrot="0" '
        f'valLabPos="-18,8" valLabRot="0" Resistance="{resistance}" />'
    )


def led(circ_id: str, pos: str, color: str = "Red") -> str:
    return item(
        f'<item itemtype="Led" CircId="{circ_id}" mainComp="false" Show_id="true" '
        f'Show_Val="false" Pos="{pos}" rotation="0" hflip="1" vflip="1" label="{circ_id}" '
        f'idLabPos="-16,-24" labelrot="0" valLabPos="0,0" valLabRot="0" Color="{color}" '
        f'Grounded="false" Threshold="2.4 V" MaxCurrent="0.03 A" Resistance="0.6 Ω" />'
    )


def potentiometer(circ_id: str, pos: str, label: str, resistance: str, value_ohm: str) -> str:
    return item(
        f'<item itemtype="Potentiometer" CircId="{circ_id}" mainComp="false" ShowProp="Resistance" '
        f'Show_id="true" Show_Val="true" Pos="{pos}" rotation="0" hflip="1" vflip="1" '
        f'label="{label}" idLabPos="-26,-44" labelrot="0" valLabPos="18,-9" '
        f'valLabRot="90" Resistance="{resistance}" Value_Ohm="{value_ohm}" />'
    )


def ldr(circ_id: str, pos: str) -> str:
    return item(
        f'<item itemtype="LDR" CircId="{circ_id}" mainComp="false" ShowProp="Lux" '
        f'Show_id="true" Show_Val="true" Pos="{pos}" rotation="90" hflip="1" vflip="1" '
        f'label="{circ_id}" idLabPos="-20,-24" labelrot="0" valLabPos="-20,30" '
        f'valLabRot="0" Lux="500 Lux" Min_Lux="0 Lux" Max_Lux="1000 Lux" Dial_Step="0 Lux" '
        f'Gamma="0.8582" R1="127410 Ω" />'
    )


def node(circ_id: str, pos: str) -> str:
    return item(f'<item itemtype="Node" CircId="{circ_id}" mainComp="false" Pos="{pos}" />')


def text(circ_id: str, pos: str, content: str) -> str:
    safe = content.replace("&", "&amp;").replace('"', "&quot;").replace("\n", "&#xa;")
    return item(
        f'<item itemtype="TextComponent" CircId="{circ_id}" mainComp="false" Show_id="false" '
        f'Show_Val="false" Pos="{pos}" rotation="0" hflip="1" vflip="1" label="{circ_id}" '
        f'idLabPos="-16,-24" labelrot="0" valLabPos="0,0" valLabRot="0" Border="1" '
        f'Margin="4" Font="Helvetica [Cronyx]" Font_Size="10" Fixed_Width="false" '
        f'Opacity="1" Text="{safe}" />'
    )


def connector(uid: str, start: str, end: str, points: str) -> str:
    return item(
        f'<item itemtype="Connector" uid="{uid}" startpinid="{start}" endpinid="{end}" '
        f'pointList="{points}" />'
    )


def serial_connectors() -> str:
    return (
        connector("Connector-serial-rx", "SerialPort-1-pin0", "Uno-1-0", "-860,-508,-900,-508,-900,-404,-612,-404")
        + connector("Connector-serial-tx", "SerialPort-1-pin1", "Uno-1-1", "-860,-492,-892,-492,-892,-396,-612,-396")
    )


def lab1_sim1(program: str, mode_label: str) -> str:
    out = circuit_header(animate=1)
    out += uno(program)
    out += text(
        "Text-1",
        "-860,-360",
        f"{mode_label}\nD2 и D3 — кнопки\nD8..D13 — светодиоды\nЗапуск: кнопка Play",
    )
    out += push("Push-1", "-840,-260", "D2", "1")
    out += push("Push-2", "-740,-260", "D3", "2")
    out += ground("Ground-1", "-840,-220")
    out += ground("Ground-2", "-740,-220")

    y_values = [-540, -500, -460, -420, -380, -340]
    for i, y in enumerate(y_values):
        pin = 8 + i
        out += resistor(f"Resistor-{i+1}", f"-300,{y}", "220 Ω")
        out += led(f"LED{i}", f"-180,{y}", "Red")
        out += ground(f"Ground-led{i}", f"-80,{y + 16}")
        out += connector(
            f"Connector-led-src-{i}",
            f"Uno-1-{pin}",
            f"Resistor-{i+1}-lPin",
            f"-612,{y + 4},-420,{y + 4},-420,{y},-316,{y}",
        )
        out += connector(
            f"Connector-led-mid-{i}",
            f"Resistor-{i+1}-rPin",
            f"LED{i}-lPin",
            f"-284,{y},-196,{y}",
        )
        out += connector(
            f"Connector-led-gnd-{i}",
            f"LED{i}-rPin",
            f"Ground-led{i}-Gnd",
            f"-164,{y},-80,{y},-80,{y + 16}",
        )

    out += connector("Connector-btn-1", "Uno-1-2", "Push-1-pinP0", "-612,-388,-700,-388,-700,-260,-856,-260")
    out += connector("Connector-btn-1-g", "Push-1-switch0pinN", "Ground-1-Gnd", "-824,-260,-840,-260,-840,-236")
    out += connector("Connector-btn-2", "Uno-1-3", "Push-2-pinP0", "-612,-380,-692,-380,-692,-260,-756,-260")
    out += connector("Connector-btn-2-g", "Push-2-switch0pinN", "Ground-2-Gnd", "-724,-260,-740,-260,-740,-236")
    out += circuit_footer()
    return out


def lab2_variant1_sim1(program: str) -> str:
    out = circuit_header(animate=1)
    out += uno(program, pos="-620,-420")
    out += serial_port("-840,-500")
    out += text(
        "Text-1",
        "-840,-340",
        "ЛР2 вариант 1\nSimulIDE не содержит LM35,\nпоэтому используется эмулятор LM35:\nпотенциометр 0..1.5V на A0",
    )
    out += potentiometer("Pot-1", "-300,-520", "LM35 emu", "10 kΩ", "3500 Ω")
    out += rail("Rail-1", "-240,-520", "1.5 V")
    out += ground("Ground-1", "-360,-500")
    out += push("Push-1", "-840,-260", "START D2", "s")
    out += ground("Ground-2", "-840,-220")
    out += serial_connectors()
    out += connector("Connector-pot-vcc", "Rail-1-outnod", "Pot-1-PinB", "-240,-504,-240,-468,-284,-468,-284,-520")
    out += connector("Connector-pot-gnd", "Ground-1-Gnd", "Pot-1-PinA", "-360,-484,-360,-520,-316,-520")
    out += connector("Connector-pot-sig", "Pot-1-PinM", "Uno-1-A0", "-300,-504,-300,-236,-612,-236")
    out += connector("Connector-btn", "Uno-1-2", "Push-1-pinP0", "-612,-388,-700,-388,-700,-260,-856,-260")
    out += connector("Connector-btn-g", "Push-1-switch0pinN", "Ground-2-Gnd", "-824,-260,-840,-260,-840,-236")
    out += circuit_footer()
    return out


def lab2_variant2_sim1(program: str) -> str:
    out = circuit_header(animate=1)
    out += uno(program, pos="-620,-420")
    out += serial_port("-840,-500")
    out += text(
        "Text-1",
        "-840,-340",
        "ЛР2 вариант 2\nКнопка D2 делает выборку\nПоворачивайте потенциометр\nВ SerialPort введите d или h",
    )
    out += potentiometer("Pot-1", "-300,-520", "A0 Pot", "10 kΩ", "5000 Ω")
    out += rail("Rail-1", "-240,-520", "5 V")
    out += ground("Ground-1", "-360,-500")
    out += push("Push-1", "-840,-260", "SAMPLE D2", "m")
    out += ground("Ground-2", "-840,-220")
    out += serial_connectors()
    out += connector("Connector-pot-vcc", "Rail-1-outnod", "Pot-1-PinB", "-240,-504,-240,-468,-284,-468,-284,-520")
    out += connector("Connector-pot-gnd", "Ground-1-Gnd", "Pot-1-PinA", "-360,-484,-360,-520,-316,-520")
    out += connector("Connector-pot-sig", "Pot-1-PinM", "Uno-1-A0", "-300,-504,-300,-236,-612,-236")
    out += connector("Connector-btn", "Uno-1-2", "Push-1-pinP0", "-612,-388,-700,-388,-700,-260,-856,-260")
    out += connector("Connector-btn-g", "Push-1-switch0pinN", "Ground-2-Gnd", "-824,-260,-840,-260,-840,-236")
    out += circuit_footer()
    return out


def lab3_sim1(program: str, accumulate: bool) -> str:
    note = (
        "ЛР3 CRC-8 accumulate\nОтправляйте данные в SerialPort\nКнопка D2 печатает CRC\nCRC не сбрасывается"
        if accumulate
        else "ЛР3 CRC-8 reset\nОтправляйте данные в SerialPort\nКнопка D2 печатает CRC\nПосле вывода CRC сбрасывается"
    )
    out = circuit_header(animate=1)
    out += uno(program, pos="-620,-420")
    out += serial_port("-840,-500")
    out += text("Text-1", "-840,-340", note)
    out += push("Push-1", "-840,-260", "CRC D2", "c")
    out += ground("Ground-1", "-840,-220")
    out += serial_connectors()
    out += connector("Connector-btn", "Uno-1-2", "Push-1-pinP0", "-612,-388,-700,-388,-700,-260,-856,-260")
    out += connector("Connector-btn-g", "Push-1-switch0pinN", "Ground-1-Gnd", "-824,-260,-840,-260,-840,-236")
    out += circuit_footer()
    return out


def lab4_sim1(program: str) -> str:
    out = circuit_header(animate=1)
    out += uno(program, pos="-640,-420")
    out += text(
        "Text-1",
        "-930,-330",
        "ЛР4 вариант 2\nМеняйте освещенность LDR\nКоличество LED зависит от A0",
    )
    out += rail("Rail-1", "-330,-560", "5 V")
    out += ldr("LDR-1", "-330,-500")
    out += resistor("Resistor-ldr", "-330,-400", "10 kΩ", rotation=90)
    out += ground("Ground-ldr", "-330,-320")
    out += node("Node-a0", "-330,-448")
    out += connector("Connector-ldr-vcc", "Rail-1-outnod", "LDR-1-lPin", "-330,-544,-330,-516")
    out += connector("Connector-ldr-a0", "LDR-1-rPin", "Node-a0-0", "-330,-484,-330,-448")
    out += connector("Connector-res-a0", "Resistor-ldr-lPin", "Node-a0-1", "-330,-416,-330,-448")
    out += connector("Connector-res-gnd", "Resistor-ldr-rPin", "Ground-ldr-Gnd", "-330,-384,-330,-336")
    out += connector("Connector-a0-uno", "Node-a0-2", "Uno-1-A0", "-330,-448,-612,-448,-612,-236")

    pins = list(range(6, 14))
    y_values = [-580, -540, -500, -460, -420, -380, -340, -300]
    for i, (pin, y) in enumerate(zip(pins, y_values)):
        out += resistor(f"Resistor-{i+1}", f"-200,{y}", "220 Ω")
        out += led(f"LED{i+1}", f"-80,{y}", "Red")
        out += ground(f"Ground-led{i+1}", f"20,{y + 16}")
        out += connector(
            f"Connector-led-src-{i}",
            f"Uno-1-{pin}",
            f"Resistor-{i+1}-lPin",
            f"-612,{y + 4},-320,{y + 4},-320,{y},-216,{y}",
        )
        out += connector(
            f"Connector-led-mid-{i}",
            f"Resistor-{i+1}-rPin",
            f"LED{i+1}-lPin",
            f"-184,{y},-96,{y}",
        )
        out += connector(
            f"Connector-led-gnd-{i}",
            f"LED{i+1}-rPin",
            f"Ground-led{i+1}-Gnd",
            f"-64,{y},20,{y},20,{y + 16}",
        )

    out += circuit_footer()
    return out


def readme_text() -> str:
    return """# Готовые проекты SimulIDE

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
"""


def generate_sim1(name: str) -> str:
    if name == "lab1_variant1":
        return lab1_sim1("lab1_variant1.hex", "ЛР1 вариант 1")
    if name == "lab1_variant2":
        return lab1_sim1("lab1_variant2.hex", "ЛР1 вариант 2")
    if name == "lab2_variant1":
        return lab2_variant1_sim1("lab2_variant1.hex")
    if name == "lab2_variant2":
        return lab2_variant2_sim1("lab2_variant2.hex")
    if name == "lab3_crc8_reset":
        return lab3_sim1("lab3_crc8_reset.hex", accumulate=False)
    if name == "lab3_crc8_accumulate":
        return lab3_sim1("lab3_crc8_accumulate.hex", accumulate=True)
    if name == "lab4_variant2":
        return lab4_sim1("lab4_variant2.hex")
    raise KeyError(name)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "README.md").write_text(readme_text(), encoding="utf-8")

    for name, meta in PROJECTS.items():
        folder = OUT / name
        folder.mkdir(parents=True, exist_ok=True)
        sim1_path = folder / f"{name}.sim1"
        ino_path = folder / f"{name}.ino"
        hex_path = folder / f"{name}.hex"

        sim1_path.write_text(generate_sim1(name), encoding="utf-8")
        shutil.copy2(meta["sketch"], ino_path)
        shutil.copy2(meta["hex"], hex_path)
        print(f"Prepared {sim1_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
