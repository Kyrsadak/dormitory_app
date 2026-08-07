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
import bot_locales

# Telegram Bot Token
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8558094760:AAFOanWcpS0PR5uhWU9k2ed-XQpIWWt2Fhg")

# Main Owner Telegram ID
MAIN_OWNER_ID = 7990114364

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "bot_config.json")
EXCEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Лист Microsoft Excel.xlsx"))
RULES_PDF_PATH = os.path.join(os.path.dirname(__file__), "Правила_проживания_в_общежитии_2.pdf")

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if "admin_ids" not in data or not isinstance(data["admin_ids"], list):
                    data["admin_ids"] = [MAIN_OWNER_ID]
                elif MAIN_OWNER_ID not in data["admin_ids"]:
                    data["admin_ids"].append(MAIN_OWNER_ID)
                return data
        except Exception:
            pass
    return {"chat_id": None, "notify_time": "09:00", "last_notified_date": None, "admin_ids": [MAIN_OWNER_ID]}

def save_config(cfg):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)

config = load_config()

def is_admin(user_id):
    if not user_id:
        return False
    return user_id in config.get("admin_ids", [MAIN_OWNER_ID])

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

def send_document(chat_id, file_path, caption=None):
    if not BOT_TOKEN:
        print("[Telegram Bot] Error: BOT_TOKEN is empty.")
        return None
    if not os.path.exists(file_path):
        print(f"[Telegram Bot] Error: File not found at {file_path}")
        return None

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    filename = os.path.basename(file_path)

    try:
        with open(file_path, "rb") as f:
            file_bytes = f.read()

        body = []
        body.append(f"--{boundary}".encode())
        body.append(b'Content-Disposition: form-data; name="chat_id"')
        body.append(b"")
        body.append(str(chat_id).encode())

        if caption:
            body.append(f"--{boundary}".encode())
            body.append(b'Content-Disposition: form-data; name="caption"')
            body.append(b'Content-Type: text/plain; charset=utf-8')
            body.append(b"")
            body.append(caption.encode())

            body.append(f"--{boundary}".encode())
            body.append(b'Content-Disposition: form-data; name="parse_mode"')
            body.append(b"")
            body.append(b"HTML")

        body.append(f"--{boundary}".encode())
        body.append(f'Content-Disposition: form-data; name="document"; filename="{filename}"'.encode())
        body.append(b"Content-Type: application/pdf")
        body.append(b"")
        body.append(file_bytes)

        body.append(f"--{boundary}--".encode())
        body.append(b"")

        payload = b"\r\n".join(body)

        req = urllib.request.Request(url, data=payload, headers={
            "Content-Type": f"multipart/form-data; boundary={boundary}"
        })
        with urllib.request.urlopen(req, timeout=60) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            return res_data
    except Exception as e:
        print(f"[Telegram Bot API sendDocument Error]: {e}")
        return None

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

def format_duty_message(duty_item, chat_type='private', user_id=None):
    if not duty_item:
        return bot_locales.t(chat_type, user_id, "duty_not_found")

    date_str = duty_item["date"]
    room_num = duty_item["room_number"]
    status = duty_item["status"]
    residents = duty_item["residents"]

    res_names = "\n".join([f"  • <b>{r['full_name']}</b> (@{r['nickname']})" if r.get('nickname') else f"  • <b>{r['full_name']}</b>" for r in residents])
    if not res_names:
        res_names = bot_locales.t(chat_type, user_id, "duty_no_residents")

    status_icon = bot_locales.t(chat_type, user_id, "duty_status_completed") if status == "completed" else bot_locales.t(chat_type, user_id, "duty_status_pending")

    msg = f"{bot_locales.t(chat_type, user_id, 'duty_title')}\n"
    msg += f"{bot_locales.t(chat_type, user_id, 'duty_date', date_str=date_str)}\n"
    msg += f"{bot_locales.t(chat_type, user_id, 'duty_status', status_icon=status_icon)}\n\n"
    msg += f"{bot_locales.t(chat_type, user_id, 'duty_today_room', room_num=room_num)}\n"
    msg += f"{res_names}\n\n"
    msg += f"{bot_locales.t(chat_type, user_id, 'duty_task')}"

    return msg

def get_duty_keyboard(duty_item, chat_type='private', user_id=None):
    if not duty_item or duty_item["status"] == "completed":
        return None

    duty_date = duty_item["date"]
    keyboard = {
        "inline_keyboard": [
            [
                {
                    "text": bot_locales.t(chat_type, user_id, "duty_btn_done"),
                    "callback_data": f"done:{duty_date}:7"
                }
            ]
        ]
    }
    return keyboard

