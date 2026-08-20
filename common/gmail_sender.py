import smtplib
from email.message import EmailMessage
import os


def send_email(gmail_cfg, to, subject, body, lang, timeout=60, attachment=None):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = f'<{gmail_cfg["user"]}>'
    msg["To"] = to
    msg["Reply-To"] = gmail_cfg["user"]
    msg.set_content(body)
    html = body.replace("\n", "<br>")
    msg.add_alternative(
        f'<div dir="rtl" lang="{lang}" style="font-family:Tahoma,Arial;font-size:14px;line-height:1.8">{html}</div>',
        subtype="html",
    )
    if attachment and os.path.exists(attachment):
        with open(attachment, "rb") as f:
            data = f.read()
        msg.add_attachment(
            data,
            maintype="application",
            subtype="pdf",
            filename=os.path.basename(attachment),
        )
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=timeout) as srv:
        srv.ehlo()
        srv.starttls()
        srv.ehlo()
        srv.login(gmail_cfg["user"], gmail_cfg["app_password"])
        srv.send_message(msg)