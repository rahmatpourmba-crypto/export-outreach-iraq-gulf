# Campaign 04 – Steel & Iron Supply from Iran

**Goal:** Supply steel, iron, rebar (rebari) and steel products from Iran to steel companies
in Iraq (Kurdistan + Arab regions) and Syria at competitive prices.

**Contacts source:** `leads/steel_companies_iraq_syria.csv` (27 companies from official
websites).

**Language split:** Kurdish Sorani for Kurdistan companies (Meskent, Darin, Van Steel,
Halkawt, Yaaqub, Erbil Steel, Hritan); Arabic for all others (Iraq Arab + Syria).

**Emails:** 16 companies (19 addresses). 9 sent successfully (Meskent, Darin, Halkawt,
Hritan ×3, Al Sultan, Iraqi Hadeed, Al-Rasheed/pr@). Remaining 11 addresses pending –
Gmail temporarily blocked SMTP after the bulk run (see README, "Important lessons").
Resume-safe: `send_emails.py` skips entries already in `logs/Steel_Email_Log.txt`.

**WhatsApp (Selenium, reliable method):**
- Meskent Group (2 numbers) delivered ✅
- Remaining: NOT_LOADED / NO_INPUT / session invalidated → needs QR re-scan, then rerun
  `send_whatsapp_selenium.py`.
- Profile: copy of the Chrome profile, logged into WhatsApp Business.

**Templates:** `templates/steel_ckb.txt`, `steel_ar.txt`.

**Run:** `python send_emails.py` (emails, resume-safe) / `python send_whatsapp_selenium.py`