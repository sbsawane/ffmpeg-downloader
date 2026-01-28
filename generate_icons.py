"""
Generate PNG icons for browser extension
Uses Pillow to create simple but attractive icons
"""

import os
import sys

def generate_icons():
    """Generate PNG icons programmatically"""
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        print("Installing Pillow...")
        os.system(f"{sys.executable} -m pip install pillow")
        from PIL import Image, ImageDraw
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    icons_dir = os.path.join(script_dir, "extension", "icons")
    
    os.makedirs(icons_dir, exist_ok=True)
    
    sizes = [16, 32, 48, 128]
    
    print("Generating PNG icons...")
    print()
    
    for size in sizes:
        output_path = os.path.join(icons_dir, f"icon-{size}.png")
        
        # Create image with transparent background
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Scale factor
        s = size / 128
        
        # Draw green circle background
        padding = int(4 * s)
        draw.ellipse(
            [padding, padding, size - padding, size - padding],
            fill='#4CAF50'
        )
        
        # Draw download arrow
        cx, cy = size // 2, size // 2
        arrow_width = int(10 * s)
        arrow_height = int(40 * s)
        head_size = int(20 * s)
        
        # Arrow shaft
        shaft_top = int(25 * s)
        shaft_bottom = int(70 * s)
        draw.rectangle(
            [cx - arrow_width//2, shaft_top, cx + arrow_width//2, shaft_bottom],
            fill='white'
        )
        
        # Arrow head (triangle)
        arrow_tip_y = int(85 * s)
        draw.polygon([
            (cx, arrow_tip_y),  # tip
            (cx - head_size, shaft_bottom - int(5*s)),  # left
            (cx + head_size, shaft_bottom - int(5*s)),  # right
        ], fill='white')
        
        # Draw tray/base
        tray_y = int(90 * s)
        tray_left = int(25 * s)
        tray_right = int(103 * s)
        tray_bottom = int(100 * s)
        line_width = max(2, int(6 * s))
        
        # Left side of tray
        draw.line([(tray_left, tray_y), (tray_left, tray_bottom)], fill='white', width=line_width)
        # Bottom of tray
        draw.line([(tray_left, tray_bottom), (tray_right, tray_bottom)], fill='white', width=line_width)
        # Right side of tray
        draw.line([(tray_right, tray_y), (tray_right, tray_bottom)], fill='white', width=line_width)
        
        # Small play icon in corner (for video indicator)
        if size >= 32:
            play_x = int(85 * s)
            play_y = int(25 * s)
            play_size = int(18 * s)
            draw.polygon([
                (play_x, play_y),
                (play_x + play_size, play_y + play_size//2),
                (play_x, play_y + play_size),
            ], fill='white')
        
        # Save
        img.save(output_path, 'PNG')
        print(f"  ✓ Created: icon-{size}.png ({size}x{size})")
    
    print()
    print("All icons generated successfully!")
    return True

if __name__ == "__main__":
    success = generate_icons()
    
    if success:
        print()
        print("Next steps:")
        print("  1. Run: build-firefox.bat (for Firefox)")
        print("  2. Reload extension in browser")
    
    sys.exit(0 if success else 1)
