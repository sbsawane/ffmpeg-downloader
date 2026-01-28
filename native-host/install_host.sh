#!/bin/bash
# Install native host for Chrome on Mac/Linux

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
HOST_NAME="com.my_downloader"

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    TARGET_DIR="$HOME/Library/Application Support/Google/Chrome/NativeMessagingHosts"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    TARGET_DIR="$HOME/.config/google-chrome/NativeMessagingHosts"
else
    echo "Unsupported OS: $OSTYPE"
    exit 1
fi

echo "Installing Chrome native host..."
echo "Script directory: $SCRIPT_DIR"
echo "Target directory: $TARGET_DIR"

# Create target directory if it doesn't exist
mkdir -p "$TARGET_DIR"

# Create manifest with correct path
cat > "$TARGET_DIR/$HOST_NAME.json" << EOF
{
  "name": "$HOST_NAME",
  "description": "FFmpeg Native Host",
  "path": "$SCRIPT_DIR/start_host.sh",
  "type": "stdio",
  "allowed_origins": [
    "chrome-extension://YOUR_EXTENSION_ID_HERE/"
  ]
}
EOF

# Make start script executable
chmod +x "$SCRIPT_DIR/start_host.sh"

echo ""
echo "✓ Chrome native host installed successfully!"
echo ""
echo "IMPORTANT: Update the extension ID in:"
echo "  $TARGET_DIR/$HOST_NAME.json"
echo ""
echo "To find your extension ID:"
echo "  1. Go to chrome://extensions"
echo "  2. Enable Developer mode"
echo "  3. Load the extension and copy its ID"
echo "  4. Replace YOUR_EXTENSION_ID_HERE in the manifest"
