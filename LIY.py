import streamlit as st
import imaplib
import email
from datetime import datetime, timedelta
import io
from PIL import Image
import pytesseract
import fitz  # PyMuPDF

def extract_text_from_email(msg):
    text_parts = []
    for part in msg.walk():
        if part.get_content_type() == 'text/plain':
            text_parts.append(part.get_payload(decode=True).decode(part.get_content_charset(), 'ignore'))
    return '\n'.join(text_parts)

def extract_text_from_image(image_data):
    try:
        # Use Tesseract for OCR
        image = Image.open(io.BytesIO(image_data))
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        st.error(f"Error extracting text from image: {e}")
        return None

def extract_text_from_pdf(pdf_data):
    try:
        # Use PyMuPDF for PDF text extraction
        pdf_document = fitz.open(stream=io.BytesIO(pdf_data))
        text = ""
        for page_number in range(pdf_document.page_count):
            page = pdf_document[page_number]
            text += page.get_text()
        return text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
        return None

def display_images_and_text(username, password, target_email, start_date):
    image_and_text_data = []

    try:
        # ... (same as the existing code)

        # Iterate through email parts
        for part in msg.walk():
            if part.get_content_maintype() == 'image':
                # Extract image data
                image_data = part.get_payload(decode=True)

                # Perform OCR to extract text from the image
                text_from_image = extract_text_from_image(image_data)

                # Append image and text data
                image_and_text_data.append({
                    'type': 'image',
                    'content': image_data,
                    'text': text_from_image if text_from_image else text_content
                })
            elif part.get_content_type() == 'application/pdf':
                # Extract PDF data
                pdf_data = part.get_payload(decode=True)

                # Extract text from the PDF
                text_from_pdf = extract_text_from_pdf(pdf_data)

                # Append PDF and text data
                image_and_text_data.append({
                    'type': 'pdf',
                    'content': pdf_data,
                    'text': text_from_pdf if text_from_pdf else text_content
                })

    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        # ... (same as the existing code)

    return image_and_text_data

# ... (same as the existing code)

if email_address and password and target_email and start_date:
    # ... (same as the existing code)

    for idx, entry in enumerate(data, start=1):
        # Display text or PDF content
        if entry['type'] == 'image':
            st.text(f'Text {idx}: {entry["text"]}')
        elif entry['type'] == 'pdf':
            st.text(f'Text {idx} (PDF): {entry["text"]}')

        # Display image or PDF using PIL or PyMuPDF directly without io.BytesIO
        if entry['type'] == 'image':
            image = Image.open(io.BytesIO(entry["content"]))
            st.image(image, caption=f'Image {idx}', use_column_width=True)
        elif entry['type'] == 'pdf':
            st.text(f'PDF content {idx}:\n{entry["text"]}')
else:
    st.warning("Please fill in all the required fields.")
