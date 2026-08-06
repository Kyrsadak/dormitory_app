import urllib.request
import urllib.parse
import json
import time
import datetime
import threading
import sys
import os

# Import local db module
sys.path.append(os.path.dirname(__file__))
import db

# Telegram Bot Token (Can be passed via argument or environment variable TELEGRAM_BOT_TOKEN)
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")

# Save target group chat ID for daily auto-notifications
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "bot_config.json")

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"chat_id": None, "notify_time": "09:00", "last_notified_date": None}

def save_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

config = load_config()

def telegram_api(method, payload=None):
    if not BOT_TOKEN:
        print("[Telegram Bot] Error: BOT_TOKEN is empty.")
        return None

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/{method}"
    try:
        data = json.dumps(payload).encode("utf-8") if payload else None
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            return res_data
    except Exception as e:
        print(f"[Telegram Bot API Error] {method}: {e}")
        return None

def send_message(chat_id, text, reply_markup=None):
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    return telegram_api("sendMessage", payload)

def edit_message(chat_id, message_id, text, reply_markup=None):
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text,
        "parse_mode": "HTML"
    }
    if reply_markup is not None:
        payload["reply_markup"] = reply_markup
    return telegram_api("editMessageText", payload)

def answer_callback_query(callback_query_id, text=""):
    payload = {
        "callback_query_id": callback_query_id,
        "text": text
    }
    return telegram_api("answerCallbackQuery", payload)

def format_duty_message(duty_item):
    if not duty_item:
        return "⚠️ Данные о дежурстве не найдены."

    date_str = duty_item["date"]
    room_num = duty_item["room_number"]
    status = duty_item["status"]
    residents = duty_item["residents"]

    res_names = "\n".join([f"  • <b>{r['full_name']}</b> (@{r['nickname']})" if r.get('nickname') else f"  • <b>{r['full_name']}</b>" for r in residents])
    if not res_names:
        res_names = "  • <i>В комнате никто не живет</i>"

    status_icon = "✅ <b>ВЫПОЛНЕНО</b>" if status == "completed" else "⏳ <b>ОЖИДАЕТ ВЫПОЛНЕНИЯ</b>"

    msg = f"🧹 <b>ГРАФИК ДЕЖУРСТВА ПО КУХНЕ (7 ЭТАЖ)</b>\n"
    msg += f"📅 <b>Дата:</b> {date_str}\n"
    msg += f"📍 <b>Статус:</b> {status_icon}\n\n"
    msg += f"🔷 <b>СЕГОДНЯ ДЕЖУРИТ КОМНАТА {room_num}:</b>\n"
    msg += f"{res_names}\n\n"
    msg += f"📌 <b>Обязанность:</b> Навести порядок на кухне 7 этажа и вынести мусор в бак."

    return msg

def get_duty_keyboard(duty_item):
    if not duty_item or duty_item["status"] == "completed":
        return None

    duty_date = duty_item["date"]
    keyboard = {
        "inline_keyboard": [
            [
                {
                    "text": "✅ Мы выполнили дежурство!",
                    "callback_data": f"done:{duty_date}:7"
                }
            ]
        ]
    }
    return keyboard

def send_today_duty_notification(chat_id):
    today_duty = db.get_today_duty()
    item = today_duty.get(7)

    if not item:
        send_message(chat_id, "⚠️ На сегодня нет назначенных дежурных комнат.")
        return

    text = format_duty_message(item)
    keyboard = get_duty_keyboard(item)
    send_message(chat_id, text, reply_markup=keyboard)

