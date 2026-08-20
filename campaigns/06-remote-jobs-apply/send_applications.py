"""
Campaign 06 - Real remote job applications: email hiring teams of currently
open remote roles (Web3 smart-contract auditing + HSE), attaching the matching resume.
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

LOG = os.path.join(os.path.dirname(__file__), "..", "..", "logs", "Remote_Jobs_Log.txt")
LOG = os.path.abspath(LOG)

CV_WEB3 = r"C:\Users\Admin\Documents\Default Project\arbitrage-bot\Abdolbaset_Rahmatpour_Web3_Developer.pdf"
CV_HSE = r"C:\Users\Admin\Documents\Default Project\arbitrage-bot\Abdolbaset_Rahmatpour_HSE_Engineer.pdf"

# (company, email, role title, cv path, body template key)
JOBS = [
    ("Poly Syncer", "careers@polysyncer.com",
     "Smart Contract Auditor (fixed-scope engagement, fully remote)",
     CV_WEB3, "web3"),
    ("Oshield", "audit@oshield.io",
     "Smart Contract Security Auditor (100% remote)",
     CV_WEB3, "web3"),
    ("SigIntZero", "contact@sigintzero.com",
     "Senior Smart Contract Auditor (remote) / Security Researcher",
     CV_WEB3, "web3"),
    ("Quantstamp", "info@quantstamp.com",
     "Auditing Engineer II (fully remote)",
     CV_WEB3, "web3"),
    ("Nethermind", "hello@nethermind.io",
     "Smart Contract Auditor - Remote, Worldwide",
     CV_WEB3, "web3"),
    ("Cyberscope", "contact@cyberscope.io",
     "Smart Contract Auditor / Blockchain Developer (Remote)",
     CV_WEB3, "web3"),
    ("Solenis", "talentacquisition@solenis.com",
     "Process Safety Engineer (Remote)",
     CV_HSE, "hse"),
]

BODY_WEB3 = """Dear {company} Hiring Team,

I am applying for the {role} position advertised on your careers page.

I am a Web3 developer and smart contract security specialist with a unique profile: 16+ years of professional risk assessment, compliance and audit management experience (ISO 45001, incident investigation, hazard analysis), now fully applied to blockchain security. I work with Solidity, Hardhat, Truffle, Web3.js and DeFi protocol analysis, and I approach smart contract auditing with the same rigorous, methodology-driven mindset that made me successful in industrial safety.

Multilingual (English B2/C1, Persian, Kurdish Sorani), fully remote-ready in any time zone, and available to start immediately.

Please find my CV attached. I would welcome the chance to discuss how I can contribute to your team.

Best regards,
Abdolbaset Rahmatpour
Web3 Developer | Smart Contract Security Auditor
Email: rahmatpour63@gmail.com | WhatsApp: +989141688217"""

BODY_HSE = """Dear {company} Hiring Team,

I am applying for the {role} position advertised by your organization.

I am a Senior HSE Engineer with 16+ years of experience in occupational health and safety, risk assessment, hazard analysis, ISO 45001 compliance, safety auditing and workforce training (500+ workers trained, 35% incident-rate reduction, 98% regulatory compliance). I hold an MBA and a B.Sc. in Occupational Health Engineering, and I am a multilingual professional (English B2/C1, Persian, Kurdish Sorani).

Fully remote-ready, flexible on time zones, and available to start immediately. My CV is attached for your review.

I would welcome the opportunity to discuss how my experience can support your team.

Best regards,
Abdolbaset Rahmatpour
Senior HSE Engineer | Occupational Health & Safety Specialist
Email: rahmatpour63@gmail.com | WhatsApp: +989141688217"""

def logline(s):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(s + "\n")
    print(s, flush=True)

if not os.path.exists(LOG):
    with open(LOG, "w", encoding="utf-8") as f:
        f.write(f"شغل‌های دورکاری - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write("=" * 60 + "\n")

total = 0
for company, to, role, cv, kind in JOBS:
    body = (BODY_WEB3 if kind == "web3" else BODY_HSE).format(company=company, role=role)
    subject = f"Application - {role}"
    try:
        gmail_sender.send_email(gmail, to, subject, body, "en", timeout=60, attachment=cv)
        total += 1
        logline(f"SENT    {company}  -> {to}  ({role[:45]})")
        tg.send_message(TOKEN, CH, f"ئیمەیڵی داوای کار نێردرا\nکۆمپانیا: {company}\nبۆ: {to}")
    except Exception as e:
        logline(f"FAIL    {company}  -> {to}  | {repr(e)[:100]}")
    time.sleep(10)

logline(f"TOTAL SENT: {total}")