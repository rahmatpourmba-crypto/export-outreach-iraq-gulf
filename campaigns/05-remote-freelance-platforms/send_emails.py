"""
Campaign 05 - Remote & freelance platforms: introduce multi-disciplinary profile
(HSE Engineer + Web3 Developer + Graphic Designer) to global remote job boards.
"""
import sys, io, os, time, datetime
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

LOG = os.path.join(os.path.dirname(__file__), "..", "..", "logs", "Remote_Platforms_Log.txt")
LOG = os.path.abspath(LOG)

SUBJECT = "Remote Professional: HSE Engineer | Web3 Developer | Graphic Designer"

BODY = """Hello {platform} Team,

My name is Abdolbaset Rahmatpour, a multilingual professional (Persian, Kurdish Sorani, English) based in Iran, looking for remote opportunities. I bring a rare combination of skills across three domains:

1) HSE ENGINEERING (16+ years): Senior HSE Engineer with extensive experience in occupational health & safety, risk assessment, hazard analysis, ISO 45001 compliance, safety auditing and workforce training (500+ workers trained). MBA + B.Sc. in Occupational Health Engineering.

2) WEB3 DEVELOPMENT: Smart contract developer & security auditor with a strong foundation in Solidity, Ethereum, Polygon, DeFi protocols, Web3.js, Hardhat and smart contract auditing. Hands-on with JavaScript, Python, React, Node.js.

3) GRAPHIC DESIGN: Logo design, branding and visual identity design services for startups and businesses.

I am available for full-time remote roles and freelance projects worldwide. Resume and portfolio are available on request.

Contact: rahmatpour63@gmail.com | WhatsApp: +989141688217

I would appreciate the opportunity to register my profile with your platform and be considered for relevant remote openings.

Best regards,
Abdolbaset Rahmatpour"""

PLATFORMS = [
    ("FlexJobs", "support@flexjobs.com"),
    ("We Work Remotely", "support@weworkremotely.com"),
    ("Remote.co", "info@remote.co"),
    ("DailyRemote", "contact@dailyremote.com"),
    ("Himalayas", "hi@himalayas.app"),
    ("Wellfound", "team@wellfound.com"),
    ("RemoteOK", "hello@remoteok.com"),
    ("Remotive", "hello@remotive.com"),
    ("Toptal", "support@toptal.com"),
    ("Freelancer.com", "support@freelancer.com"),
    ("Fiverr", "support@fiverr.com"),
    ("99designs", "support@99designs.com"),
    ("Designhill", "support@designhill.com"),
    ("Dribbble", "contact@dribbble.com"),
    ("Working Not Working", "hello@workingnotworking.com"),
    ("Guru.com", "contactus@guru.com"),
    ("PeoplePerHour", "support@peopleperhour.com"),
    ("ProZ.com", "support@proz.com"),
]

def logline(s):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(s + "\n")
    print(s, flush=True)

if not os.path.exists(LOG):
    with open(LOG, "w", encoding="utf-8") as f:
        f.write(f"پلتفرم‌های دورکاری - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write("=" * 60 + "\n")

total = 0
for platform, to in PLATFORMS:
    body = BODY.format(platform=platform)
    try:
        gmail_sender.send_email(gmail, to, SUBJECT, body, "en", timeout=60)
        total += 1
        logline(f"SENT    {platform}  -> {to}")
        tg.send_message(TOKEN, CH, f"ئیمەیڵ بۆ پلاتفۆرمی دورکاری نێردرا\nپلاتفۆرم: {platform}\nبۆ: {to}")
    except Exception as e:
        logline(f"FAIL    {platform}  -> {to}  | {repr(e)[:100]}")
    time.sleep(8)

logline(f"TOTAL SENT: {total}")