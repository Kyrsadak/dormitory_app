import urllib.request
import urllib.parse
import json
import time
import datetime
import threading
import sys
import os

# Import local modules
sys.path.append(os.path.dirname(__file__))
import db
import excel_sync

# Telegram Bot Token (Can be passed via argument or environment variable TELEGRAM_BOT_TOKEN)
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8558094760:AAFOanWcpS0PR5uhWU9k2ed-XQpIWWt2Fhg")

# Admin Telegram User IDs (Allowed all admin features in Telegram)
ADMIN_TELEGRAM_IDS = [7990114364]
env_admin_id = os.environ.get("ADMIN_TELEGRAM_ID")
if env_admin_id:
    try:
        ADMIN_TELEGRAM_IDS.append(int(env_admin_id))
    except ValueError:
        pass

# Config file for group chat ID & settings
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "bot_config.json")
EXCEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Лист Microsoft Excel.xlsx"))

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
        with urllib.request.urlopen(req, timeout=40) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            return res_data
    except Exception as e:
        if "timed out" not in str(e).lower():
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

def answer_callback_query(callback_query_id, text="", show_alert=False):
    payload = {
        "callback_query_id": callback_query_id,
        "text": text,
        "show_alert": show_alert
    }
    return telegram_api("answerCallbackQuery", payload)

def is_admin(user_id):
    return user_id in ADMIN_TELEGRAM_IDS

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

