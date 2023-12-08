import streamlit as st
import imaplib
import email
from datetime import datetime, timedelta
import io
from PIL import Image
import pytesseract

def extract_text_from_email(msg):
    text_parts = []
    for part in msg.walk():
        if part.get_content_type() == 'text/plain':
            text_parts.append(part.get_payload(decode=True).decode(part.get_content_charset(), 'ignore'))
    return '\n'.join(text_parts)

def extract_text_from_image(image_data):
    try:
        # Use pytesseract for OCR (no need to download Tesseract separately)
        text = pytesseract.image_to_string(Image.open(io.BytesIO(image_data)))
        return text
    except Exception as e:
        st.error(f"Error extracting text from image: {e}")
        return None

def display_images_with_text(imap_server, username, password, target_email, start_date):
    image_and_text_data = []

    try:
        # Convert start_date to datetime object
        start_date = datetime.strptime(start_date, '%Y-%m-%d')

        # Connect to the IMAP server
        mail = imaplib.IMAP4_SSL(imap_server)

        # Login to the email account
        mail.login(username, password)

        # Select the mailbox (e.g., 'inbox')
        mail.select("inbox")

        # Construct the search criterion using the date range and target email address
        search_criterion = f'(FROM "{target_email}" SINCE "{start_date.strftime("%d-%b-%Y")}" BEFORE "{(start_date + timedelta(days=1)).strftime("%d-%b-%Y")}")'

        # Search for emails matching the criteria
        result, data = mail.uid('search', None, search_criterion)
        email_ids = data[0].split()

        # Iterate through the email IDs
        for email_id in email_ids:
            result, msg_data = mail.uid('fetch', email_id, "(RFC822)")
            raw_email = msg_data[0][1]

            # Parse the raw email content
            msg = email.message_from_bytes(raw_email)

            # Extract text from the email
            text_content = extract_text_from_email(msg)

            # Iterate through email parts
            for part in msg.walk():
                if part.get_content_maintype() == 'image':
                    # Extract image data
                    image_data = part.get_payload(decode=True)

                    # Perform OCR to extract text from the image
                    text_from_image = extract_text_from_image(image_data)

                    # Append image and text data
                    image_and_text_data.append({
                        'image': image_data,
                        'text': text_from_image if text_from_image else text_content
                    })

    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        # Logout from the IMAP server (even if an error occurs)
        mail.logout()

    return image_and_text_data

# Streamlit app
st.title("Image and Text Viewer")

# Get user input through Streamlit
imap_server = st.text_input("Enter your IMAP server (e.g., imap.gmail.com):")
email_addre
