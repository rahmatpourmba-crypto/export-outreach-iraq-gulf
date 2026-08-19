# Export Outreach – Iraq & Gulf

B2B outreach campaigns by **Abdolbaset Rahmatpour** (عەبدولباسیت ڕەحمەتپوور) to companies in
Iraq (Kurdistan + Arabs), Syria and the GCC: dental supplies purchasing, food & energy-drink
export, new-car import from Kurdistan, and steel/iron supply from Iran.

Each campaign sends **localized emails** (Kurdish Sorani for Kurdistan, Arabic for Arab
companies, Persian for the first food round) plus **WhatsApp** messages, with progress logged
and mirrored to a Telegram channel.

## Campaigns

| # | Folder | Goal | Markets | Language | Emails sent | WhatsApp |
|---|--------|------|---------|----------|-------------|----------|
| 01 | `campaigns/01-dental-supplies` | Buy dental equipment & supplies | Kurdistan-Iraq | ckb | 6 | 5 (unreliable, see below) |
| 02 | `campaigns/02-energy-drinks-food` | Export energy drinks & vitamin C supplements | Iraq, UAE, KSA, Oman, Kuwait | fa, ckb, ar | 20 + 20 localized | 14 (unreliable) |
| 03 | `campaigns/03-car-import` | Buy new cars (2023+) in Kurdistan, import to Iran | Kurdistan-Iraq | ckb, ar | 7 | 23 (unreliable) |
| 04 | `campaigns/04-steel-iron` | Supply steel, iron & rebar from Iran | Iraq, Syria | ckb, ar | 9 of 16 companies (in progress) | Meskent only (Selenium) |

## Structure

```
├── campaigns/            # one folder per campaign (scripts + notes)
├── common/               # shared modules (config loader, Gmail SMTP sender, telegram, whatsapp)
├── templates/            # localized message templates (ckb / ar / fa)
├── leads/                # source contact lists (PDF scans, CSV, TXT)
└── logs/                 # send logs used for resume/skip logic
```

## Setup

1. Install Python 3.10+.
2. `pip install requests pywhatkit selenium`
3. `cp config.example.json config.json` and fill in:
   - `gmail.user` / `gmail.app_password` – your Gmail address and a
     [Gmail App Password](https://support.google.com/accounts/answer/185833) (16 chars, no spaces).
   - `telegram.bot_token` / `telegram.channel_id` – optional Telegram notifications.
4. Run a campaign script, e.g. `python campaigns/04-steel-iron/send_emails.py`.

> `config.json` is git-ignored. Never commit real credentials.

## Important lessons learned (hard-won)

### Email (reliable)
- Gmail SMTP (`smtp.gmail.com:587`, STARTTLS) works fine. Use an **app password**, not the
  account password.
- Bulk-sending to many new addresses quickly triggers a **temporary SMTP block**
  (`TimeoutError 10060` while IMAP port 993 still works). The block usually lifts within ~24h.
  Use the resume scripts (they skip already-logged entries) once it lifts.
- Set a per-connection timeout (`timeout=60`) so one dead address can't stall the whole run.
- Persian/Kurdish/Arabic bodies are sent as UTF-8 plain text + an RTL HTML alternative with
  `dir="rtl"` and the right `lang` attribute – renders correctly in all clients.

### WhatsApp via pywhatkit (DO NOT USE – reports success without sending)
- `pywhatkit` opens `web.whatsapp.com` with `webbrowser.open()` in the **default browser**.
  If that browser is not logged into WhatsApp Web, `sendwhatmsg_instantly` still returns
  "success" but **nothing is sent**. All pywhatkit-based sends in campaigns 01–03 are
  unverified and were later confirmed **not delivered** (the default browser was Firefox,
  logged out).

### WhatsApp via Selenium (reliable – used in campaign 04)
- Install: `pip install --index-url https://pypi.org/simple selenium` (plain `pip install`
  failed with "No matching distribution found" on this machine).
- Use a **Chrome user-data-dir** copy of your profile that is already logged into WhatsApp
  Web / WhatsApp Business. Scan the QR code once beforehand.
- Navigate with `driver.execute_script("window.location.href=...")`, **not** `driver.get()`
  (which reloads and breaks the session).
- Verify the right chat opened via `div[contenteditable="true"][data-tab="10"]` whose
  `aria-label` contains the target digits, then type and click `button[data-testid="send"]`
  (or press Enter).
- Do **not** reload between sends; keep one session and wait ~14s per chat.
- Rapid consecutive sends can get the session invalidated (chat-list disappears) – slow down
  and re-scan the QR code if that happens.

## Bounced addresses (learned from Gmail inbox)
- `info@dentalin.net`, `info@ahramcompany.com`, `info@bgt-company.com`, `info@anf.ae`
- Older job-related: `Iraq-recruiting@slb.com`, `recruitment.ksa@tractebel.engie.com`,
  `bill.mooney@politickernj.com`, `recruitment@halliburton.com`

## Contact
- WhatsApp: +989141688217
- Email: rahmatpour63@gmail.com