import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import uuid

# Paths
template_path = "id_card_template.jpg"
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
    # photo_pos = (200, 50)
    photo_size = (300, 300)

    # Draw text
    draw.text(name_pos, f"Name: {row['Name']}", fill="White", font=font)
    draw.text(id_pos, f"{row['ID']}", fill="green", font=font)
    draw.text(batch_pos, f"{row['Batch']}", fill="black", font=font)
    draw.text(phone_pos, f"Phone: {row['Phone']}", fill="blue", font=font)

    # Draw text - DEFAULT
    # draw.text(name_pos, f"Name: {row['Name']}", fill="White", font=font)
    # draw.text(id_pos, f"ID: {row['ID']}", fill="green", font=font)
    # draw.text(phone_pos, f"Phone: {row['Phone']}", fill="blue", font=font)

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
        except Exception as e:
            print(f"Error processing {row['ID']}: {e}")

print("ID cards and receipts generated successfully!")