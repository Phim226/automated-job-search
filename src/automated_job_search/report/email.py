import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv


class Email:

    def __init__(self, content: str, subject: str) -> None:
        load_dotenv()
        self.content = content
        self.subject = subject


    def send_email(self) -> None:
        msg = EmailMessage()
        msg.add_alternative(self.content, subtype = "html")

        msg["Subject"] = self.subject
        msg["From"] = os.environ["SMTP_FROM"]
        msg["To"] = os.environ["SMTP_TO"]

        with smtplib.SMTP_SSL(os.environ["SMTP_SERVER"], int(os.environ["SMTP_PORT"])) as s:
            s.login(os.environ["SMTP_USERNAME"], os.environ["SMTP_PASSWORD"])
            s.send_message(msg)



