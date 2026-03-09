#!/usr/bin/env python3
"""
Complete rebuild script for EXA VS Code extension
Run from /workspaces/EXAs directory
"""

import json
import os
import shutil
import subprocess
import sys

print("🔧 EXA Extension Builder")
print("=" * 50)

# Ensure we're in the right directory
if not os.path.exists("data.json"):
    print("❌ Error: data.json not found!")
    print("   Run this script from /workspaces/EXAs")
    sys.exit(1)

# Read opcodes from data.json
print("\n📖 Reading data.json...")
with open("data.json", "r") as f:
    data = json.load(f)
    opcodes = list(data["opcodes"].keys())

print(f"   Found {len(opcodes)} instructions: {', '.join(sorted(opcodes))}")

# Create extension directory
ext_dir = "syntax_highlight/exa-extension"
print(f"\n📁 Creating extension in {ext_dir}...")

if os.path.exists(ext_dir):
    shutil.rmtree(ext_dir)
os.makedirs(ext_dir)
os.makedirs(f"{ext_dir}/syntaxes")

# Generate package.json
print("   ✓ Generating package.json")
package_json = {
    "name": "exa-assembly",
    "publisher": "futurekismo",
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
print("   ✓ Generating syntax highlighting rules")
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
            "match": "(?!\\b(" + "|".join(opcodes) + ")\\b)\\b[a-zA-Z_][a-zA-Z0-9_]*\\b"
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
print("   ✓ Generating language configuration")
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
print("   ✓ Generating README")
readme = f"""# EXA Assembly Language Support

Syntax highlighting for EXA assembly language (.ac files).

## Features

- Syntax highlighting for all EXA instructions
- Comment support with <<
- Label highlighting
- Register and number highlighting  
- String support

## Instructions Supported

{', '.join(sorted(opcodes))}

## Usage

Files with `.ac` extension will automatically use EXA syntax highlighting.
"""

with open(f"{ext_dir}/README.md", "w") as f:
    f.write(readme)

# Package the extension
print("\n📦 Packaging extension...")
os.chdir(ext_dir)

try:
    result = subprocess.run(
        ["vsce", "package", "--allow-missing-repository"],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("❌ Packaging failed!")
        print(result.stderr)
        sys.exit(1)
    
    print("   ✓ Extension packaged successfully")
    
except FileNotFoundError:
    print("❌ vsce not found! Install with:")
    print("   npm install -g @vscode/vsce")
    sys.exit(1)

# Find the .vsix file
vsix_files = [f for f in os.listdir(".") if f.endswith(".vsix")]
if not vsix_files:
    print("❌ No .vsix file created!")
    sys.exit(1)

vsix_file = vsix_files[0]

# Uninstall old version
print("\n🗑️  Uninstalling old extension...")
subprocess.run(
    ["code", "--uninstall-extension", "futurekismo.exa-assembly"],
    capture_output=True
)

# Install new version
print("💾 Installing extension...")
result = subprocess.run(
    ["code", "--install-extension", vsix_file],
    capture_output=True,
    text=True
)

if result.returncode == 0:
    print("   ✓ Extension installed successfully")
else:
    print(f"❌ Installation failed: {result.stderr}")
    sys.exit(1)

print("\n✅ Done!")
print("\n📝 Next steps:")
print("   1. Reload VS Code window")
print("   2. Open a .ac file to see syntax highlighting")
print(f"   3. Extension file: {ext_dir}/{vsix_file}")
print("\n💡 Tip: Commit the .vsix to your repo to sync across machines")
