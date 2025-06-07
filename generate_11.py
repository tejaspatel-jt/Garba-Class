import os
import sys
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from datetime import datetime
import uuid
import logging

# Setup logging to capture errors
logging.basicConfig(filename='errors.log', level=logging.ERROR, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Paths
# Set base path to the .exe or script's folder
base_path = os.path.dirname(sys.argv[0])

# Paths (relative to .exe/script folder)
template_path = os.path.join(base_path, "input_data", "templates", "idcard_template.jpg")
receipt_template_path = os.path.join(base_path, "input_data", "templates", "receipt_template.png")
photos_path = os.path.join(base_path, "input_data", "photos")
output_base_path = os.path.join(base_path, "ID_Receipts")
excel_path = os.path.join(base_path, "input_data", "students.xlsx")
font_path = os.path.join(base_path, "arial.ttf")

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
try:
    df = pd.read_excel(excel_path)
except Exception as e:
    logging.error(f"Error reading Excel file: {e}")
    print(f"Error reading Excel file: {e}. Check errors.log.")
    sys.exit(1)

# Font settings for ID card (adjust path to a TrueType font on your system)
# Font settings
font_size = 44
try:
    font = ImageFont.truetype(font_path, font_size)
except Exception as e:
    logging.error(f"Error loading font: {e}")
    print(f"Error loading font: {e}. Ensure 'arial.ttf' is in the folder. Check errors.log.")
    sys.exit(1)

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
    c.drawString(100, 630, f"Payment Amount: ${row['Payment Amount']}")
    c.drawString(100, 610, "Thank you for your payment!")

    c.save()
    return receipt_path

# New function to generate image-based payment receipt PDF
# ✅ TEXT IS VISIBLE now in BBF - Big Black Font 😜
# ✅ Photo also added at perfect position
# ✅ Receipt PDF is now created Perfectly from image - but lot to be worked on size and position of text
def generate_receipt_from_image(row, template_path, output_path):
    try:
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template not found: {template_path}")
        template = Image.open(template_path)

        # Resize template to fit letter-sized page (8.5x11 inches at 300 DPI)
        # target_height = 3300  # 11 inches at 300 DPI
        # target_width = int(target_height * (6480 / 11520))  # Maintain 9:16 aspect ratio

        target_height = 11520  # static height from the template
        target_width = 6480  # static width from the template

        resized_template = template.resize((target_width, target_height), Image.LANCZOS)

        # Draw text on resized template
        draw = ImageDraw.Draw(resized_template)

        # Coordinates for text (scaled for resized template: 1860x3300 pixels)
        # scale_factor = target_width / 6480  # ~0.287
        # date_pos = (int(200 * scale_factor), int(200 * scale_factor))
        # name_pos = (int(200 * scale_factor), int(400 * scale_factor))
        # id_pos = (int(200 * scale_factor), int(600 * scale_factor))
        # phone_pos = (int(200 * scale_factor), int(800 * scale_factor))
        # batch_pos = (int(200 * scale_factor), int(1000 * scale_factor))
        # amount_pos = (int(200 * scale_factor), int(1200 * scale_factor))

        date_pos = (50, 30)
        name_pos = (50, 70)
        id_pos = (50, 110)
        phone_pos = (50, 150)
        batch_pos = (50, 190)
        amount_pos = (50, 230)
        photo_size = (1200, 1400)
        photo_pos = (4450, 1650)
        

        # Use larger font for visibility
        receipt_font_size = 60
        receipt_font = ImageFont.truetype(font_path, receipt_font_size)

        # Draw text
        draw.text(date_pos, f"Date: {datetime.now().strftime('%Y-%m-%d')}", fill="black", font=receipt_font)
        draw.text(name_pos, f"Name: {row['Name']}", fill="black", font=receipt_font)
        draw.text(id_pos, f"ID: {row['ID']}", fill="black", font=receipt_font)
        draw.text(phone_pos, f"Phone: {row['Phone']}", fill="black", font=receipt_font)
        draw.text(batch_pos, f"Batch: {row['Batch']}", fill="black", font=receipt_font)
        draw.text(amount_pos, f"Payment Amount: ${row['Payment Amount']}", fill="black", font=receipt_font)

        # Add photo
        photo_path = os.path.join(photos_path, row['PhotoFilename'])
        if os.path.exists(photo_path):
            photo = Image.open(photo_path)
            photo = photo.resize(photo_size, Image.LANCZOS)
            # template.paste(photo, photo_pos)
            resized_template.paste(photo, photo_pos)
        else:
            logging.warning(f"Photo not found: {photo_path}")

        # Save temporary image as PNG
        temp_image_path = os.path.join(output_path, f"{row['ID']}_temp_receipt.png")
        resized_template.save(temp_image_path, format="PNG")

        # Convert ID card image to PDF
        pdf_path = os.path.join(output_path, f"{row['ID']}_ReceiptFromTemp.pdf")
        resized_template.save(pdf_path, "PDF", resolution=100.0)

        # Create PDF
        receipt_path = os.path.join(output_path, f"{row['ID']}_Receipt_Image.pdf")
        # c = canvas.Canvas(receipt_path, pagesize=letter)
        c = canvas.Canvas(receipt_path, pagesize=None)
        img = ImageReader(temp_image_path)

        # Center image on page
        # x_offset = (letter[0] - target_width) / 2  # Center horizontally
        # y_offset = 0  # Start from bottom to ensure full image visibility
        # c.drawImage(img, x_offset, y_offset, width=target_width, height=target_height, preserveAspectRatio=True)

        img_width, img_height = resized_template.size
        c.drawImage(img, 0, letter[1] - img_height, width=img_width, height=img_height)
        # c.drawImage(img, 0, 0, width=img_width, height=img_height)

        c.save()

        # Clean up temporary image
        # os.remove(temp_image_path)

        return receipt_path
    except Exception as e:
        logging.error(f"Error generating image receipt for ID {row['ID']}: {e}")
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

            print(f"processing row {row['ID']}: {row['Name']}")
        except Exception as e:
            print(f"Error processing {row['ID']}: {e}")

print("ID cards and receipts generated successfully!")