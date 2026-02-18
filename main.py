import os
import requests
import threading
from telethon import TelegramClient, events
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

CHAT_IDS = [int(x.strip()) for x in os.getenv("CHAT_IDS").split(",")]
CHANNEL_IDS = [int(x.strip()) for x in os.getenv("CHANNEL_IDS").split(",")]

client = TelegramClient("session", API_ID, API_HASH)

# =========================
# КЛЮЧЕВЫЕ СЛОВА ЗАКАЗОВ
# =========================
KEYWORDS_INTENT = [
    "ищу", "ищем", "нужен", "нужна", "нужно",
    "требуется", "интересует", "кто может"
]

KEYWORDS_PRODUCTION = [
    "пошив", "производство", "фабрика", "цех",
    "отшить", "швейн", "ателье", "закройщ"
]

KEYWORDS_PRODUCT = [
    "футболк", "худи", "лонгслив", "брюк",
    "шорт", "юбк", "куртк", "пальто", "пижам"
]

KEYWORDS_FABRIC = [
    "ткан", "трикотаж", "футер", "кулир",
    "рибана", "кашкорсе", "вискоз",
    "флис", "шифон"
]

KEYWORDS_VOLUME = [
    "шт", "штук", "партия", "тираж",
    "100", "200", "300", "500", "1000"
]

# =========================
# ❌ СТОП-СЛОВА (НЕ ЗАКАЗЫ)
# =========================
BLACKLIST = [
    # вакансии / поиск сотрудников
    "вакансия", "работа", "сотрудник", "сотрудники",
    "менеджер", "ассистент", "оператор",
    "удалён", "удален", "зарплата", "зп",
    "оклад", "график", "обязанности",
    "требуется сотрудник", "нужны люди",
    "без опыта", "лс", "личные сообщения",

    # маркетплейсы
    "avito", "озон", "ozon", "wildberries", "вб",
    "маркетплейс"
]

LOGS = []

# =========================
def send_to_all(text: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    for chat_id in CHAT_IDS:
        try:
            requests.post(url, data={
                "chat_id": chat_id,
                "text": text
            })
        except Exception as e:
            print(f"Ошибка отправки в {chat_id}: {e}")

# =========================
def looks_like_job_post(text: str) -> bool:
    """
    Дополнительная защита от вакансий
    """
    t = text.lower()

    job_patterns = [
        "зарплата",
        "обязанности",
        "условия",
        "график",
        "в команду",
        "ищем сотрудника",
        "ищем менеджера",
        "нужны люди",
        "на работу",
    ]

    return any(p in t for p in job_patterns)

# =========================
def is_order_request(text: str) -> bool:
    t = text.lower()

    # стоп-слова → сразу игнор
    if any(b in t for b in BLACKLIST):
        return False

    # выглядит как вакансия → игнор
    if looks_like_job_post(t):
        return False

    intent = any(k in t for k in KEYWORDS_INTENT)
    production = any(k in t for k in KEYWORDS_PRODUCTION)
    product = any(k in t for k in KEYWORDS_PRODUCT)
    fabric = any(k in t for k in KEYWORDS_FABRIC)
    volume = any(k in t for k in KEYWORDS_VOLUME)

    if intent and (production or product):
        return True

    if intent and fabric:
        return True

    if product and volume:
        return True

    return False

# =========================
def make_link(chat, msg_id: int) -> str:
    if getattr(chat, "username", None):
        return f"https://t.me/{chat.username}/{msg_id}"

    return f"https://t.me/c/{str(chat.id)[4:]}/{msg_id}"

# =========================
@client.on(events.NewMessage(chats=CHANNEL_IDS))
async def handler(event):
    text = event.message.text or ""
    if not text:
        return

    if not is_order_request(text):
        return

    chat = await event.get_chat()
    title = getattr(chat, "title", "Группа/канал")
    link = make_link(chat, event.message.id)

    message = (
        "🧵 ПОХОЖЕ НА ЗАКАЗ\n"
        f"📢 {title}\n"
        f"🔗 {link}\n\n"
        f"{text[:900]}"
    )

    send_to_all(message)
    LOGS.append(f"[{title}] {text[:50]}")

# =========================
def check_commands():
    last_update_id = 0

    while True:
        try:
            response = requests.get(
                f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates",
                params={"offset": last_update_id + 1}
            ).json()

            for update in response.get("result", []):
                last_update_id = update["update_id"]

                msg = update.get("message", {})
                if msg.get("text") == "/check":
                    chat_id = msg["chat"]["id"]

                    status = (
                        "✅ Бот работает\n"
                        f"Каналов: {len(CHANNEL_IDS)}\n\n"
                        "Последние логи:\n"
                        + ("\n".join(LOGS[-10:]) if LOGS else "нет")
                    )

                    requests.post(
                        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                        data={
                            "chat_id": chat_id,
                            "text": status
                        }
                    )

        except Exception as e:
            print("Ошибка check_commands:", e)

# =========================
print("🚀 Бот запущен и фильтрует ТОЛЬКО заказы...")

threading.Thread(
    target=check_commands,
    daemon=True
).start()

client.start()
client.run_until_disconnected()
