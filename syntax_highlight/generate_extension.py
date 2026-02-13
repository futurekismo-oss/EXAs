#!/usr/bin/env python3
"""
Auto-generate VS Code syntax highlighting extension for EXA language
Reads opcodes from data.json and creates the extension structure
"""

import json
import os
import shutil

# Read opcodes from data.json
with open("../data.json", "r") as f:
    data = json.load(f)
    opcodes = list(data["opcodes"].keys())

# Create extension directory
ext_dir = "exa-extension"
if os.path.exists(ext_dir):
    shutil.rmtree(ext_dir)
os.makedirs(ext_dir)
os.makedirs(f"{ext_dir}/syntaxes")

# Generate package.json
package_json = {
    "name": "exa-assembly",
    "displayName": "EXA Assembly",
    "description": "Syntax highlighting for EXA assembly language (.ac files)",
    "version": "0.0.1",
    "engines": {
        "vscode": "^1.60.0"
    },
    "categories": ["Programming Languages"],
    "contributes": {
        "languages": [{
            "id": "exa",
            "aliases": ["EXA", "exa"],
            "extensions": [".ac"],
            "configuration": "./language-configuration.json"
        }],
        "grammars": [{
            "language": "exa",
            "scopeName": "source.exa",
            "path": "./syntaxes/exa.tmLanguage.json"
        }]
    }
}

with open(f"{ext_dir}/package.json", "w") as f:
    json.dump(package_json, f, indent=2)

# Generate tmLanguage.json
keyword_pattern = "\\b(" + "|".join(opcodes) + ")\\b"

tmlanguage = {
    "$schema": "https://raw.githubusercontent.com/martinring/tmlanguage/master/tmlanguage.json",
    "name": "EXA",
    "patterns": [
        {"include": "#comments"},
        {"include": "#labels"},
        {"include": "#keywords"},
        {"include": "#registers"},
        {"include": "#numbers"},
        {"include": "#strings"}
    ],
    "repository": {
        "comments": {
            "name": "comment.line.exa",
            "match": "<<.*$"
        },
        "labels": {
            "name": "entity.name.label.exa",
            "match": "^[a-zA-Z_][a-zA-Z0-9_]*:"
        },
        "keywords": {
            "patterns": [{
                "name": "keyword.control.exa",
                "match": keyword_pattern
            }]
        },
        "registers": {
            "name": "variable.parameter.exa",
            "match": "\\b[a-zA-Z_][a-zA-Z0-9_]*\\b"
        },
        "numbers": {
            "name": "constant.numeric.exa",
            "match": "\\b-?[0-9]+\\b"
        },
        "strings": {
            "name": "string.quoted.double.exa",
            "begin": "\"",
            "end": "\"",
            "patterns": [{
                "name": "constant.character.escape.exa",
                "match": "\\\\."
            }]
        }
    },
    "scopeName": "source.exa"
}

with open(f"{ext_dir}/syntaxes/exa.tmLanguage.json", "w") as f:
    json.dump(tmlanguage, f, indent=2)

# Generate language-configuration.json
lang_config = {
    "comments": {
        "lineComment": "<<"
    },
    "brackets": [],
    "autoClosingPairs": [
        ["\"", "\""]
    ],
    "surroundingPairs": [
        ["\"", "\""]
    ]
}

with open(f"{ext_dir}/language-configuration.json", "w") as f:
    json.dump(lang_config, f, indent=2)

# Generate README.md
readme = """# EXA Assembly Language Support

Syntax highlighting for EXA assembly language (.ac files).

## Features

- Syntax highlighting for all EXA instructions
- Comment support with <<
- Label highlighting
- Register and number highlighting
- String support

## Instructions Supported

{}

## Usage

Files with `.ac` extension will automatically use EXA syntax highlighting.
""".format(", ".join(sorted(opcodes)))

with open(f"{ext_dir}/README.md", "w") as f:
    f.write(readme)

print("✓ Extension generated in exa-extension/")
print(f"✓ Found {len(opcodes)} instructions")
print("\nNext steps:")
print("1. cd exa-extension")
print("2. vsce package --allow-missing-repository")
print("3. code --install-extension exa-assembly-*.vsix")