def get_admin_keyboard(chat_type='private', user_id=None):
    keyboard = {
        "inline_keyboard": [
            [
                {"text": bot_locales.t(chat_type, user_id, "btn_stats"), "callback_data": "adm:stats_view"},
                {"text": bot_locales.t(chat_type, user_id, "btn_residents"), "callback_data": "adm:list_view"}
            ],
            [
                {"text": bot_locales.t(chat_type, user_id, "btn_change_duty"), "callback_data": "adm:duty_rooms"},
                {"text": bot_locales.t(chat_type, user_id, "btn_logs"), "callback_data": "adm:logs_view"}
            ],
            [
                {"text": bot_locales.t(chat_type, user_id, "btn_admins"), "callback_data": "adm:admins_view"},
                {"text": bot_locales.t(chat_type, user_id, "btn_language"), "callback_data": "adm:lang_select"}
            ],
            [
                {"text": bot_locales.t(chat_type, user_id, "btn_applications"), "callback_data": "adm:applications"}
            ],
            [
                {"text": bot_locales.t(chat_type, user_id, "btn_refresh"), "callback_data": "adm:menu"}
            ]
        ]
    }
    return keyboard

def get_back_to_menu_keyboard(chat_type='private', user_id=None):
    return {
        "inline_keyboard": [
            [
                {"text": bot_locales.t(chat_type, user_id, "btn_back"), "callback_data": "adm:menu"}
            ]
        ]
    }

def get_language_keyboard():
    return {
        "inline_keyboard": [
            [
                {"text": "🇷🇺 Русский", "callback_data": "lang:ru"},
                {"text": "🇬🇧 English", "callback_data": "lang:en"},
                {"text": "🇺🇿 O'zbekcha", "callback_data": "lang:uz"}
            ]
        ]
    }

def send_today_duty_notification(chat_id, chat_type='private', user_id=None):
    today_duty = db.get_today_duty()
    item = today_duty.get(7)

    if not item:
        send_message(chat_id, bot_locales.t(chat_type, user_id, "duty_no_schedule_today"))
        return

    text = format_duty_message(item, chat_type=chat_type, user_id=user_id)
    keyboard = get_duty_keyboard(item, chat_type=chat_type, user_id=user_id)
    send_message(chat_id, text, reply_markup=keyboard)

def render_admin_menu_text(chat_type='private', user_id=None):
    return bot_locales.t(chat_type, user_id, 'admin_menu')


# ─────────────── APPLICATION STATE MACHINE ───────────────
# {user_id: {'step': 1..4, 'date': str, 'name': str, 'login': str, 'comments': str}}
_apply_states = {}
# {admin_id: {'app_id': int, 'action': 'approve'|'reject'}}
_pending_decision = {}


def notify_admins_new_application(app_id, full_name, login, move_in_date, comments, telegram_user):
    """Send new application notification to all admins."""
    admin_ids = config.get("admin_ids", [MAIN_OWNER_ID])
    tg_info = f"@{telegram_user['username']}" if telegram_user.get('username') else f"ID:{telegram_user.get('id', '?')}"
    created = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    comment_text = comments if comments else "-"

    approve_btn = bot_locales.t('private', None, 'app_approve_btn')
    reject_btn  = bot_locales.t('private', None, 'app_reject_btn')

    keyboard = {
        "inline_keyboard": [[
            {"text": approve_btn, "callback_data": f"app:approve:{app_id}"},
            {"text": reject_btn,  "callback_data": f"app:reject:{app_id}"}
        ]]
    }

    for admin_id in admin_ids:
        text = bot_locales.t('private', admin_id, 'admin_new_app',
            app_id=app_id, name=full_name, login=login,
            date=move_in_date, comment=comment_text, tg=tg_info, created=created)
        send_message(admin_id, text, reply_markup=keyboard)


