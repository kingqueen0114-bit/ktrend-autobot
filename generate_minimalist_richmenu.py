from PIL import Image, ImageDraw, ImageFont

def create_rich_menu_image(output_path="assets/rich_menu_v7_minimal.png"):
    # Size for LINE rich menu: 2500x1686 (Large standard format)
    # Since the user wants a single row of 3 "square" buttons, we use
    # a half-height menu layout: 2500 x 843
    width = 2500
    height = 843
    
    # Create new image with a white background
    img = Image.new('RGB', (width, height), color='#ffffff')
    draw = ImageDraw.Draw(img)
    
    # Clean, stylish color palette
    text_color = '#111111'   # Deep black
    border_color = '#111111' # Black border for the buttons
    
    # Grid sizes: 3 columns, full height
    cell_w = width // 3
    
    # Draw Background (already white)
    
    # Draw sleek, black borders around each button
    # Left button
    draw.rectangle([0, 0, cell_w, height], outline=border_color, width=6)
    # Middle button
    draw.rectangle([cell_w, 0, cell_w * 2, height], outline=border_color, width=6)
    # Right button
    draw.rectangle([cell_w * 2, 0, width, height], outline=border_color, width=6)
    
    # Load Fonts
    # K-Trend Times likely uses a clean Mincho (Serif) or modern Gothic (Sans-Serif).
    # We will try to load a beautiful Japanese Mincho or default to a sleek Sans.
    try:
        # Try a sleek Serif style for a "magazine" feel
        font_main = ImageFont.truetype("/System/Library/Fonts/Hiragino Mincho ProN.ttc", 130)
    except:
        try:
            # Fallback to standard clean Arial Unicode or Hiragino Sans
            font_main = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", 140)
        except:
            font_main = ImageFont.load_default()

    # Layout offsets
    cy = height // 2

    # --- Column 1: 記事作成 ---
    draw.text((cell_w // 2, cy), "記事作成", fill=text_color, font=font_main, anchor="mm")
    
    # --- Column 2: 記事一覧 ---
    draw.text((cell_w + cell_w // 2, cy), "記事一覧", fill=text_color, font=font_main, anchor="mm")
    
    # --- Column 3: レポート ---
    draw.text((cell_w * 2 + cell_w // 2, cy), "レポート", fill=text_color, font=font_main, anchor="mm")
    
    # Save Image
    # High-quality save
    img.save(output_path, quality=100)
    print(f"Created minimalist 3-col rich menu image at {output_path}")

if __name__ == "__main__":
    create_rich_menu_image()
