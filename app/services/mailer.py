from __future__ import annotations
import smtplib
from email.message import EmailMessage

class Mailer:
    def __init__(self, host: str | None, port: int | None, user: str | None, password: str | None):
        self.host, self.port, self.user, self.password = host, port, user, password

    def send(self, to: str, subject: str, body: str) -> bool:
        if not self.host:
            return False
        msg = EmailMessage()
        msg["From"] = self.user or "noreply@example.com"
        msg["To"] = to
        msg["Subject"] = subject
        msg.set_content(body)
        with smtplib.SMTP(self.host, self.port or 25) as s:
            if self.user and self.password:
                s.starttls()
                s.login(self.user, self.password)
            s.send_message(msg)
        return True