def get_admin_keyboard():
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "📊 Статистика", "callback_data": "adm:stats"},
                {"text": "📑 Журнал логов", "callback_data": "adm:logs"}
            ],
            [
                {"text": "🧹 Сменить дежурного", "callback_data": "adm:setduty_prompt"},
                {"text": "👥 Список жильцов", "callback_data": "adm:list"}
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
    user_id = message.get("from", {}).get("id")
    text = message.get("text", "").strip()

    if text in ["/start", "/help"]:
        config["chat_id"] = chat_id
        save_config(config)

        admin_note = "\n\n👑 <b>Вы распознаны как Главный Администратор!</b> Используйте /admin для доступа к меню управления." if is_admin(user_id) else ""

        welcome_msg = (
            "👋 <b>Привет! Я бот Общежития по дежурству на кухне.</b>\n\n"
            "📌 <b>Доступные команды:</b>\n"
            "• /duty или /today — Узнать кто сегодня дежурит и отметить выполнение\n"
            "• /setgroup — Привязать этот чат для ежедневных напоминаний в 09:00\n"
            f"{admin_note}\n"
            "<i>Все отметки и изменения мгновенно синхронизируются с веб-сайтом!</i>"
        )
        send_message(chat_id, welcome_msg)

    elif text in ["/duty", "/today", "/dezhurstvo"]:
        send_today_duty_notification(chat_id)

    elif text == "/setgroup":
        config["chat_id"] = chat_id
        save_config(config)
        send_message(chat_id, "✅ <b>Группа успешно привязана!</b> Теперь каждое утро в 09:00 сюда будет приходить напоминание о дежурных.")

    # --- ADMIN COMMANDS ---
    elif text in ["/admin", "/menu"]:
        if not is_admin(user_id):
            send_message(chat_id, f"⛔ <b>Доступ запрещен.</b> Панель администратора доступна только владельцу (ID: 7990114364). Ваш ID: <code>{user_id}</code>")
            return

        admin_msg = (
            "👑 <b>ПАНЕЛЬ АДМИНИСТРАТОРА ОБЩЕЖИТИЯ</b>\n\n"
            "Вы авторизованы как Администратор системы.\n\n"
            "📌 <b>Быстрые команды управления:</b>\n"
            "• <code>/add ФИО | Ник | Пол(M/F) | Комната</code> — Заселить жильца\n"
            "• <code>/evict ID_или_ФИО</code> — Выселить жильца\n"
            "• <code>/move ID Комната</code> — Переселить жильца\n"
            "• <code>/setduty YYYY-MM-DD Комната</code> — Назначить дежурство\n"
            "• /stats — Статистика общежития\n"
            "• /logs — Последние логи действий\n"
            "• /list — Список всех проживающих"
        )
        send_message(chat_id, admin_msg, reply_markup=get_admin_keyboard())

    elif text == "/stats":
        stats = db.get_stats()
        msg = (
            "📊 <b>СТАТИСТИКА ОБЩЕЖИТИЯ (PROD)</b>\n\n"
            f"• Всего жильцов: <b>{stats['total_residents']}</b>\n"
            f"• 2 Этаж (Женский): <b>{stats['floor2_count']}</b> чел.\n"
            f"• 7 Этаж (Мужской): <b>{stats['floor7_count']}</b> чел.\n"
            f"• Временные (14 дней): <b>{stats['temp_count']}</b> чел.\n"
            f"• В очереди: <b>{stats['waiting_count']}</b> чел.\n"
            f"• Свободных койко-мест: <b>{stats['free_beds']}</b> из {stats['total_capacity']}"
        )
        send_message(chat_id, msg)

    elif text == "/logs":
        if not is_admin(user_id):
            send_message(chat_id, "⛔ Ошибка доступа.")
            return

        logs = db.get_activity_logs(10)
        log_lines = "\n".join([f"• <i>{l['timestamp']}</i> — <b>{l['action']}</b>: {l['details']}" for l in logs])
        send_message(chat_id, f"📑 <b>ЖУРНАЛ ПОСЛЕДНИХ ДЕЙСТВИЙ (АУДИТ):</b>\n\n{log_lines}")

    elif text == "/list":
        if not is_admin(user_id):
            send_message(chat_id, "⛔ Ошибка доступа.")
            return

        floors_data = db.get_floors_data()
        msg = "👥 <b>СПИСОК ПРОЖИВАЮЩИХ ПО КОМНАТАМ:</b>\n\n"
        
        for fl_num in [2, 7]:
            rooms = floors_data["floors"].get(fl_num, [])
            msg += f"<b>{fl_num} ЭТАЖ:</b>\n"
            for rm in rooms:
                if rm["residents"]:
                    names = ", ".join([f"{r['full_name']} (ID:#{r['id']})" for r in rm["residents"]])
                    msg += f"  • <b>Комн. {rm['room_number']}:</b> {names}\n"
            msg += "\n"

        send_message(chat_id, msg)

    elif text.startswith("/add"):
        if not is_admin(user_id):
            send_message(chat_id, "⛔ Ошибка доступа.")
            return

        # Format: /add ФИО | Ник | M/F | Комната
        try:
            parts = text[4:].strip().split("|")
            full_name = parts[0].strip()
            nickname = parts[1].strip() if len(parts) > 1 else ""
            gender = parts[2].strip().upper() if len(parts) > 2 else "M"
            room_num = parts[3].strip() if len(parts) > 3 else None

            res_id = db.add_resident(full_name, nickname, "", gender, room_num, "permanent")
            excel_sync.export_db_to_excel(db.DB_PATH, EXCEL_PATH)
            send_message(chat_id, f"✅ <b>Жилец успешно заселен!</b>\nID: #{res_id}\nФИО: {full_name}\nКомната: {room_num or 'В очереди'}")
        except Exception as e:
            send_message(chat_id, "⚠️ <b>Формат команды:</b>\n<code>/add ФИО | Ник | M/F | НомерКомнаты</code>\n\n<i>Пример:</i>\n<code>/add Иванов Иван | ivanov_i | M | 705</code>")

    elif text.startswith("/evict"):
        if not is_admin(user_id):
            send_message(chat_id, "⛔ Ошибка доступа.")
            return

        try:
            val = text[6:].strip()
            res_id = int(val)
            db.evict_resident(res_id)
            excel_sync.export_db_to_excel(db.DB_PATH, EXCEL_PATH)
            send_message(chat_id, f"✅ <b>Жилец ID #{res_id} успешно выселен!</b> Статус обновлен на сайте и в Excel.")
        except Exception:
            send_message(chat_id, "⚠️ <b>Формат команды:</b>\n<code>/evict ID_жильца</code>\n\n<i>Пример:</i> <code>/evict 15</code>")

    elif text.startswith("/move"):
        if not is_admin(user_id):
            send_message(chat_id, "⛔ Ошибка доступа.")
            return

        try:
            parts = text[5:].strip().split()
            res_id = int(parts[0])
            new_room = parts[1]

            conn = db.get_db_connection()
            c = conn.cursor()
            c.execute("SELECT * FROM residents WHERE id = ?", (res_id,))
            res = c.fetchone()
            conn.close()

            if res:
                db.update_resident(res_id, res["full_name"], res["nickname"] or "", res["profile_url"] or "", res["gender"], new_room, res["status"])
                excel_sync.export_db_to_excel(db.DB_PATH, EXCEL_PATH)
                send_message(chat_id, f"✅ <b>Жилец {res['full_name']} переселен в комнату {new_room}!</b>")
            else:
                send_message(chat_id, "⚠️ Жилец с таким ID не найден.")
        except Exception:
            send_message(chat_id, "⚠️ <b>Формат команды:</b>\n<code>/move ID_жильца НоваяКомната</code>\n\n<i>Пример:</i> <code>/move 15 706</code>")

    elif text.startswith("/setduty"):
        if not is_admin(user_id):
            send_message(chat_id, "⛔ Ошибка доступа.")
            return

        try:
            parts = text[8:].strip().split()
            duty_date = parts[0]
            room_num = parts[1]

            db.set_manual_duty(duty_date, 7, room_num, "pending", "Назначено через Telegram админа")
            excel_sync.export_db_to_excel(db.DB_PATH, EXCEL_PATH)
            send_message(chat_id, f"✅ <b>Дежурство на {duty_date} назначено на комнату {room_num}!</b> Данные обновлены на сайте.")
        except Exception:
            send_message(chat_id, "⚠️ <b>Формат команды:</b>\n<code>/setduty ГГГГ-ММ-ДД НомерКомнаты</code>\n\n<i>Пример:</i> <code>/setduty 2026-08-10 706</code>")

def handle_callback_query(cb):
    cb_id = cb["id"]
    chat_id = cb["message"]["chat"]["id"]
    msg_id = cb["message"]["message_id"]
    user_id = cb.get("from", {}).get("id")
    data = cb.get("data", "")

    if data.startswith("done:"):
        parts = data.split(":")
        duty_date = parts[1]
        floor = int(parts[2])

        # 1. Immediately answer callback so Telegram removes loading spinner
        answer_callback_query(cb_id, "✅ Дежурство успешно отмечено как выполненное!", show_alert=True)

        # 2. Mark in SQLite Database & Sync Excel
        db.mark_duty_status(duty_date, floor, "completed", notes="Отмечено кнопкой в Telegram")
        excel_sync.export_db_to_excel(db.DB_PATH, EXCEL_PATH)

        # 3. Update Telegram message text
        user_name = cb.get("from", {}).get("first_name", "Студент")
        today_duty = db.get_today_duty()
        item = today_duty.get(7)

        updated_text = format_duty_message(item) + f"\n\n🎉 <b>ОТМЕЧЕНО ВЫПОЛНЕННЫМ:</b> {user_name} в Telegram!\n<i>Статус мгновенно синхронизирован с веб-сайтом!</i>"
        edit_message(chat_id, msg_id, updated_text, reply_markup=None)

    elif data == "adm:stats":
        stats = db.get_stats()
        answer_callback_query(cb_id, f"Жильцов: {stats['total_residents']} | Свободно мест: {stats['free_beds']}", show_alert=True)

    elif data == "adm:logs":
        if not is_admin(user_id):
            answer_callback_query(cb_id, "⛔ Нет прав доступа", show_alert=True)
            return
        logs = db.get_activity_logs(5)
        log_lines = "\n".join([f"• {l['action']}: {l['details']}" for l in logs])
        answer_callback_query(cb_id, log_lines, show_alert=True)

    elif data == "adm:setduty_prompt":
        answer_callback_query(cb_id, "Отправьте команду:\n/setduty YYYY-MM-DD НомерКомнаты", show_alert=True)

    elif data == "adm:list":
        answer_callback_query(cb_id, "Используйте команду /list для просмотра полного списка", show_alert=True)

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
        print("========================================================\n")
        return

    print(f"[Telegram Bot] Running for Admin ID: 7990114364...")

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
            if "timed out" not in str(e).lower():
                print(f"[Bot Loop Error]: {e}")

        time.sleep(1)

def start_bot_in_background(token=None):
    """Start Telegram bot loop in a daemon thread so it runs automatically with server.py in the cloud."""
    bot_thread = threading.Thread(target=run_bot, args=(token,), daemon=True)
    bot_thread.start()
    print("[Telegram Bot] Launched in background thread.")

if __name__ == "__main__":
    token_arg = sys.argv[1] if len(sys.argv) > 1 else None
    run_bot(token_arg)
