"""
Campaign 04 - Steel & iron supply: sell steel/rebar from Iran to Iraq & Syria.
Emails via Gmail SMTP. Resume mode skips entries already present in the log.
"""
import sys, io, os, datetime
sys.path.insert(0, r"C:\Users\Admin\Documents\Default Project\export-outreach-iraq-gulf\common")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", write_through=True)
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", write_through=True)

import config as cf
import gmail_sender
import telegram as tg

cfg = cf.load_config()
gmail = cfg["gmail"]
TOKEN = cfg["telegram"]["bot_token"]
CH = cfg["telegram"]["channel_id"]
MY_NAME = cfg["candidate"]["name"]

LOG = os.path.join(os.path.dirname(__file__), "..", "..", "logs", "Steel_Email_Log.txt")
LOG = os.path.abspath(LOG)

MSG_CKB = cf.load_template("steel_ckb.txt")
MSG_AR = cf.load_template("steel_ar.txt")
SUBJ_CKB = "دابینکردنی پۆڵا و ئاسن لە ئێران - {company}"
SUBJ_AR = "توريد الحديد والصلب من إيران - {company}"

EMAILS = [
    ("Meskent Group", ["info@meskent-group.com"], "ckb"),
    ("Darin Steel", ["info@darinsteel.com"], "ckb"),
    ("Halkawt Steel", ["info@halkawtsteel.com"], "ckb"),
    ("Hritan Iron & Steel", ["info@hritansteel.com.iq", "manager@hritansteel.com.iq", "sales@hritansteel.com.iq"], "ckb"),
    ("Al Sultan Group", ["info@alsultan-group.net"], "ar"),
    ("Iraqi Hadeed", ["info@iraqishaded.com"], "ar"),
    ("Al-Rasheed International Trading", ["pr@rasheedtrading.com", "rasheed@rasheedtrading.com"], "ar"),
    ("AL-Fairoz Al-Thahabi", ["info@fairozthahabi.com"], "ar"),
    ("Khan Alhadeed", ["info@khanalhadeed.com.iq"], "ar"),
    ("Maalim Al-Asima", ["husseinsalm30@gmail.com"], "ar"),
    ("Bilad Alwafaa", ["biladalwafaaco@gmail.com"], "ar"),
    ("Alam Al-Hadid", ["info@alamalhadid.com"], "ar"),
    ("Basra Steel Galvanizing", ["info@basra-galvanizing.com", "omar.jamal@basra-galvanizing.com"], "ar"),
    ("Steel Syria", ["info@steel-syria.com", "sales@steel-syria.com"], "ar"),
    ("Isnad", ["sales@isnad-sy.com"], "ar"),
    ("Mediterranean Steel", ["info@med-steel.com"], "ar"),
]

def logline(s):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(s + "\n")
    print(s, flush=True)

def already_sent(company, to):
    if not os.path.exists(LOG):
        return False
    with open(LOG, encoding="utf-8") as f:
        return any(f"{company}  -> {to}" in line for line in f)

if not os.path.exists(LOG):
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    with open(LOG, "w", encoding="utf-8") as f:
        f.write(f"ایمیل فولاد - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write("=" * 60 + "\n")

total = 0
for company, emails, lang in EMAILS:
    body = (MSG_CKB if lang == "ckb" else MSG_AR).format(company=company, my=MY_NAME)
    subj = (SUBJ_CKB if lang == "ckb" else SUBJ_AR).format(company=company)
    for em in emails:
        if already_sent(company, em):
            print(f"SKIP    {lang:3s} {company}  -> {em}  (already)")
            continue
        try:
            gmail_sender.send_email(gmail, em, subj, body, lang)
            total += 1
            logline(f"SENT    {lang:3s} {company}  -> {em}")
            tg.send_message(TOKEN, CH, f"ئیمەیڵی فۆڵاد نێردرا\nکۆمپانیا: {company}\nبۆ: {em}")
        except Exception as e:
            logline(f"FAIL    {lang:3s} {company}  -> {em}  | {repr(e)[:80]}")

logline(f"TOTAL NEW SENT: {total}")