import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_config():
    path = os.path.join(ROOT, "config.json")
    if not os.path.exists(path):
        raise SystemExit(
            "config.json not found. Copy config.example.json to config.json "
            "and fill in your Gmail app password and Telegram bot credentials."
        )
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_template(name):
    path = os.path.join(ROOT, "templates", name)
    with open(path, encoding="utf-8") as f:
        return f.read()