import streamlit as st
import imaplib
import email
from datetime import datetime, timedelta
import io
from PIL import Image
import pytesseract
from pytesseract import Output

# Set the path to the Tesseract executable (change this to your Tesseract installation path)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image_bytes):
    try:
        # Open the image using PIL
        image = Image.open(io.BytesIO(image_bytes))

        # Use pytesseract to perform OCR on the image
        extracted_text = pytesseract.image_to_string(image, output_type=Output.STRING)

        return extracted_text
    except Exception as e:
        return f"Text extraction error: {e}"

def display_images(username, password, target_email, start_date):
    # ... (your existing code)

    # Iterate through the email IDs
    for email_id in email_ids:
        result, msg_data = mail.uid('fetch', email_id, "(RFC822)")
        raw_email = msg_data[0][1]

        # Parse the raw email content
        msg = email.message_from_bytes(raw_email)

        # Iterate through email parts
        for part in msg.walk():
            if part.get_content_maintype() == 'image':
                # Extract image data
                image_bytes = part.get_payload(decode=True)

                # Display image using PIL
                image = Image.open(io.BytesIO(image_bytes))
                st.image(image, caption=f'Image {idx}', use_column_width=True)

                # Extract text from the image
                extracted_text = extract_text_from_image(image_bytes)
                st.text(f'Text from Image {idx}: {extracted_text}')

# ... (your existing Streamlit code)
