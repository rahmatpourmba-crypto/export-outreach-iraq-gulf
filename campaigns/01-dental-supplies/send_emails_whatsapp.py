"""
Campaign 01 - Dental supplies: buy dental equipment/clinics from Kurdistan.
Emails via Gmail SMTP + WhatsApp via pywhatkit (UNRELIABLE - see README).
"""
import sys, io
sys.path.insert(0, r"C:\Users\Admin\Documents\Default Project\export-outreach-iraq-gulf\common")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", write_through=True)

import config as cf
import gmail_sender
import telegram as tg
import whatsapp as wa

cfg = cf.load_config()
gmail = cfg["gmail"]
TOKEN = cfg["telegram"]["bot_token"]
CH = cfg["telegram"]["channel_id"]
MY_NAME = cfg["candidate"]["name"]
BODY = cf.load_template("dental_ckb.txt")

EMAILS = [
    ("Snow Medical", "info@snowiraq.com"),
    ("TMC", "info@tmc-iraq.com"),
    ("LOK Medical", "info@lokcompany.com"),
    ("Dar Al-Meshkat", "info@dar-almeshkat.com.iq"),
    ("CosmoLight Group", "info@cosmolight-group.com"),
    ("Dentalin", "info@dentalin.net"),
]

PHONES = [
    ("Yohan Company", "07504698854"),
    ("Crown Dent (Erbil)", "9647504857538"),
    ("Crown Dent (Sulaymaniyah)", "9647517236090"),
    ("Yanal Company", "9647504940333"),
    ("Snow Medical", "07709955551"),
]

print("=== EMAILS ===")
for company, to in EMAILS:
    try:
        gmail_sender.send_email(gmail, to, f"کڕینی کەلوپەلی ددانپزیشکی - {company}",
                                BODY.format(company=company, my=MY_NAME), "ckb")
        print("SENT OK:", company, "->", to)
        tg.send_message(TOKEN, CH, f"ئیمەیڵ نێردرا\nکۆمپانیا: {company}\nبۆ: {to}")
    except Exception as e:
        print("FAIL:", company, "->", to, "|", repr(e))

print("=== WHATSAPP ===")
for company, num in PHONES:
    try:
        ok, info = wa.send_whatsapp(num, BODY.format(company=company, my=MY_NAME), wait_seconds=18, close_tab=True)
        print(("SENT OK" if ok else "FAIL"), company, "->", info)
        if ok:
            tg.send_message(TOKEN, CH, f"واتساپ نێردرا\nکۆمپانیا: {company}\nبۆ: +{info}")
    except Exception as e:
        print("FAIL:", company, "|", repr(e))

print("DONE")