#!/bin/bash
# Install native host for Firefox on Mac/Linux

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
HOST_NAME="com.my_downloader"

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    TARGET_DIR="$HOME/Library/Application Support/Mozilla/NativeMessagingHosts"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    TARGET_DIR="$HOME/.mozilla/native-messaging-hosts"
else
    echo "Unsupported OS: $OSTYPE"
    exit 1
fi

echo "Installing Firefox native host..."
echo "Script directory: $SCRIPT_DIR"
echo "Target directory: $TARGET_DIR"

# Create target directory if it doesn't exist
mkdir -p "$TARGET_DIR"

# Create manifest with correct path
cat > "$TARGET_DIR/$HOST_NAME.json" << EOF
{
  "name": "$HOST_NAME",
  "description": "FFmpeg Native Host for Firefox",
  "path": "$SCRIPT_DIR/start_host.sh",
  "type": "stdio",
  "allowed_extensions": [
    "ffmpeg-downloader@example.com"
  ]
}
EOF

# Make start script executable
chmod +x "$SCRIPT_DIR/start_host.sh"

echo ""
echo "✓ Firefox native host installed successfully!"
echo ""
echo "IMPORTANT: Update the extension ID in:"
echo "  $TARGET_DIR/$HOST_NAME.json"
echo ""
echo "To find your extension ID:"
echo "  1. Go to about:debugging in Firefox"
echo "  2. Find your extension"
echo "  3. Copy the Extension ID (UUID)"
echo "  4. Replace 'ffmpeg-downloader@example.com' with your ID"
