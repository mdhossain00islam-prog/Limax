# -*- coding: utf-8 -*-
import os
import asyncio
import re
import requests
import time
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

# ===== CONFIG =====
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
MY_USER = os.getenv("MY_USER")
MY_PASS = os.getenv("MY_PASS")

TARGET_URL = "http://2.59.169.96/ints/agent/SMSCDRStats"
LOGIN_URL = "http://2.59.169.96/ints/login"

# ✅ Firebase URL
FB_URL = "https://mhnirob-default-rtdb.firebaseio.com/bot"

ADMIN_LINK = "https://t.me/Mhnirob1"
BOT_LINK = "https://t.me/tsall_bot"
DV_LINK = "https://t.me/Mhnirob1"
CN_LINK = "https://t.me/TS_CHENNEL"

sent_msgs = {}
START_TIME = time.time()

# ===== FIREBASE FUNCTION (UPDATED) =====
def update_firebase(num, msg, date_str, cli_source):
    try:
        unique_id = f"{num}_{int(time.time()*1000)}"  # ✅ unique key
        url = f"{FB_URL}/sms_logs/{num}.json"

        payload = {
            "number": num,
            "message": msg,
            "time": date_str,
            "service": cli_source,   # ✅ added
            "paid": False
        }

        requests.put(url, json=payload, timeout=5)

    except Exception as e:
        print("Firebase Error:", e)


# ===== UTILITIES =====
def extract_otp(msg):
    match = re.search(r'\b\d{3,4}(?:[ -]?\d{3,4})?\b', msg)

    if match:
        otp = match.group(0)

        # space ও dash remove
        otp = re.sub(r'[\s-]', '', otp)

        return otp

    return "N/A"

def send_telegram(date_str, num, sms_text, otp, cli_source, is_update=False):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    masked = num[:4] + "TS" + num[-4:] if len(num) > 8 else num

    header = "🔄🛎️ <b>UPDATED SMS RECEIVED</b>" if is_update else "🛎️ <b>NEW SMS RECEIVED</b>"

    text = f"{header}\n\n" \
           f"📞 <b>Number:</b> <code>{masked}</code>\n" \
           f"🌐 <b>Service:</b> <code>{cli_source}</code>\n\n" \
           f"🔑 <b>OTP:</b> <code>{otp}</code>\n\n" \
           f"📩 <b>Full Message:</b><blockquote>{sms_text}</blockquote>\n"

    keyboard = [
        [
            {"text": "👨‍🦲Admin", "url": ADMIN_LINK},
            {"text": "🔢Number bot", "url": BOT_LINK}
        ],
        [
            {"text": "💥Channel", "url": CN_LINK},
            {"text": "💻 Developer", "url": DV_LINK}
        ]
    ]

    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "reply_markup": {"inline_keyboard": keyboard}
    }

    try:
        res = requests.post(url, json=payload, timeout=10)
        return res.status_code == 200
    except:
        return False


# ===== MAIN BOT =====
async def start_bot():
    print("🚀 Bot started...")

    async with Stealth().use_async(async_playwright()) as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox"])
        context = await browser.new_context(viewport={'width': 1280, 'height': 720})
        page = await context.new_page()

        async def login():
            try:
                await page.goto(LOGIN_URL, wait_until="networkidle", timeout=60000)

                await page.evaluate(f"""() => {{
                    const myUser = "{MY_USER}";
                    const myPass = "{MY_PASS}";
                    let userField, passField, ansField;

                    document.querySelectorAll('input').forEach(inp => {{
                        let p = (inp.placeholder || "").toLowerCase();

                        if (inp.type === 'password') passField = inp;
                        else if (p.includes('user') || inp.type === 'text') {{
                            if (!userField && !p.includes('answer')) userField = inp;
                        }}

                        if (p.includes('answer')  (inp.name  "").includes('ans')) ansField = inp;
                    }});

                    let match = document.body.innerText.match(/What is\\s+(\\d+)\\s*\\+\\s*(\\d+)/i);
                    let sum = match ? (parseInt(match[1]) + parseInt(match[2])) : "";