def handle_apply_text(message):
    """Handle text messages when user is in the /apply flow."""
    chat_type = message.get("chat", {}).get("type", "private")
    chat_id = message["chat"]["id"]
    user_id = message.get("from", {}).get("id")
    text = message.get("text", "").strip()

    state = _apply_states.get(user_id)
    if not state:
        return False  # not in apply flow

    step = state.get('step', 1)

    if text == bot_locales.t(chat_type, user_id, 'apply_cancel_btn'):
        _apply_states.pop(user_id, None)
        send_message(chat_id, bot_locales.t(chat_type, user_id, 'apply_cancelled'),
                     reply_markup={"remove_keyboard": True})
        return True

    if step == 1:
        # Validate date DD.MM.YYYY
        import re
        if not re.match(r'^\d{2}\.\d{2}\.\d{4}$', text):
            send_message(chat_id, bot_locales.t(chat_type, user_id, 'apply_invalid_date'))
            return True
        state['date'] = text
        state['step'] = 2
        send_message(chat_id, bot_locales.t(chat_type, user_id, 'apply_step2'))

    elif step == 2:
        state['name'] = text
        state['step'] = 3
        send_message(chat_id, bot_locales.t(chat_type, user_id, 'apply_step3'))

    elif step == 3:
        state['login'] = text
        state['step'] = 4
        skip_btn = bot_locales.t(chat_type, user_id, 'apply_skip_btn')
        cancel_btn = bot_locales.t(chat_type, user_id, 'apply_cancel_btn')
        send_message(chat_id, bot_locales.t(chat_type, user_id, 'apply_step4'),
                     reply_markup={"keyboard": [[{"text": skip_btn}], [{"text": cancel_btn}]],
                                   "resize_keyboard": True, "one_time_keyboard": True})

    elif step == 4:
        skip_text = bot_locales.t(chat_type, user_id, 'apply_skip_btn')
        state['comments'] = '' if text == skip_text else text
        state['step'] = 5
        # Show confirmation
        comment_display = state['comments'] if state['comments'] else '-'
        confirm_text = bot_locales.t(chat_type, user_id, 'apply_confirm',
            date=state['date'], name=state['name'],
            login=state['login'], comment=comment_display)
        confirm_btn = bot_locales.t(chat_type, user_id, 'apply_confirm_btn')
        edit_btn = bot_locales.t(chat_type, user_id, 'apply_edit_btn')
        cancel_btn = bot_locales.t(chat_type, user_id, 'apply_cancel_btn')
        send_message(chat_id, confirm_text,
                     reply_markup={"keyboard": [[{"text": confirm_btn}],
                                                [{"text": edit_btn}],
                                                [{"text": cancel_btn}]],
                                   "resize_keyboard": True, "one_time_keyboard": True})

    elif step == 5:
        confirm_btn = bot_locales.t(chat_type, user_id, 'apply_confirm_btn')
        edit_btn = bot_locales.t(chat_type, user_id, 'apply_edit_btn')
        if text == edit_btn:
            # Reset to step 1
            state['step'] = 1
            send_message(chat_id, bot_locales.t(chat_type, user_id, 'apply_step1'),
                         reply_markup={"remove_keyboard": True})
        elif text == confirm_btn:
            # Save to DB
            user_from = message.get('from', {})
            tg_username = user_from.get('username', '')
            lang = bot_locales.get_user_lang(chat_type, user_id)
            app_id = db.add_application(
                telegram_id=user_id,
                telegram_username=tg_username,
                full_name=state['name'],
                school21_login=state['login'],
                move_in_date=state['date'],
                comments=state.get('comments', ''),
                lang=lang
            )
            _apply_states.pop(user_id, None)
            # Send success
            send_message(chat_id,
                bot_locales.t(chat_type, user_id, 'apply_success', app_id=app_id),
                reply_markup={"remove_keyboard": True})
            # Notify admins
            notify_admins_new_application(
                app_id, state['name'], state['login'],
                state['date'], state.get('comments', ''), user_from)

    return True
