"""
Create Placeholder Images for Portfolio
This script creates simple placeholder images for your projects
Install Pillow first: pip install Pillow
Usage: python create_images.py
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder_image(filename, title, color, size=(800, 500)):
    """Create a simple placeholder image with text"""
    
    # Create image with gradient background
    img = Image.new('RGB', size, color)
    draw = ImageDraw.Draw(img)
    
    # Add darker overlay for better text visibility
    overlay = Image.new('RGBA', size, (0, 0, 0, 100))
    img.paste(overlay, (0, 0), overlay)
    
    # Try to use a nice font, fallback to default
    try:
        # Adjust font size based on title length
        font_size = 40 if len(title) < 30 else 32
        font = ImageFont.truetype("arial.ttf", font_size)
        small_font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Add project title
    text_bbox = draw.textbbox((0, 0), title, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Center the text
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    # Draw text with shadow for better visibility
    draw.text((x+2, y+2), title, fill=(0, 0, 0), font=font)
    draw.text((x, y), title, fill=(255, 255, 255), font=font)
    
    # Add "ByCodeHub" watermark
    watermark = "ByCodeHub Project"
    wm_bbox = draw.textbbox((0, 0), watermark, font=small_font)
    wm_width = wm_bbox[2] - wm_bbox[0]
    wm_x = (size[0] - wm_width) // 2
    wm_y = y + text_height + 30
    
    draw.text((wm_x, wm_y), watermark, fill=(200, 200, 200), font=small_font)
    
    return img


def create_all_placeholders():
    """Create placeholder images for all projects"""
    
    # Create images directory if it doesn't exist
    images_dir = 'static/images'
    os.makedirs(images_dir, exist_ok=True)
    
    # Define project images with colors
    projects = [
        ('agro-hub.jpg', 'Agro-Hub', (34, 139, 34)),  # Green
        ('maatri-suraksha.jpg', 'Maatri Suraksha', (255, 105, 180)),  # Pink
        ('demand-forecast.jpg', 'Demand Forecasting', (30, 144, 255)),  # Blue
        ('juggle-ai.jpg', 'Juggle.AI', (138, 43, 226)),  # Purple
        ('ecommerce.jpg', 'E-Commerce Platform', (255, 140, 0)),  # Orange
        ('hospital-mgmt.jpg', 'Hospital Management', (220, 20, 60)),  # Red
        ('disease-predict.jpg', 'Disease Prediction', (46, 139, 87)),  # Sea Green
        ('sentiment-analysis.jpg', 'Sentiment Analysis', (70, 130, 180)),  # Steel Blue
        ('fitness-tracker.jpg', 'Fitness Tracker', (255, 69, 0)),  # Red Orange
        ('attendance-app.jpg', 'Attendance System', (75, 0, 130)),  # Indigo
        ('food-delivery.jpg', 'Food Delivery', (255, 215, 0)),  # Gold
        ('stock-predict.jpg', 'Stock Prediction', (0, 128, 128)),  # Teal
        ('library-mgmt.jpg', 'Library Management', (139, 69, 19)),  # Brown
        ('weather-app.jpg', 'Weather App', (135, 206, 235)),  # Sky Blue
        ('exam-portal.jpg', 'Exam Portal', (128, 0, 128)),  # Purple
    ]
    
    print("🎨 Creating placeholder images...")
    print("="*60)
    
    created_count = 0
    for filename, title, color in projects:
        filepath = os.path.join(images_dir, filename)
        
        if os.path.exists(filepath):
            print(f"⊘ Skipped (already exists): {filename}")
        else:
            img = create_placeholder_image(filename, title, color)
            img.save(filepath, quality=95)
            created_count += 1
            print(f"✓ Created: {filename}")
    
    print("\n" + "="*60)
    print(f"✅ Created {created_count} new placeholder images!")
    
    # Create additional essential images
    create_essential_images(images_dir)


def create_essential_images(images_dir):
    """Create essential images (logo, favicon, placeholder)"""
    
    print("\n📦 Creating essential images...")
    print("-"*60)
    
    # Create logo
    logo_path = os.path.join(images_dir, 'logo.png')
    if not os.path.exists(logo_path):
        logo = Image.new('RGB', (200, 200), (77, 163, 255))
        draw = ImageDraw.Draw(logo)
        
        # Draw a simple "BC" for ByCodeHub
        try:
            font = ImageFont.truetype("arial.ttf", 80)
        except:
            font = ImageFont.load_default()
        
        text = "BC"
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        x = (200 - text_width) // 2
        y = (200 - text_height) // 2
        
        draw.text((x, y), text, fill=(255, 255, 255), font=font)
        logo.save(logo_path, quality=95)
        print(f"✓ Created: logo.png")
    else:
        print(f"⊘ Skipped: logo.png (already exists)")
    
    # Create favicon
    favicon_path = os.path.join(images_dir, 'favicon.png')
    if not os.path.exists(favicon_path):
        favicon = Image.new('RGB', (64, 64), (77, 163, 255))
        draw = ImageDraw.Draw(favicon)
        
        try:
            font = ImageFont.truetype("arial.ttf", 32)
        except:
            font = ImageFont.load_default()
        
        text = "BC"
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        x = (64 - text_width) // 2
        y = (64 - text_height) // 2
        
        draw.text((x, y), text, fill=(255, 255, 255), font=font)
        favicon.save(favicon_path, quality=95)
        print(f"✓ Created: favicon.png")
    else:
        print(f"⊘ Skipped: favicon.png (already exists)")
    
    # Create generic project placeholder
    placeholder_path = os.path.join(images_dir, 'project-placeholder.jpg')
    if not os.path.exists(placeholder_path):
        placeholder = create_placeholder_image(
            'project-placeholder.jpg',
            'ByCodeHub Project',
            (50, 50, 50)
        )
        placeholder.save(placeholder_path, quality=95)
        print(f"✓ Created: project-placeholder.jpg")
    else:
        print(f"⊘ Skipped: project-placeholder.jpg (already exists)")


def create_gradient_image(filename, title, start_color, end_color, size=(800, 500)):
    """Create an image with gradient background"""
    
    img = Image.new('RGB', size)
    draw = ImageDraw.Draw(img)
    
    # Create gradient
    for y in range(size[1]):
        r = int(start_color[0] + (end_color[0] - start_color[0]) * y / size[1])
        g = int(start_color[1] + (end_color[1] - start_color[1]) * y / size[1])
        b = int(start_color[2] + (end_color[2] - start_color[2]) * y / size[1])
        draw.line([(0, y), (size[0], y)], fill=(r, g, b))
    
    # Add text
    try:
        font = ImageFont.truetype("arial.ttf", 40)
        small_font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    text_bbox = draw.textbbox((0, 0), title, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    # Text with shadow
    draw.text((x+2, y+2), title, fill=(0, 0, 0), font=font)
    draw.text((x, y), title, fill=(255, 255, 255), font=font)
    
    watermark = "ByCodeHub"
    wm_bbox = draw.textbbox((0, 0), watermark, font=small_font)
    wm_width = wm_bbox[2] - wm_bbox[0]
    wm_x = (size[0] - wm_width) // 2
    wm_y = y + text_height + 30
    
    draw.text((wm_x, wm_y), watermark, fill=(220, 220, 220), font=small_font)
    
    return img


if __name__ == '__main__':
    try:
        print("🚀 Starting Image Creation Process...")
        print("="*60)
        print("📦 Required: PIL/Pillow library")
        print("   Install with: pip install Pillow")
        print("="*60 + "\n")
        
        create_all_placeholders()
        
        print("\n✅ Image creation completed successfully!")
        print("\n📁 All images saved to: static/images/")
        print("\n💡 You can now:")
        print("   1. Replace these placeholders with your own images")
        print("   2. Keep the same filenames")
        print("   3. Or update image_url in the database")
        print("\n🎉 Your portfolio is ready with placeholder images!")
        
    except ImportError:
        print("\n❌ Error: Pillow library not found!")
        print("\n📦 Please install it first:")
        print("   pip install Pillow")
        print("\nThen run this script again.")
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        print("\n💡 Make sure:")
        print("   1. You're in the project root directory")
        print("   2. The 'static/images' folder exists")
        print("   3. You have write permissions")