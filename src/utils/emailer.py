from email.message import EmailMessage

e_message = EmailMessage()
e_message["From"] = "From"
e_message["To"] = "To"
e_message["Subject"] = "Subject"
e_message.set_content("Test message")
