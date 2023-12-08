import streamlit as st
import imaplib
import email
import base64
import os

# Function to extract PDF attachments from Gmail using IMAP
def extract_pdf_attachments(username, password):
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(username, password)
    mail.select('inbox')

    result, data = mail.search(None, 'ALL')
    mail_ids = data[0].split()

    for i in mail_ids:
        result, data = mail.fetch(i, '(RFC822)')
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            filename = part.get_filename()
            if filename and filename.endswith('.pdf'):
                file_data = part.get_payload(decode=True)
                st.write(f'Found PDF: {filename}')
                st.write(file_data)

    mail.close()
    mail.logout()

# Streamlit app
st.title('Gmail PDF Extractor')
st.write('This app extracts PDF attachments from your Gmail inbox.')

username = st.text_input('Gmail Username')
password = st.text_input('Gmail Password', type='password')

if st.button('Extract PDFs'):
    extract_pdf_attachments(username, password)
