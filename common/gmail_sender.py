import smtplib
from email.message import EmailMessage


def send_email(gmail_cfg, to, subject, body, lang, timeout=60):
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
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=timeout) as srv:
        srv.ehlo()
        srv.starttls()
        srv.ehlo()
        srv.login(gmail_cfg["user"], gmail_cfg["app_password"])
        srv.send_message(msg)