def handle_command(message):
    chat_type = message.get("chat", {}).get("type", "private")
    chat_id = message["chat"]["id"]
    user_id = message.get("from", {}).get("id")
    text = message.get("text", "").strip()

    if text.startswith("/start") or text == "/help":
        config["chat_id"] = chat_id
        save_config(config)
        # Cancel any pending apply flow
        _apply_states.pop(user_id, None)

        admin_text = bot_locales.t(chat_type, user_id, "admin_privilege") if is_admin(user_id) else ""
        welcome_msg = bot_locales.t(chat_type, user_id, "welcome", admin_text=admin_text)

        reply_markup = get_language_keyboard() if chat_type == 'private' else None
        send_message(chat_id, welcome_msg, reply_markup=reply_markup)

        # If user came via deep link /start apply, show application conditions immediately
        if "apply" in text.lower():
            if chat_type == 'private':
                _apply_states[user_id] = {'step': 1}
                cancel_btn = bot_locales.t(chat_type, user_id, 'apply_cancel_btn')
                apply_btn  = bot_locales.t(chat_type, user_id, 'apply_conditions_btn')
                keyboard = {"inline_keyboard": [[
                    {"text": apply_btn, "callback_data": "apply:start"},
                    {"text": cancel_btn, "callback_data": "apply:cancel"}
                ]]}
                send_message(chat_id, bot_locales.t(chat_type, user_id, 'apply_conditions'), reply_markup=keyboard)
                _apply_states.pop(user_id, None)

    elif text in ["/language", "/lang", "/til"]:
        if chat_type != 'private':
            send_message(chat_id, "\u2139️ В групповых чатах язык всегда русский.")
            return
        send_message(chat_id, bot_locales.t(chat_type, user_id, "select_language"), reply_markup=get_language_keyboard())

    elif text in ["/duty", "/today", "/dezhurstvo"]:
        send_today_duty_notification(chat_id, chat_type=chat_type, user_id=user_id)

    elif text == "/setgroup":
        config["chat_id"] = chat_id
        save_config(config)
        send_message(chat_id, bot_locales.t(chat_type, user_id, "group_linked"))

    elif text in ["/apply", "/ariza", "/zayvka"]:
        if chat_type != 'private':
            send_message(chat_id, "ℹ️ Подать заявку можно только в личных сообщениях с ботом.")
            return
        _apply_states[user_id] = {'step': 1}
        cancel_btn = bot_locales.t(chat_type, user_id, 'apply_cancel_btn')
        apply_btn  = bot_locales.t(chat_type, user_id, 'apply_conditions_btn')
        keyboard = {"inline_keyboard": [[
            {"text": apply_btn, "callback_data": "apply:start"},
            {"text": cancel_btn, "callback_data": "apply:cancel"}
        ]]}
        send_message(chat_id, bot_locales.t(chat_type, user_id, 'apply_conditions'), reply_markup=keyboard)
        _apply_states.pop(user_id, None)  # wait for inline btn

    elif text in ["/applications"]:
        if not is_admin(user_id):
            send_message(chat_id, bot_locales.t(chat_type, user_id, "no_admin_perm"))
            return
        apps = db.get_all_applications(status='pending')
        if not apps:
            send_message(chat_id, bot_locales.t(chat_type, user_id, 'app_no_pending'))
            return
        text_out = bot_locales.t(chat_type, user_id, 'applications_title')
        for app in apps:
            text_out += bot_locales.t(chat_type, user_id, 'app_list_item',
                id=app['id'], name=app['full_name'],
                login=app['school21_login'], status=app['status'])
        send_message(chat_id, text_out)

    # Check if user is in apply text flow (but text doesn't start with / or is inline step)
    elif not text.startswith('/'):
        # Check admin decision comment flow
        if user_id in _pending_decision:
            pending = _pending_decision.pop(user_id)
            app_id = pending['app_id']
            action = pending['action']
            admin_comment = text if text != '-' else ''
            _finalize_application_decision(chat_id, msg_id=None, user_id=user_id,
                                           chat_type=chat_type, app_id=app_id,
                                           action=action, admin_comment=admin_comment)
            return
        # Apply flow text
        handle_apply_text(message)
        return

    # --- ADMIN COMMANDS ---
    elif text in ["/admin", "/menu"]:
        if not is_admin(user_id):
            send_message(chat_id, bot_locales.t(chat_type, user_id, "no_admin_perm"))
            return

        send_message(chat_id, render_admin_menu_text(chat_type, user_id), reply_markup=get_admin_keyboard(chat_type, user_id))


    elif text == "/stats":
        if not is_admin(user_id):
            send_message(chat_id, bot_locales.t(chat_type, user_id, "no_admin_perm"))
            return

        stats = db.get_stats()
        msg = (
            bot_locales.t(chat_type, user_id, 'stats_title')
            + bot_locales.t(chat_type, user_id, 'stats_total', total=stats['total_residents'])
            + bot_locales.t(chat_type, user_id, 'stats_floor2', count=stats['floor2_count'])
            + bot_locales.t(chat_type, user_id, 'stats_floor7', count=stats['floor7_count'])
            + bot_locales.t(chat_type, user_id, 'stats_temp', count=stats['temp_count'])
            + bot_locales.t(chat_type, user_id, 'stats_waiting', count=stats['waiting_count'])
            + bot_locales.t(chat_type, user_id, 'stats_free_beds', free=stats['free_beds'], total_cap=stats['total_capacity'])
            + bot_locales.t(chat_type, user_id, 'stats_footer')
        )
        send_message(chat_id, msg, reply_markup=get_back_to_menu_keyboard(chat_type, user_id))

    elif text == "/logs":
        if not is_admin(user_id):
            send_message(chat_id, bot_locales.t(chat_type, user_id, "no_admin_perm"))
            return

        logs = db.get_activity_logs(10)
        log_lines = "\n".join([f"• <i>{l['timestamp']}</i> — <b>{l['action']}</b>: {l['details']}" for l in logs])
        send_message(chat_id, bot_locales.t(chat_type, user_id, 'logs_title') + log_lines, reply_markup=get_back_to_menu_keyboard(chat_type, user_id))

    elif text == "/list":
        if not is_admin(user_id):
            send_message(chat_id, bot_locales.t(chat_type, user_id, "no_admin_perm"))
            return

        floors_data = db.get_floors_data()
        msg = bot_locales.t(chat_type, user_id, 'residents_title')
        
        for fl_num in [2, 7]:
            rooms = floors_data["floors"].get(fl_num, [])
            msg += bot_locales.t(chat_type, user_id, 'residents_floor', floor=fl_num)
            for rm in rooms:
                if rm["residents"]:
                    names = ", ".join([f"{r['full_name']} (ID:#{r['id']})" for r in rm["residents"]])
                    msg += bot_locales.t(chat_type, user_id, 'residents_room', room=rm['room_number'], names=names)
            msg += "\n"

        send_message(chat_id, msg, reply_markup=get_back_to_menu_keyboard(chat_type, user_id))

    elif text.startswith("/addadmin"):
        if not is_admin(user_id):
            send_message(chat_id, bot_locales.t(chat_type, user_id, "no_admin_perm"))
            return

        try:
            new_id = int(text.split()[1].strip())
            admin_ids = config.get("admin_ids", [MAIN_OWNER_ID])
            if new_id not in admin_ids:
                admin_ids.append(new_id)
                config["admin_ids"] = admin_ids
                save_config(config)
                send_message(chat_id, bot_locales.t(chat_type, user_id, 'addadmin_success', uid=new_id))
            else:
                send_message(chat_id, bot_locales.t(chat_type, user_id, 'addadmin_already', uid=new_id))
        except Exception:
            send_message(chat_id, bot_locales.t(chat_type, user_id, 'addadmin_error'))

    elif text.startswith("/deladmin"):
        if not is_admin(user_id):
            send_message(chat_id, bot_locales.t(chat_type, user_id, "no_admin_perm"))
            return

        try:
            target_id = int(text.split()[1].strip())
            if target_id == MAIN_OWNER_ID:
                send_message(chat_id, bot_locales.t(chat_type, user_id, 'deladmin_owner'))
                return

            admin_ids = config.get("admin_ids", [MAIN_OWNER_ID])
            if target_id in admin_ids:
                admin_ids.remove(target_id)
                config["admin_ids"] = admin_ids
                save_config(config)
                send_message(chat_id, bot_locales.t(chat_type, user_id, 'deladmin_success', uid=target_id))
            else:
                send_message(chat_id, bot_locales.t(chat_type, user_id, 'deladmin_not_found', uid=target_id))
        except Exception:
            send_message(chat_id, bot_locales.t(chat_type, user_id, 'deladmin_error'))

    elif text.startswith("/add "):
        if not is_admin(user_id):
            send_message(chat_id, bot_locales.t(chat_type, user_id, "no_admin_perm"))
            return

        try:
            parts = text[4:].strip().split("|")
            full_name = parts[0].strip()
            nickname = parts[1].strip() if len(parts) > 1 else ""
            gender = parts[2].strip().upper() if len(parts) > 2 else "M"
            room_num = parts[3].strip() if len(parts) > 3 else None

            res_id = db.add_resident(full_name, nickname, "", gender, room_num, "permanent")
            excel_sync.export_db_to_excel(db.DB_PATH, EXCEL_PATH)
            room_display = room_num or bot_locales.t(chat_type, user_id, 'add_waiting')
            send_message(chat_id, bot_locales.t(chat_type, user_id, 'add_success', res_id=res_id, name=full_name, room=room_display))
        except Exception:
            send_message(chat_id, bot_locales.t(chat_type, user_id, 'add_error'))

    elif text.startswith("/evict"):
        if not is_admin(user_id):
            send_message(chat_id, bot_locales.t(chat_type, user_id, "no_admin_perm"))
            return

        try:
            val = text[6:].strip()
            res_id = int(val)
            db.evict_resident(res_id)
            excel_sync.export_db_to_excel(db.DB_PATH, EXCEL_PATH)
            send_message(chat_id, bot_locales.t(chat_type, user_id, 'evict_success', res_id=res_id))
        except Exception:
            send_message(chat_id, bot_locales.t(chat_type, user_id, 'evict_error'))

    elif text.startswith("/move"):
        if not is_admin(user_id):
            send_message(chat_id, bot_locales.t(chat_type, user_id, "no_admin_perm"))
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
                send_message(chat_id, bot_locales.t(chat_type, user_id, 'move_success', name=res['full_name'], room=new_room))
            else:
                send_message(chat_id, bot_locales.t(chat_type, user_id, 'move_not_found'))
        except Exception:
            send_message(chat_id, bot_locales.t(chat_type, user_id, 'move_error'))

    elif text.startswith("/setduty"):
        if not is_admin(user_id):
            send_message(chat_id, bot_locales.t(chat_type, user_id, "no_admin_perm"))
            return

        try:
            parts = text[8:].strip().split()
            duty_date = parts[0]
            room_num = parts[1]

            db.set_manual_duty(duty_date, 7, room_num, "pending", "Назначено через Telegram")
            excel_sync.export_db_to_excel(db.DB_PATH, EXCEL_PATH)
            send_message(chat_id, bot_locales.t(chat_type, user_id, 'setduty_success', date=duty_date, room=room_num))
        except Exception:
            send_message(chat_id, bot_locales.t(chat_type, user_id, 'setduty_error'))


