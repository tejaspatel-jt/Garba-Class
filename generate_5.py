import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from datetime import datetime
import uuid

# Paths
template_path = "id_card_template.jpg"
receipt_template_path = "receipt_template.png"
photos_path = "Photos"
output_base_path = "Garba_Students"
excel_path = "students.xlsx"

# Create main output directory
if not os.path.exists(output_base_path):
    os.makedirs(output_base_path)

# Create batch folders
batches = ["A", "B", "C", "D"]
for batch in batches:
    batch_path = os.path.join(output_base_path, batch)
    if not os.path.exists(batch_path):
        os.makedirs(batch_path)

# Read data from Excel
df = pd.read_excel(excel_path)

# Font settings for ID card (adjust path to a TrueType font on your system)
font_path = "arial.ttf"  # Ensure this font is available
font_size = 44
font = ImageFont.truetype(font_path, font_size)

# Function to generate ID card
def generate_id_card(row, template_path, output_path):
    # Load template
    template = Image.open(template_path)
    draw = ImageDraw.Draw(template)

    # Coordinates for text and photo (adjust based on template)
    name_pos = (420, 200)
    id_pos = (650, 280)
    batch_pos = (680, 345)
    phone_pos = (420, 400)
    photo_pos = (70, 170)
    photo_size = (300, 300)

    # Draw text
    draw.text(name_pos, f"Name: {row['Name']}", fill="White", font=font)
    draw.text(id_pos, f"{row['ID']}", fill="green", font=font)
    draw.text(batch_pos, f"{row['Batch']}", fill="black", font=font)
    draw.text(phone_pos, f"Phone: {row['Phone']}", fill="blue", font=font)

    # Add photo
    photo_path = os.path.join(photos_path, row['PhotoFilename'])
    if os.path.exists(photo_path):
        photo = Image.open(photo_path)
        photo = photo.resize(photo_size, Image.LANCZOS)
        template.paste(photo, photo_pos)

    # Save ID card
    id_card_path = os.path.join(output_path, f"{row['ID']}_IDCard.jpg")
    template.save(id_card_path)
    return id_card_path

# Function to generate payment receipt PDF
def generate_receipt(row, output_path):
    receipt_path = os.path.join(output_path, f"{row['ID']}_Receipt.pdf")
    c = canvas.Canvas(receipt_path, pagesize=letter)
    c.setFont("Helvetica", 15)

    # Receipt content
    c.drawString(100, 750, "Payment Receipt")
    c.drawString(100, 730, f"Date: {datetime.now().strftime('%Y-%m-%d')}")
    c.drawString(100, 710, f"Student Name: {row['Name']}")
    c.drawString(100, 690, f"Student ID: {row['ID']}")
    c.drawString(100, 670, f"Phone: {row['Phone']}")
    c.drawString(100, 650, f"Batch: {row['Batch']}")
    c.drawString(100, 630, f"Payment Amount: ${row['PaymentAmount']}")
    c.drawString(100, 610, "Thank you for your payment!")

    c.save()
    return receipt_path

# New function to generate image-based payment receipt PDF
# image in pdf is cropped to center now and no text this time.
def generate_receipt_from_image(row, template_path, output_path):
    try:
        template = Image.open(template_path)

        # Resize template to fit letter-sized page (8.5x11 inches at 300 DPI)
        target_height = 3300  # 11 inches at 300 DPI
        target_width = int(target_height * (6480 / 11520))  # Maintain 9:16 aspect ratio
        resized_template = template.resize((target_width, target_height), Image.LANCZOS)

        # Draw text on resized template
        draw = ImageDraw.Draw(resized_template)

        # Coordinates for text (scaled for resized template: 1860x3300 pixels)
        scale_factor = target_width / 6480  # ~0.287
        date_pos = (int(200 * scale_factor), int(200 * scale_factor))
        name_pos = (int(200 * scale_factor), int(400 * scale_factor))
        id_pos = (int(200 * scale_factor), int(600 * scale_factor))
        phone_pos = (int(200 * scale_factor), int(800 * scale_factor))
        batch_pos = (int(200 * scale_factor), int(1000 * scale_factor))
        amount_pos = (int(200 * scale_factor), int(1200 * scale_factor))

        # Use larger font for visibility
        receipt_font_size = 60
        receipt_font = ImageFont.truetype(font_path, receipt_font_size)

        # Draw text
        draw.text(date_pos, f"Date: {datetime.now().strftime('%Y-%m-%d')}", fill="black", font=receipt_font)
        draw.text(name_pos, f"Name: {row['Name']}", fill="black", font=receipt_font)
        draw.text(id_pos, f"ID: {row['ID']}", fill="black", font=receipt_font)
        draw.text(phone_pos, f"Phone: {row['Phone']}", fill="black", font=receipt_font)
        draw.text(batch_pos, f"Batch: {row['Batch']}", fill="black", font=receipt_font)
        draw.text(amount_pos, f"Payment Amount: ${row['PaymentAmount']}", fill="black", font=receipt_font)

        # Save temporary image as PNG
        temp_image_path = os.path.join(output_path, f"{row['ID']}_temp_receipt.png")
        resized_template.save(temp_image_path, format="PNG")

        # Create PDF
        receipt_path = os.path.join(output_path, f"{row['ID']}_Receipt_Image.pdf")
        c = canvas.Canvas(receipt_path, pagesize=letter)
        img = ImageReader(temp_image_path)

        # Center image on page
        x_offset = (letter[0] - target_width) / 2  # Center horizontally
        y_offset = 0  # Start from bottom to ensure full image visibility
        c.drawImage(img, x_offset, y_offset, width=target_width, height=target_height, preserveAspectRatio=True)

        c.save()

        # Clean up temporary image
        os.remove(temp_image_path)
        return receipt_path
    except Exception as e:
        print(f"Error generating image receipt for ID {row['ID']}: {e}")
        return None

# Process each batch
for batch in batches:
    batch_data = df[df['Batch'] == batch]
    batch_output_path = os.path.join(output_base_path, batch)

    for _, row in batch_data.iterrows():
        try:
            # Generate ID card
            generate_id_card(row, template_path, batch_output_path)
            # Generate receipt
            generate_receipt(row, batch_output_path)
            # Generate image-based receipt in PDF from Image
            generate_receipt_from_image(row, receipt_template_path, batch_output_path)
        except Exception as e:
            print(f"Error processing {row['ID']}: {e}")

print("ID cards and receipts generated successfully!")