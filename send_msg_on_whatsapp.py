from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import urllib.parse

# Set up Chrome options
options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

# Open WhatsApp Web
driver.get("https://web.whatsapp.com")
print("Please scan the QR code...")
time.sleep(30)  # Allow time to scan

# Load contacts from CSV
df = pd.read_csv("contacts.csv", encoding='utf-8-sig')
df = df.drop_duplicates(subset=['Number'])

# Message you want to send
message = """✨ *Garba Workshop Reminder!* 💃🕺

Hello! 👋 This is a reminder for our *Sunday Garba Workshop*. 
Please don't forget to join us and enjoy the rhythm and energy! 💃🔥

📍 *Location*: 16, Pritam Nagar Rd, Ellisbridge, Ahmedabad
🕒 *Time*: 7:30 PM to 10:00 PM

Bring your friends and let's celebrate together! 🎉"""

# URL encode message
message2 = """
Hello_from_Python_script
using whatsapp_web
"""
encoded_message = urllib.parse.quote(message2)

# Iterate and send messages
for i, row in df.iterrows():
    raw_number = str(row["Number"]).strip().replace(" ", "").replace("+91", "")
    if not raw_number.isdigit() or len(raw_number) < 10:
        print(f"⚠️ Skipping invalid number: {raw_number}")
        continue

    number = raw_number[-10:]
    url = f"https://web.whatsapp.com/send?phone=91{number}&text={encoded_message}"
    driver.get(url)
    print(f"➡️ Opening chat with {number}...")
    time.sleep(12)

    try:
        input_box = driver.find_element(By.XPATH, '//div[@aria-label="Type a message"]')
        input_box.send_keys(Keys.ENTER)
        print(f"✅ Message sent to {number}")
        time.sleep(3)
    except Exception as e:
        print(f"❌ Could not send to {number}: {e}")

driver.quit()
