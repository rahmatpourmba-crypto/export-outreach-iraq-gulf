"""
Campaign 04 - Steel WhatsApp via Selenium (RELIABLE method).
Requires a Chrome profile already logged into WhatsApp Web.
Prerequisite: scan the QR code once so the profile session stays active.
"""
import sys, io, time, os, datetime
sys.path.insert(0, r"C:\Users\Admin\Documents\Default Project\export-outreach-iraq-gulf\common")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", write_through=True)
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", write_through=True)
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import config as cf

MY_NAME = cf.load_config()["candidate"]["name"]
MSG_CKB = cf.load_template("steel_ckb.txt")
MSG_AR = cf.load_template("steel_ar.txt")

LOG = os.path.join(os.path.dirname(__file__), "..", "..", "logs", "Steel_WhatsApp_Log.txt")
LOG = os.path.abspath(LOG)

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PROFILE = os.environ.get("WA_PROFILE", r"C:\Users\Admin\AppData\Local\Temp\opencode\wa_profile")

COMPANIES = [
    ("Meskent Group", "+9647504467931; +9647512225555", "ckb"),
    ("Darin Steel", "+9647502950001", "ckb"),
    ("Van Steel Iraq", "+9647502036262; +9647737273333", "ckb"),
    ("Halkawt Steel", "+964662514013", "ckb"),
    ("Yaaqub Group", "+9647703550960", "ckb"),
    ("Erbil Steel Company", "+9647504351818", "ckb"),
    ("Hritan Iron & Steel", "+9647708849352; +9647733738738; +9647800442035", "ckb"),
    ("Qasr Al-Maaden", "+9647903960030", "ar"),
    ("Al Sultan Group", "+9647702735970; +9647722222335", "ar"),
    ("Aradh Alhadeed", "+9647733333544; +9647901874632", "ar"),
    ("Iraqi Hadeed", "+9647770010700; +9647870010700", "ar"),
    ("Al-Rasheed International Trading", "+201103845000; +201144453000", "ar"),
    ("AL-Fairoz Al-Thahabi", "+9647730957222; +9647739093531", "ar"),
    ("Khan Alhadeed", "+9647812229099", "ar"),
    ("Maalim Al-Asima", "+9647731313156", "ar"),
    ("Bilad Alwafaa", "+9647509385152", "ar"),
    ("Alam Al-Hadid", "+9647504441797; +9647511111797", "ar"),
    ("Star Steel Iraq", "+9647707007800; +9647855556060", "ar"),
    ("State Company for Iron and Steel", "+9647801025474", "ar"),
    ("Basra Steel Galvanizing", "+9647811111767", "ar"),
    ("Steel Syria", "+963214731045; +963214731046; +963214731057", "ar"),
    ("Isnad", "+963115855016", "ar"),
    ("Mediterranean Steel", "+963115851281", "ar"),
    ("ALLOH Steel Industries", "+963116216584; +963944282628", "ar"),
    ("Syrian Steel & Iron Company (Salb)", "+963115851110; +963115851112; +963115851113; +963947777602", "ar"),
    ("Steel Tech Company", "+963115851240", "ar"),
]

opts = Options()
opts.binary_location = CHROME
opts.add_argument(f"--user-data-dir={PROFILE}")
opts.add_argument("--profile-directory=Default")
opts.add_argument("--disable-notifications")
opts.add_argument("--no-first-run")
opts.add_argument("--remote-debugging-port=0")
opts.add_experimental_option("excludeSwitches", ["enable-automation"])
opts.add_experimental_option("useAutomationExtension", False)

d = webdriver.Chrome(options=opts)
d.get("https://web.whatsapp.com/")
time.sleep(25)

with open(LOG, "w", encoding="utf-8") as f:
    f.write(f"واتساپ فولاد (Selenium v4) - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    f.write("=" * 60 + "\n")

try:
    WebDriverWait(d, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="chat-list"]')))
    print("LOGIN OK", flush=True)
except Exception:
    print("FATAL: NOT LOGGED IN - scan QR code in the opened Chrome window", flush=True)
    d.quit()
    sys.exit(1)

sent = 0
for idx, (company, nums, lang) in enumerate(COMPANIES):
    msg = (MSG_CKB if lang == "ckb" else MSG_AR).format(company=company, my=MY_NAME)
    for num in [n.strip() for n in nums.split(";")]:
        digits = "".join(ch for ch in num if ch.isdigit())
        try:
            d.execute_script(f"window.location.href='https://web.whatsapp.com/send?phone={digits}'")
            time.sleep(14)
            url = d.current_url
            if "accept?code" in url:
                print(f"SKIP    {lang:3s} {company}  {num}  NO_WHATSAPP", flush=True)
                continue
            box = None
            try:
                box = WebDriverWait(d, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[contenteditable="true"][data-tab="10"]'))
                )
                aria = (box.get_attribute("aria-label") or "").replace(" ", "")
                if digits not in aria:
                    print(f"FAIL    {lang:3s} {company}  {num}  WRONG_CHAT({aria[:40]})", flush=True)
                    continue
            except Exception:
                print(f"FAIL    {lang:3s} {company}  {num}  NO_INPUT", flush=True)
                continue
            box.click()
            box.send_keys(msg)
            time.sleep(2)
            btns = d.find_elements(By.CSS_SELECTOR, 'button[data-testid="send"]')
            if btns:
                btns[0].click()
            else:
                box.send_keys(Keys.ENTER)
            time.sleep(5)
            sent += 1
            print(f"SENT    {lang:3s} {company}  {num}", flush=True)
        except Exception as e:
            print(f"ERR     {lang:3s} {company}  {num}  {str(e)[:80]}", flush=True)

print(f"TOTAL SENT: {sent}", flush=True)
time.sleep(3)
d.quit()