def _finalize_application_decision(chat_id, msg_id, user_id, chat_type, app_id, action, admin_comment):
    """Finalize approve or reject and notify applicant."""
    app = db.get_application_by_id(app_id)
    if not app:
        send_message(chat_id, "⚠️ Заявка не найдена.")
        return

    if app['status'] != 'pending':
        send_message(chat_id, bot_locales.t(chat_type, user_id, 'app_already_decided', status=app['status']))
        return

    comment_display = admin_comment if admin_comment else ('-' if action == 'reject' else 'Одобрено администрацией')

    db.update_application_status(app_id, action, admin_comment)

    # Edit admin message to show result
    done_label = bot_locales.t(chat_type, user_id,
        'app_done_label_approve' if action == 'approved' else 'app_done_label_reject')
    if msg_id:
        edit_message(chat_id, msg_id,
            f"✅ <b>Заявка #{app_id} — {done_label}</b>\n💬 Комментарий: <i>{comment_display}</i>",
            reply_markup=None)
    else:
        send_message(chat_id,
            f"✅ <b>Заявка #{app_id} — {done_label}</b>\n💬 Комментарий: <i>{comment_display}</i>")

    applicant_tg_id = app.get('telegram_id')
    if applicant_tg_id:
        if action == 'approved':
            # Auto-add to waiting list
            existing_login = app.get('school21_login', '')
            gender = app.get('gender') or 'M'
            res_id = db.add_resident(
                full_name=app['full_name'],
                nickname=existing_login,
                profile_url='',
                gender=gender,
                room_number=None,
                status='waiting'
            )
            send_message(chat_id, bot_locales.t(chat_type, user_id, 'app_added_to_waiting', name=app['full_name']))
            # Notify applicant
            notify_text = bot_locales.t('private', applicant_tg_id, 'app_approved_notify', comment=comment_display)
            send_message(applicant_tg_id, notify_text)

            # Send Rules PDF Document to the applicant upon approval
            if os.path.exists(RULES_PDF_PATH):
                rules_caption = bot_locales.t('private', applicant_tg_id, 'app_rules_sent')
                send_document(applicant_tg_id, RULES_PDF_PATH, caption=rules_caption)
        else:
            notify_text = bot_locales.t('private', applicant_tg_id, 'app_rejected_notify', comment=comment_display)
            send_message(applicant_tg_id, notify_text)

