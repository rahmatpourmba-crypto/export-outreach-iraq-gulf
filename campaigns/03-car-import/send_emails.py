"""
Campaign 03 - New car import: buy new cars (2023+) from Kurdistan for Iran.
Emails via Gmail SMTP + WhatsApp via pywhatkit / Selenium (see send_whatsapp_selenium.py).
"""
import sys, io
sys.path.insert(0, r"C:\Users\Admin\Documents\Default Project\export-outreach-iraq-gulf\common")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", write_through=True)

import config as cf
import gmail_sender
import telegram as tg

cfg = cf.load_config()
gmail = cfg["gmail"]
TOKEN = cfg["telegram"]["bot_token"]
CH = cfg["telegram"]["channel_id"]
MY_NAME = cfg["candidate"]["name"]

MSG_CKB = cf.load_template("car_ckb.txt")
MSG_AR = cf.load_template("car_ar.txt")

CKB_LIST = [
    ("Al Uroush Automotive (BMW)", "info@bmw-iraq.com"),
    ("Sardar Trading Agencies", "info@sta.iq"),
    ("Bajger Co / Geely", "info@Bajger.com"),
    ("Mahroos Motors", "info@mahroosgroup.com"),
    ("Friend Car Trading (FCG)", "info@friendgroup-iq.com"),
    ("Frias Trading (Harko)", "info@friastrading.com"),
]

AR_LIST = [
    ("Al-Mansour (MAC)", "info@maciraq.com"),
]

print("=== CKB EMAILS ===")
for name, to in CKB_LIST:
    try:
        gmail_sender.send_email(gmail, to, f"کڕینی ئۆتۆمبێلی نوێ بۆ ئێران - {name}",
                                MSG_CKB.format(company=name, my=MY_NAME), "ckb")
        print("SENT OK:", name, "->", to)
        tg.send_message(TOKEN, CH, f"ئیمەیڵی کوردی نێردرا\nکۆمپانیا: {name}\nبۆ: {to}")
    except Exception as e:
        print("FAIL:", name, "->", to, "|", repr(e))

print("=== AR EMAILS ===")
for name, to in AR_LIST:
    try:
        gmail_sender.send_email(gmail, to, f"شراء سيارات جديدة إلى إيران - {name}",
                                MSG_AR.format(company=name, my=MY_NAME), "ar")
        print("SENT OK:", name, "->", to)
        tg.send_message(TOKEN, CH, f"ئیمەیڵی عەرەبی نێردرا\nکۆمپانیا: {name}\nبۆ: {to}")
    except Exception as e:
        print("FAIL:", name, "->", to, "|", repr(e))

print("DONE")