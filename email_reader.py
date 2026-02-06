import imaplib
import email
from email.header import decode_header
import Config  # Make sure your config file is named Config.py

def read_latest_email():
    # Connect to the server
    mail = imaplib.IMAP4_SSL(Config.IMAP_SERVER)
    
    # Login to your account
    mail.login(Config.mygmail, Config.password)
    
    # Select the inbox folder
    mail.select("inbox", readonly=True)
    
    # Search for all emails
    status, messages = mail.search(None, "ALL")
    
    # Convert messages to list of email IDs
    email_ids = messages[0].split()
    
    # Get the latest email ID
    latest_email_id = email_ids[-1]
    
    # Fetch the latest email
    status, msg_data = mail.fetch(latest_email_id, "(RFC822)")
    
    # Convert raw bytes to message object
    msg = email.message_from_bytes(msg_data[0][1])
    
    # Decode the subject
    subject_data = decode_header(msg['Subject'])[0]
    subject = subject_data[0]
    if isinstance(subject, bytes):
        subject = subject.decode(subject_data[1] if subject_data[1] else "utf-8")
    
    # Extract the body
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain" and "attachment" not in part.get("Content-Disposition", ""):
                body = part.get_payload(decode=True).decode()
                break
    else:
        body = msg.get_payload(decode=True).decode()
    
    # Logout and close connection
    mail.logout()
    
    # Return subject and body
    return subject, body

subject, body = read_latest_email()
print("Subject:", subject)
print("Body:", body)