def handle_callback_query(cb):
    cb_id = cb["id"]
    chat_type = cb.get("message", {}).get("chat", {}).get("type", "private")
    chat_id = cb["message"]["chat"]["id"]
    msg_id = cb["message"]["message_id"]
    user_id = cb.get("from", {}).get("id")
    data = cb.get("data", "")

    # ─── Apply flow inline buttons ───
    if data == "apply:start":
        answer_callback_query(cb_id)
        _apply_states[user_id] = {'step': 1}
        cancel_btn = bot_locales.t(chat_type, user_id, 'apply_cancel_btn')
        send_message(chat_id, bot_locales.t(chat_type, user_id, 'apply_step1'),
                     reply_markup={"keyboard": [[{"text": cancel_btn}]],
                                   "resize_keyboard": True, "one_time_keyboard": False})
        return

    elif data == "apply:cancel":
        answer_callback_query(cb_id)
        _apply_states.pop(user_id, None)
        send_message(chat_id, bot_locales.t(chat_type, user_id, 'apply_cancelled'),
                     reply_markup={"remove_keyboard": True})
        return

    # ─── Admin: approve/reject application ───
    elif data.startswith("app:approve:") or data.startswith("app:reject:"):
        if not is_admin(user_id):
            answer_callback_query(cb_id, bot_locales.t(chat_type, user_id, 'no_access'), show_alert=True)
            return
        answer_callback_query(cb_id)
        parts = data.split(":")
        action_key = parts[1]  # 'approve' or 'reject'
        app_id = int(parts[2])

        app = db.get_application_by_id(app_id)
        if not app:
            send_message(chat_id, "⚠️ Заявка не найдена.")
            return
        if app['status'] != 'pending':
            send_message(chat_id, bot_locales.t(chat_type, user_id, 'app_already_decided', status=app['status']))
            return

        # Ask for comment then finalize
        _pending_decision[user_id] = {'app_id': app_id, 'action': 'approved' if action_key == 'approve' else 'rejected', 'msg_id': msg_id}
        send_message(chat_id, bot_locales.t(chat_type, user_id, 'app_comment_prompt'))
        return

    if data.startswith("lang:"):
        new_lang = data.split(":")[1]
        if chat_type != 'private':
            answer_callback_query(cb_id, "ℹ️ В группах язык всегда русский.", show_alert=True)
            return
        db.set_user_language(user_id, new_lang)
        confirm_text = bot_locales.t(chat_type, user_id, "lang_changed")
        answer_callback_query(cb_id, confirm_text, show_alert=False)
        send_message(chat_id, confirm_text)

    elif data == "adm:lang_select":
        answer_callback_query(cb_id)
        if chat_type != 'private':
            send_message(chat_id, "ℹ️ В групповых чатах язык всегда русский.")
            return
        send_message(chat_id, bot_locales.t(chat_type, user_id, "select_language"), reply_markup=get_language_keyboard())

    elif data.startswith("done:"):
        parts = data.split(":")
        duty_date = parts[1]
        floor = int(parts[2])

        answer_callback_query(cb_id, bot_locales.t(chat_type, user_id, "duty_marked_done"), show_alert=False)

        db.mark_duty_status(duty_date, floor, "completed", notes="Отмечено в Telegram")
        excel_sync.export_db_to_excel(db.DB_PATH, EXCEL_PATH)

        user_name = cb.get("from", {}).get("first_name", "Студент")
        today_duty = db.get_today_duty()
        item = today_duty.get(7)

        updated_text = format_duty_message(item, chat_type=chat_type, user_id=user_id) + "\n\n" + bot_locales.t(chat_type, user_id, 'duty_done_updated', user_name=user_name)
        edit_message(chat_id, msg_id, updated_text, reply_markup=None)

    elif data == "adm:menu":
        if not is_admin(user_id):
            answer_callback_query(cb_id, bot_locales.t(chat_type, user_id, 'no_access'), show_alert=True)
            return
        answer_callback_query(cb_id)
        edit_message(chat_id, msg_id, render_admin_menu_text(chat_type, user_id), reply_markup=get_admin_keyboard(chat_type, user_id))


    elif data == "adm:stats_view":
        if not is_admin(user_id):
            answer_callback_query(cb_id, bot_locales.t(chat_type, user_id, 'no_access'), show_alert=True)
            return
        answer_callback_query(cb_id)

        stats = db.get_stats()
        text = (
            bot_locales.t(chat_type, user_id, 'stats_title')
            + bot_locales.t(chat_type, user_id, 'stats_total', total=stats['total_residents'])
            + bot_locales.t(chat_type, user_id, 'stats_floor2', count=stats['floor2_count'])
            + bot_locales.t(chat_type, user_id, 'stats_floor7', count=stats['floor7_count'])
            + bot_locales.t(chat_type, user_id, 'stats_temp', count=stats['temp_count'])
            + bot_locales.t(chat_type, user_id, 'stats_waiting', count=stats['waiting_count'])
            + bot_locales.t(chat_type, user_id, 'stats_free_beds', free=stats['free_beds'], total_cap=stats['total_capacity'])
            + bot_locales.t(chat_type, user_id, 'stats_footer')
        )
        edit_message(chat_id, msg_id, text, reply_markup=get_back_to_menu_keyboard(chat_type, user_id))

    elif data == "adm:list_view":
        if not is_admin(user_id):
            answer_callback_query(cb_id, bot_locales.t(chat_type, user_id, 'no_access'), show_alert=True)
            return
        answer_callback_query(cb_id)

        floors_data = db.get_floors_data()
        text = bot_locales.t(chat_type, user_id, 'residents_title')
        
        for fl_num in [2, 7]:
            rooms = floors_data["floors"].get(fl_num, [])
            text += bot_locales.t(chat_type, user_id, 'residents_floor', floor=fl_num)
            for rm in rooms:
                if rm["residents"]:
                    names = ", ".join([f"{r['full_name']} (ID:#{r['id']})" for r in rm["residents"]])
                    text += bot_locales.t(chat_type, user_id, 'residents_room', room=rm['room_number'], names=names)
            text += "\n"

        edit_message(chat_id, msg_id, text, reply_markup=get_back_to_menu_keyboard(chat_type, user_id))

    elif data == "adm:logs_view":
        if not is_admin(user_id):
            answer_callback_query(cb_id, bot_locales.t(chat_type, user_id, 'no_access'), show_alert=True)
            return
        answer_callback_query(cb_id)

        logs = db.get_activity_logs(10)
        log_lines = "\n".join([f"• <i>{l['timestamp']}</i> — <b>{l['action']}</b>: {l['details']}" for l in logs])
        text = bot_locales.t(chat_type, user_id, 'logs_title') + log_lines
        edit_message(chat_id, msg_id, text, reply_markup=get_back_to_menu_keyboard(chat_type, user_id))

    elif data == "adm:admins_view":
        if not is_admin(user_id):
            answer_callback_query(cb_id, bot_locales.t(chat_type, user_id, 'no_access'), show_alert=True)
            return
        answer_callback_query(cb_id)

        admin_ids = config.get("admin_ids", [MAIN_OWNER_ID])
        owner_label = bot_locales.t(chat_type, user_id, 'admins_owner_label')
        ids_str = "\n".join([f"  • <code>{aid}</code> {owner_label if aid == MAIN_OWNER_ID else ''}" for aid in admin_ids])

        text = (
            bot_locales.t(chat_type, user_id, 'admins_title')
            + ids_str + "\n\n"
            + bot_locales.t(chat_type, user_id, 'admins_add_hint') + "\n\n"
            + bot_locales.t(chat_type, user_id, 'admins_del_hint')
        )
        edit_message(chat_id, msg_id, text, reply_markup=get_back_to_menu_keyboard(chat_type, user_id))

    elif data == "adm:duty_rooms":
        if not is_admin(user_id):
            answer_callback_query(cb_id, bot_locales.t(chat_type, user_id, 'no_access'), show_alert=True)
            return
        answer_callback_query(cb_id)

        male_rooms = ["701", "702", "703", "704", "705", "706", "709", "711", "712", "714"]
        buttons = []
        row = []
        for r_num in male_rooms:
            row.append({"text": bot_locales.t(chat_type, user_id, 'duty_room_btn', room=r_num), "callback_data": f"adm:setduty_today:{r_num}"})
            if len(row) == 2:
                buttons.append(row)
                row = []
        if row:
            buttons.append(row)
        buttons.append([{"text": bot_locales.t(chat_type, user_id, 'btn_back_to_menu'), "callback_data": "adm:menu"}])

        text = bot_locales.t(chat_type, user_id, 'duty_rooms_title')
        edit_message(chat_id, msg_id, text, reply_markup={"inline_keyboard": buttons})

    elif data.startswith("adm:setduty_today:"):
        if not is_admin(user_id):
            answer_callback_query(cb_id, bot_locales.t(chat_type, user_id, 'no_access'), show_alert=True)
            return

        room_num = data.split(":")[2]
        today_str = datetime.date.today().strftime("%Y-%m-%d")

        db.set_manual_duty(today_str, 7, room_num, "pending", "Назначено кнопкой в Telegram")
        excel_sync.export_db_to_excel(db.DB_PATH, EXCEL_PATH)

        answer_callback_query(cb_id, bot_locales.t(chat_type, user_id, 'duty_assigned_alert', room=room_num, date=today_str), show_alert=True)
        edit_message(chat_id, msg_id, bot_locales.t(chat_type, user_id, 'duty_assigned_msg', room=room_num, date=today_str), reply_markup=get_back_to_menu_keyboard(chat_type, user_id))

    elif data == "adm:applications":
        if not is_admin(user_id):
            answer_callback_query(cb_id, bot_locales.t(chat_type, user_id, 'no_access'), show_alert=True)
            return
        answer_callback_query(cb_id)

        apps = db.get_all_applications(status='pending')
        if not apps:
            edit_message(chat_id, msg_id,
                bot_locales.t(chat_type, user_id, 'app_no_pending'),
                reply_markup=get_back_to_menu_keyboard(chat_type, user_id))
            return

        text_out = bot_locales.t(chat_type, user_id, 'applications_title')
        for app in apps:
            text_out += bot_locales.t(chat_type, user_id, 'app_list_item',
                id=app['id'], name=app['full_name'],
                login=app['school21_login'], status=app['status'])
        edit_message(chat_id, msg_id, text_out, reply_markup=get_back_to_menu_keyboard(chat_type, user_id))

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

_bot_running_lock = False

def run_bot(token=None):
    global BOT_TOKEN, _bot_running_lock
    if _bot_running_lock:
        print("[Telegram Bot] Warning: Bot instance is already running. Skipping duplicate start.")
        return
    _bot_running_lock = True

    if token:
        BOT_TOKEN = token

    if not BOT_TOKEN:
        print("[Telegram Bot] Error: TELEGRAM_BOT_TOKEN is empty!")
        return

    print(f"[Telegram Bot] Running for Admin IDs: {config.get('admin_ids', [MAIN_OWNER_ID])}...")

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
