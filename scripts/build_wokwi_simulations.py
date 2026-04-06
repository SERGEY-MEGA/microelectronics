#!/usr/bin/env python3
"""Generate deliverables/wokwi-simulations/*/diagram.json from templates."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables" / "wokwi-simulations"
LABS = ROOT / "labs"


def base_meta() -> dict:
    return {
        "version": 1,
        "author": "SERGEY-MEGA/microelectronics",
        "editor": "wokwi",
    }


def lab1_diagram() -> dict:
    parts = [
        {"type": "wokwi-arduino-uno", "id": "uno", "left": 40, "top": 40},
    ]
    conns: list[list] = []
    for i in range(6):
        pin = str(8 + i)
        top = 30 + i * 45
        parts += [
            {
                "type": "wokwi-resistor",
                "id": f"r{i}",
                "left": 300,
                "top": top,
                "attrs": {"value": "220"},
            },
            {
                "type": "wokwi-led",
                "id": f"led{i}",
                "left": 400,
                "top": top,
                "attrs": {"color": "red"},
            },
        ]
        conns += [
            [f"uno:{pin}", f"r{i}:1", "green", []],
            [f"r{i}:2", f"led{i}:A", "green", []],
            [f"led{i}:C", "uno:GND.1", "black", []],
        ]
    parts += [
        {
            "type": "wokwi-pushbutton",
            "id": "btnA",
            "left": 40,
            "top": 300,
            "attrs": {"color": "green", "label": "D2", "key": "1"},
        },
        {
            "type": "wokwi-pushbutton",
            "id": "btnB",
            "left": 160,
            "top": 300,
            "attrs": {"color": "blue", "label": "D3", "key": "2"},
        },
    ]
    conns += [
        ["uno:2", "btnA:1.r", "green", []],
        ["btnA:2.r", "uno:GND.2", "black", []],
        ["uno:3", "btnB:1.r", "green", []],
        ["btnB:2.r", "uno:GND.3", "black", []],
    ]
    d = base_meta()
    d["parts"] = parts
    d["connections"] = conns
    return d


def lab2_v1_diagram() -> dict:
    parts = [
        {"type": "wokwi-arduino-uno", "id": "uno", "left": 40, "top": 40},
        {
            "type": "wokwi-potentiometer",
            "id": "pot1",
            "left": 380,
            "top": 40,
            "attrs": {"value": "512"},
        },
        {
            "type": "wokwi-pushbutton",
            "id": "btn1",
            "left": 40,
            "top": 280,
            "attrs": {"color": "red", "label": "START D2", "key": "s"},
        },
    ]
    conns = [
        ["uno:5V", "pot1:VCC", "red", []],
        ["pot1:GND", "uno:GND.1", "black", []],
        ["pot1:SIG", "uno:A0", "orange", []],
        ["uno:2", "btn1:1.r", "green", []],
        ["btn1:2.r", "uno:GND.2", "black", []],
    ]
    d = base_meta()
    d["parts"] = parts
    d["connections"] = conns
    d["serialMonitor"] = {"display": "always", "collapse": False}
    return d


def lab2_v2_diagram() -> dict:
    parts = [
        {"type": "wokwi-arduino-uno", "id": "uno", "left": 40, "top": 40},
        {
            "type": "wokwi-potentiometer",
            "id": "pot1",
            "left": 380,
            "top": 40,
            "attrs": {"value": "512"},
        },
        {
            "type": "wokwi-pushbutton",
            "id": "btn1",
            "left": 40,
            "top": 280,
            "attrs": {"color": "green", "label": "SAMPLE D2", "key": "m"},
        },
    ]
    conns = [
        ["uno:5V", "pot1:VCC", "red", []],
        ["pot1:GND", "uno:GND.1", "black", []],
        ["pot1:SIG", "uno:A0", "orange", []],
        ["uno:2", "btn1:1.r", "green", []],
        ["btn1:2.r", "uno:GND.2", "black", []],
    ]
    d = base_meta()
    d["parts"] = parts
    d["connections"] = conns
    d["serialMonitor"] = {"display": "always", "collapse": False}
    return d


def lab3_diagram() -> dict:
    parts = [
        {"type": "wokwi-arduino-uno", "id": "uno", "left": 80, "top": 60},
        {
            "type": "wokwi-pushbutton",
            "id": "btn1",
            "left": 80,
            "top": 280,
            "attrs": {"color": "yellow", "label": "CRC D2", "key": "c"},
        },
    ]
    conns = [
        ["uno:2", "btn1:1.r", "green", []],
        ["btn1:2.r", "uno:GND.1", "black", []],
    ]
    d = base_meta()
    d["parts"] = parts
    d["connections"] = conns
    d["serialMonitor"] = {
        "display": "always",
        "newline": "none",
        "collapse": False,
    }
    return d


def lab4_diagram() -> dict:
    parts = [
        {"type": "wokwi-arduino-uno", "id": "uno", "left": 20, "top": 40},
        {
            "type": "wokwi-photoresistor-sensor",
            "id": "ldr1",
            "left": 420,
            "top": 20,
            "attrs": {"lux": "800"},
        },
    ]
    conns = [
        ["uno:5V", "ldr1:VCC", "red", []],
        ["ldr1:GND", "uno:GND.1", "black", []],
        ["ldr1:AO", "uno:A0", "orange", []],
    ]
    for i in range(8):
        pin = str(6 + i)
        top = 40 + i * 38
        parts += [
            {
                "type": "wokwi-resistor",
                "id": f"r{i}",
                "left": 260,
                "top": top,
                "attrs": {"value": "220"},
            },
            {
                "type": "wokwi-led",
                "id": f"led{i}",
                "left": 340,
                "top": top,
                "attrs": {"color": "red"},
            },
        ]
        conns += [
            [f"uno:{pin}", f"r{i}:1", "green", []],
            [f"r{i}:2", f"led{i}:A", "green", []],
            [f"led{i}:C", "uno:GND.2", "black", []],
        ]
    d = base_meta()
    d["parts"] = parts
    d["connections"] = conns
    return d


SKETCH_SOURCES = {
    "lab1_variant1": LABS / "lab1" / "variant1" / "lab1_variant1" / "lab1_variant1.ino",
    "lab1_variant2": LABS / "lab1" / "variant2" / "lab1_variant2" / "lab1_variant2.ino",
    "lab2_variant1": LABS / "lab2" / "variant1" / "lab2_variant1" / "lab2_variant1.ino",
    "lab2_variant2": LABS / "lab2" / "variant2" / "lab2_variant2" / "lab2_variant2.ino",
    "lab3_crc8_reset": LABS / "lab3" / "erofeev" / "lab3_crc8_reset" / "lab3_crc8_reset.ino",
    "lab3_crc8_accumulate": LABS / "lab3" / "erofeev" / "lab3_crc8_accumulate" / "lab3_crc8_accumulate.ino",
    "lab4_variant2": LABS / "lab4" / "variant2" / "lab4_variant2" / "lab4_variant2.ino",
}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    diagrams: list[tuple[str, dict]] = [
        ("lab1_variant1", lab1_diagram()),
        ("lab1_variant2", lab1_diagram()),
        ("lab2_variant1", lab2_v1_diagram()),
        ("lab2_variant2", lab2_v2_diagram()),
        ("lab3_crc8_reset", lab3_diagram()),
        ("lab3_crc8_accumulate", lab3_diagram()),
        ("lab4_variant2", lab4_diagram()),
    ]
    for name, diagram in diagrams:
        folder = OUT / name
        folder.mkdir(parents=True, exist_ok=True)
        target_json = folder / "diagram.json"
        target_json.write_text(
            json.dumps(diagram, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        src_ino = SKETCH_SOURCES[name]
        shutil.copy2(src_ino, folder / "sketch.ino")
        print(f"Wrote {target_json.relative_to(ROOT)} + sketch.ino")


if __name__ == "__main__":
    main()
