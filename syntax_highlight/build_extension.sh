#!/bin/bash
# Build and package EXA VS Code extension

echo "🔧 Generating extension from data.json..."
python3 generate_extension.py

if [ $? -ne 0 ]; then
    echo "❌ Extension generation failed"
    exit 1
fi

echo ""
echo "📦 Packaging extension..."
cd exa-extension
vsce package --allow-missing-repository

if [ $? -ne 0 ]; then
    echo "❌ Packaging failed. Make sure vsce is installed:"
    echo "   npm install -g @vscode/vsce"
    exit 1
fi

echo ""
echo "✅ Extension built successfully!"
echo ""
echo "📁 Install with:"
echo "   code --install-extension exa-extension/exa-assembly-*.vsix"
echo ""
echo "💾 Or commit the .vsix to your repo for syncing across machines"
