"""
Campaign 02 - Food & energy drinks export: Persian round + localized (CKB/AR) round.
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

MSG_FA = cf.load_template("food_fa.txt")
MSG_CKB = cf.load_template("food_ckb.txt")
MSG_AR = cf.load_template("food_ar.txt")

SUBJ_FA = "پیشنهاد همکاری صادراتی - تولید محصولات غذایی از ایران"
SUBJ_CKB = "پێشنیاری هاوکاری هەناردەکردن - بەرهەمهێنانی خۆراکی لە ئێران"
SUBJ_AR = "عرض تعاون تصديري - إنتاج منتجات غذائية من إيران"

EMAILS = [
    ("Mega Power", "info@megapoweriraq.com"),
    ("Ahram General Trading", "info@ahramcompany.com"),
    ("BGT", "info@bgt-company.com"),
    ("Larsa Group", "info@larsagroup.net"),
    ("T. Road Trading", "info@tradingroad.com"),
    ("SweetSnack", "info@sweetsnack.co"),
    ("Al Shorooq Oasis", "alshorooqoasis@gmail.com"),
    ("Treasure Islands F&B", "info@treasureislands.ae"),
    ("RVT Royal Ventures", "Info@rvtbeverages.com"),
    ("ANF Multinational", "info@anf.ae"),
    ("Vivandi Distribution", "info@vivandidistribution.com"),
    ("Qimia Nutrition", "info@qimiamiddleeast.com"),
    ("Unique Light Company", "unique.light.fd@gmail.com"),
    ("Al-Madhaq Al-Alami", "Badr@tastyfoodcorp.com"),
    ("Quality Trading Co", "customercare@qtcarabia.com"),
    ("Mahmood Saeed", "info@mscc.com.sa"),
    ("Qasyon International", "info@qasyonint.com"),
    ("Muscat Chemical", "muscatchemical.com@gmail.com"),
    ("AW Pharma", "info@awpharma.net"),
    ("Zululan Health Care", "info@zululanpharma.com"),
]

CKB_EMAILS = EMAILS[:6]
AR_EMAILS = EMAILS[6:]

CKB_WA = [
    ("Mega Power", "9647733069933"),
    ("Ahram General Trading", "9647504505019"),
    ("BGT", "9647507005070"),
    ("Larsa Group", "9647501329601"),
    ("T. Road Trading", "9647504445559"),
    ("SweetSnack", "9647729772601"),
]

AR_WA = [
    ("Treasure Islands F&B", "971506319525"),
    ("RVT Royal Ventures", "971502694513"),
    ("Qimia Nutrition", "971528028591"),
    ("Unique Light Company", "966579397854"),
    ("Al-Madhaq Al-Alami", "966505619079"),
    ("Qasyon International", "96891992727"),
    ("Muscat Chemical", "96893960629"),
    ("Aljameel International", "96566848065"),
]

print("=== PERSIAN EMAILS ===")
for name, to in EMAILS:
    try:
        gmail_sender.send_email(gmail, to, SUBJ_FA, MSG_FA, "fa")
        print("SENT OK:", name, "->", to)
        tg.send_message(TOKEN, CH, f"ئیمەیڵ نێردرا\nکۆمپانیا: {name}\nبۆ: {to}")
    except Exception as e:
        print("FAIL:", name, "->", to, "|", repr(e))

print("=== CKB EMAILS ===")
for name, to in CKB_EMAILS:
    try:
        gmail_sender.send_email(gmail, to, SUBJ_CKB, MSG_CKB, "ckb")
        print("SENT OK:", name, "->", to)
        tg.send_message(TOKEN, CH, f"ئیمەیڵی کوردی نێردرا\nکۆمپانیا: {name}\nبۆ: {to}")
    except Exception as e:
        print("FAIL:", name, "->", to, "|", repr(e))

print("=== AR EMAILS ===")
for name, to in AR_EMAILS:
    try:
        gmail_sender.send_email(gmail, to, SUBJ_AR, MSG_AR, "ar")
        print("SENT OK:", name, "->", to)
        tg.send_message(TOKEN, CH, f"ئیمەیڵی عەرەبی نێردرا\nکۆمپانیا: {name}\nبۆ: {to}")
    except Exception as e:
        print("FAIL:", name, "->", to, "|", repr(e))

print("=== CKB WHATSAPP ===")
for name, num in CKB_WA:
    try:
        ok, info = wa.send_whatsapp(num, MSG_CKB, wait_seconds=18, close_tab=True)
        print(("SENT OK" if ok else "FAIL"), name, "->", info)
        if ok:
            tg.send_message(TOKEN, CH, f"واتساپی کوردی نێردرا\nکۆمپانیا: {name}\nبۆ: +{info}")
    except Exception as e:
        print("FAIL:", name, "|", repr(e))

print("=== AR WHATSAPP ===")
for name, num in AR_WA:
    try:
        ok, info = wa.send_whatsapp(num, MSG_AR, wait_seconds=18, close_tab=True)
        print(("SENT OK" if ok else "FAIL"), name, "->", info)
        if ok:
            tg.send_message(TOKEN, CH, f"واتساپی عەرەبی نێردرا\nکۆمپانیا: {name}\nبۆ: +{info}")
    except Exception as e:
        print("FAIL:", name, "|", repr(e))

print("DONE")