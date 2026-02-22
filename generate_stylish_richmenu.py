from PIL import Image, ImageDraw, ImageFont

def create_rich_menu_image(output_path="assets/rich_menu_v6.png"):
    # Size for LINE rich menu: 2500x1686
    width = 2500
    height = 1686
    
    # Create new image with a background color
    img = Image.new('RGB', (width, height), color='#ffffff')
    draw = ImageDraw.Draw(img)
    
    # Define distinct, stylish color palette for 3 rows
    colors = {
        'row1_bg': '#1e88e5',    # Professional Blue
        'row2_bg': '#43a047',    # Trustworthy Green
        'row3_bg': '#fb8c00',    # Vibrant Orange
        'border': '#ffffff',     # White dividers for clean look
        'text_light': '#ffffff', # White text for dark backgrounds
        'text_sub': '#e0e0e0'    # Slightly dimmed white
    }
    
    # Grid sizes: 3 rows full width
    row_h = height // 3
    
    # Draw Background rows
    draw.rectangle([0, 0, width, row_h], fill=colors['row1_bg'])
    draw.rectangle([0, row_h, width, row_h * 2], fill=colors['row2_bg'])
    draw.rectangle([0, row_h * 2, width, height], fill=colors['row3_bg'])
    
    # Draw bold dividers
    draw.line([(0, row_h), (width, row_h)], fill=colors['border'], width=12)
    draw.line([(0, row_h * 2), (width, row_h * 2)], fill=colors['border'], width=12)
    
    # Load Fonts (Use Arial Unicode which reliably supports Japanese, make sizes huge)
    try:
        font_emoji = ImageFont.truetype("/System/Library/Fonts/Apple Color Emoji.ttc", 350)
    except:
        font_emoji = ImageFont.load_default()
        
    try:
        font_main = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", 200)
        font_sub = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", 100)
    except:
        font_main = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    # Layout offsets
    icon_x = width // 3 - 100
    text_x = width // 2 + 100

    # --- Row 1: 記事作成 (Category) ---
    cy = row_h // 2
    try: draw.text((icon_x, cy), "📝", font=font_emoji, anchor="mm")
    except: pass
    draw.text((text_x, cy - 60), "記事作成", fill=colors['text_light'], font=font_main, anchor="mm")
    draw.text((text_x, cy + 120), "カテゴリから自動生成", fill=colors['text_sub'], font=font_sub, anchor="mm")
    
    # --- Row 2: 記事管理・編集 (Drafts Web UI) ---
    cy = int(row_h * 1.5)
    try: draw.text((icon_x, cy), "🌐", font=font_emoji, anchor="mm")
    except: pass
    draw.text((text_x, cy - 60), "記事一覧・管理", fill=colors['text_light'], font=font_main, anchor="mm")
    draw.text((text_x, cy + 120), "下書き・公開済みの再編集", fill=colors['text_sub'], font=font_sub, anchor="mm")
    
    # --- Row 3: 統計 (Analytics) ---
    cy = int(row_h * 2.5)
    try: draw.text((icon_x, cy), "📊", font=font_emoji, anchor="mm")
    except: pass
    draw.text((text_x, cy - 60), "アクセス統計", fill=colors['text_light'], font=font_main, anchor="mm")
    draw.text((text_x, cy + 120), "PV・収益レポート", fill=colors['text_sub'], font=font_sub, anchor="mm")
    
    # Save Image
    img.save(output_path, quality=95)
    print(f"Created 3-row stylish rich menu image at {output_path}")

if __name__ == "__main__":
    create_rich_menu_image()
