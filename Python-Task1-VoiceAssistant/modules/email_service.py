import smtplib
from email.message import EmailMessage
from config import EMAIL_ADDRESS, EMAIL_PASSWORD
from modules.speech import speak, listen
from modules.logger import setup_logger

logger = setup_logger("EmailService")

CONTACTS = {
    "vishu": "vishvaraj@responseinfoway.com"
}


def send_email() -> None:
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        error_msg = "Email service is not configured. Please set EMAIL_ADDRESS and EMAIL_PASSWORD."
        logger.warning(error_msg)
        speak("Email configuration credentials are missing in the environment.")
        return

    speak("Who should I send the email to?")
    name = listen().lower().strip()

    receiver_email = CONTACTS.get(name)
    if not receiver_email:
        if "@" in name:
            receiver_email = name
        else:
            speak("I couldn't find that contact in your address book.")
            logger.info(f"Contact not found for name: {name}")
            return

    speak("What is the subject?")
    subject = listen()
    if not subject:
        speak("No subject provided. Email cancelled.")
        return

    speak("What should I write in the email?")
    body = listen()
    if not body:
        speak("No body content provided. Email cancelled.")
        return

    try:
        msg = EmailMessage()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.set_content(body)

        with smtplib.SMTP("smtp.gmail.com", 587, timeout=10) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

        logger.info(f"Email successfully sent to {receiver_email}")
        speak("Email sent successfully.")

    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        speak("Sorry, I couldn't send the email.")