def handle_command(message):
    chat_id = message["chat"]["id"]
    text = message.get("text", "").strip()

    if text in ["/start", "/help"]:
        # Save group chat ID for automatic notifications
        config["chat_id"] = chat_id
        save_config(config)

        welcome_msg = (
            "👋 <b>Привет! Я бот Общежития по дежурству на кухне.</b>\n\n"
            "📌 <b>Команды бота:</b>\n"
            "• /duty или /today — Узнать кто сегодня дежурит и отметить выполнение\n"
            "• /setgroup — Привязать этот чат для ежедневных напоминаний в 09:00\n\n"
            "<i>Все отметки о выполнении мгновенно синхронизируются с веб-сайтом!</i>"
        )
        send_message(chat_id, welcome_msg)

    elif text in ["/duty", "/today", "/dezhurstvo"]:
        send_today_duty_notification(chat_id)

    elif text == "/setgroup":
        config["chat_id"] = chat_id
        save_config(config)
        send_message(chat_id, "✅ <b>Группа успешно привязана!</b> Теперь каждое утро сюда будет приходить напоминание о дежурных.")

def handle_callback_query(cb):
    cb_id = cb["id"]
    chat_id = cb["message"]["chat"]["id"]
    msg_id = cb["message"]["message_id"]
    data = cb.get("data", "")

    if data.startswith("done:"):
        parts = data.split(":")
        duty_date = parts[1]
        floor = int(parts[2])

        # Mark in SQLite Database
        db.mark_duty_status(duty_date, floor, "completed", notes="Отмечено через Telegram бота")

        # Answer callback popup
        answer_callback_query(cb_id, "✅ Дежурство успешно отмечено как выполненное!")

        # Update Telegram message
        user_name = cb.get("from", {}).get("first_name", "Студент")
        
        today_duty = db.get_today_duty()
        item = today_duty.get(7)

        updated_text = format_duty_message(item) + f"\n\n🎉 <i>Отмечено пользователем {user_name} в Telegram!</i>"
        edit_message(chat_id, msg_id, updated_text, reply_markup=None)

def daily_scheduler_loop():
    """Background thread to send automatic morning duty reminders."""
    print("[Telegram Bot Scheduler] Started.")
    while True:
        try:
            now = datetime.datetime.now()
            today_str = now.strftime("%Y-%m-%d")
            time_str = now.strftime("%H:%M")

            target_time = config.get("notify_time", "09:00")
            last_date = config.get("last_notified_date")
            chat_id = config.get("chat_id")

            if chat_id and time_str == target_time and last_date != today_str:
                print(f"[Telegram Bot Scheduler] Sending daily reminder to chat {chat_id}")
                send_today_duty_notification(chat_id)
                config["last_notified_date"] = today_str
                save_config(config)

        except Exception as e:
            print(f"[Telegram Bot Scheduler Error]: {e}")

        time.sleep(30)

def run_bot(token=None):
    global BOT_TOKEN
    if token:
        BOT_TOKEN = token

    if not BOT_TOKEN:
        print("\n========================================================")
        print("❌ ОШИБКА: Не указан TELEGRAM_BOT_TOKEN!")
        print("Инструкция:")
        print("1. Создайте бота у @BotFather в Telegram и скопируйте ТОКЕН.")
        print("2. Запустите бота командой: python telegram_bot.py YOUR_BOT_TOKEN")
        print("========================================================\n")
        return

    print(f"🤖 Telegram Бот Общежития запущен и слушает сообщения...")

    # Start Scheduler Thread
    scheduler_thread = threading.Thread(target=daily_scheduler_loop, daemon=True)
    scheduler_thread.start()

    offset = 0
    while True:
        try:
            updates = telegram_api("getUpdates", {"offset": offset, "timeout": 30})
            if updates and updates.get("ok"):
                for item in updates.get("result", []):
                    offset = item["update_id"] + 1

                    if "message" in item:
                        handle_command(item["message"])
                    elif "callback_query" in item:
                        handle_callback_query(item["callback_query"])
        except Exception as e:
            print(f"[Bot Loop Error]: {e}")

        time.sleep(1)

if __name__ == "__main__":
    token_arg = sys.argv[1] if len(sys.argv) > 1 else None
    run_bot(token_arg)
