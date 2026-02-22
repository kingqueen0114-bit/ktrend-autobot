from PIL import Image, ImageDraw, ImageFont

def create_rich_menu_image(output_path="assets/rich_menu_v4.png"):
    # Size for LINE rich menu: 2500x1686
    width = 2500
    height = 1686
    
    # Create new image with a background color
    img = Image.new('RGB', (width, height), color='#f0f2f5')
    draw = ImageDraw.Draw(img)
    
    # Colors
    primary_color = '#1DB446' # LINE Verde
    text_color = '#333333'
    white = '#ffffff'
    border_color = '#cccccc'
    
    # Grid: 2 columns, 2 rows
    cell_w = width // 2
    cell_h = height // 2
    
    # Optional: try to load a font, otherwise use default
    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/Hiragino Sans GB.ttc", 100)
        font_emoji = ImageFont.truetype("/System/Library/Fonts/Apple Color Emoji.ttc", 150)
    except:
        font_large = ImageFont.load_default()
        font_emoji = ImageFont.load_default()

    # Draw boxes
    for row in range(2):
        for col in range(2):
            x1 = col * cell_w
            y1 = row * cell_h
            x2 = x1 + cell_w
            y2 = y1 + cell_h
            
            # Fill with white and draw border
            draw.rectangle([x1, y1, x2, y2], fill=white, outline=border_color, width=4)
            
    # Draw content
    # Top Left: 記事作成
    draw.text((cell_w//2, cell_h//2 - 100), "📝", fill=text_color, font=font_emoji, anchor="mm")
    draw.text((cell_w//2, cell_h//2 + 50), "記事作成(カテゴリ)", fill=text_color, font=font_large, anchor="mm")
    
    # Top Right: 統計
    draw.text((cell_w*1.5, cell_h//2 - 100), "📊", fill=text_color, font=font_emoji, anchor="mm")
    draw.text((cell_w*1.5, cell_h//2 + 50), "統計", fill=text_color, font=font_large, anchor="mm")
    
    # Bottom Left: 未公開記事
    draw.text((cell_w//2, cell_h*1.5 - 100), "📬", fill=text_color, font=font_emoji, anchor="mm")
    draw.text((cell_w//2, cell_h*1.5 + 50), "未公開の下書き", fill=text_color, font=font_large, anchor="mm")
    
    # Bottom Right: 記事管理
    # Draw a special background for this new button
    draw.rectangle([cell_w, cell_h, width, height], fill='#e8f5e9', outline=primary_color, width=8)
    draw.text((cell_w*1.5, cell_h*1.5 - 100), "🌐", fill=text_color, font=font_emoji, anchor="mm")
    draw.text((cell_w*1.5, cell_h*1.5 + 50), "記事一覧・管理", fill=primary_color, font=font_large, anchor="mm")
    draw.text((cell_w*1.5, cell_h*1.5 + 180), "(公開済みも編集可能)", fill='#666666', font=ImageFont.truetype("/System/Library/Fonts/Hiragino Sans GB.ttc", 60) if 'font_large' in locals() else ImageFont.load_default(), anchor="mm")
    
    # Save Image
    img.save(output_path)
    print(f"Created rich menu image at {output_path}")

create_rich_menu_image()
