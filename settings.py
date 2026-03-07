import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Hashmaps, located in json files
with open(os.path.join(BASE_DIR, "data.json"), "r") as data:
    data = json.load(data)

    OPCODES = data["opcodes"]
    COLORS = data["terminal_colors"]
    ARG = data["argument_n"]


color = {
    "r": COLORS["red"],
    "g": COLORS["green"],
    "b": COLORS["blue"],
    "y": COLORS["yellow"],
    "reset": COLORS["reset"],
}
