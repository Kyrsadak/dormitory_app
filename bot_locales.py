import db

LOCALES = {
    'ru': {
        'lang_name': '🇷🇺 Русский',
        'welcome': (
            "👋 <b>Привет! Я официальный бот Общежития.</b>\n\n"
            "📌 <b>Доступные команды:</b>\n"
            "• /duty или /today — Кто сегодня дежурит и отметка о выполнении\n"
            "• /language — Сменить язык / Change language / Tilni o'zgartirish\n"
            "• /setgroup — Привязать этот чат для утренних напоминаний в 09:00\n"
            "{admin_text}\n\n"
            "<i>Все данные мгновенно синхронизируются с веб-сайтом!</i>"
        ),
        'admin_privilege': "\n\n👑 <b>Вам доступна Панель Администратора!</b> Отправьте /admin для входа.",
        'select_language': "🌐 <b>Выберите язык интерфейса / Select language / Tilni tanlang:</b>",
        'lang_changed': "✅ <b>Язык успешно изменен на Русский!</b>",
        'duty_title': "🧹 <b>ГРАФИК ДЕЖУРСТВА ПО КУХНЕ (7 ЭТАЖ)</b>",
        'duty_date': "📅 <b>Дата:</b> {date_str}",
        'duty_status': "📍 <b>Статус:</b> {status_icon}",
        'duty_today_room': "🔷 <b>СЕГОДНЯ ДЕЖУРИТ КОМНАТА {room_num}:</b>",
        'duty_no_residents': "  • <i>В комнате никто не живет</i>",
        'duty_task': "📌 <b>Обязанность:</b> Навести порядок на кухне 7 этажа и вынести мусор в бак.",
        'duty_status_completed': "✅ <b>ВЫПОЛНЕНО</b>",
        'duty_status_pending': "⏳ <b>ОЖИДАЕТ ВЫПОЛНЕНИЯ</b>",
        'duty_btn_done': "✅ Мы выполнили дежурство!",
        'duty_not_found': "⚠️ Данные о дежурстве не найдены.",
        'duty_no_schedule_today': "⚠️ На сегодня нет назначенных дежурных комнат.",
        'group_linked': "✅ <b>Группа успешно привязана!</b> Каждый день в 09:00 сюда будет приходить график дежурств.",
        'no_admin_perm': "⛔ У вас нет доступа к административной панели общежития.",
        'duty_marked_done': "✅ Дежурство отмечено выполненным!",
        'btn_stats': "📊 Статистика",
        'btn_residents': "👥 Список жильцов",
        'btn_change_duty': "🧹 Сменить дежурного",
        'btn_logs': "📑 Журнал аудита",
        'btn_admins': "🔑 Список Админов",
        'btn_refresh': "🔄 Обновить панель",
        'btn_back': "⬅️ Вернуться в Главное Меню",
        'btn_language': "🌐 Сменить язык",
    },
    'en': {
        'lang_name': '🇬🇧 English',
        'welcome': (
            "👋 <b>Hello! I am the official Dormitory Bot.</b>\n\n"
            "📌 <b>Available commands:</b>\n"
            "• /duty or /today — Today's duty schedule & completion check\n"
            "• /language — Change language / Сменить язык / Tilni o'zgartirish\n"
            "• /setgroup — Link this group chat for 09:00 morning notifications\n"
            "{admin_text}\n\n"
            "<i>All data is instantly synced with the website!</i>"
        ),
        'admin_privilege': "\n\n👑 <b>Admin Panel is available to you!</b> Send /admin to enter.",
        'select_language': "🌐 <b>Select language / Выберите язык / Tilni tanlang:</b>",
        'lang_changed': "✅ <b>Language successfully changed to English!</b>",
        'duty_title': "🧹 <b>KITCHEN DUTY SCHEDULE (7TH FLOOR)</b>",
        'duty_date': "📅 <b>Date:</b> {date_str}",
        'duty_status': "📍 <b>Status:</b> {status_icon}",
        'duty_today_room': "🔷 <b>ROOM {room_num} IS ON DUTY TODAY:</b>",
        'duty_no_residents': "  • <i>Room is empty</i>",
        'duty_task': "📌 <b>Duty:</b> Clean the 7th-floor kitchen and take out trash to the bin.",
        'duty_status_completed': "✅ <b>COMPLETED</b>",
        'duty_status_pending': "⏳ <b>PENDING</b>",
        'duty_btn_done': "✅ We completed our duty!",
        'duty_not_found': "⚠️ Duty data not found.",
        'duty_no_schedule_today': "⚠️ No room assigned for duty today.",
        'group_linked': "✅ <b>Group successfully linked!</b> Daily duty schedule will be posted here at 09:00 AM.",
        'no_admin_perm': "⛔ You do not have admin permissions for the dormitory.",
        'duty_marked_done': "✅ Duty marked as completed!",
        'btn_stats': "📊 Statistics",
        'btn_residents': "👥 Resident List",
        'btn_change_duty': "🧹 Change Duty Room",
        'btn_logs': "📑 Audit Logs",
        'btn_admins': "🔑 Admin List",
        'btn_refresh': "🔄 Refresh Panel",
        'btn_back': "⬅️ Back to Main Menu",
        'btn_language': "🌐 Change Language",
    },
    'uz': {
        'lang_name': "🇺🇿 O'zbekcha",
        'welcome': (
            "👋 <b>Salom! Men Yotoqxona rasmiy botiman.</b>\n\n"
            "📌 <b>Mavjud buyruqlar:</b>\n"
            "• /duty yoki /today — Bugungi navbatchilik va bajarilganlik belgisi\n"
            "• /language — Tilni o'zgartirish / Сменить язык / Change language\n"
            "• /setgroup — Ertalabki 09:00 bildirishnomalari uchun guruhni ulash\n"
            "{admin_text}\n\n"
            "<i>Barcha ma'lumotlar veb-sayt bilan zumda sinxronlanadi!</i>"
        ),
        'admin_privilege': "\n\n👑 <b>Siz uchun Admin Paneli mavjud!</b> Kirish uchun /admin yuboring.",
        'select_language': "🌐 <b>Tilni tanlang / Select language / Выберите язык:</b>",
        'lang_changed': "✅ <b>Til muvaffaqiyatli O'zbek tiliga o'zgartirildi!</b>",
        'duty_title': "🧹 <b>OSHXONA NAVBATCHILIK JADVALI (7-QAVAT)</b>",
        'duty_date': "📅 <b>Sana:</b> {date_str}",
        'duty_status': "📍 <b>Holat:</b> {status_icon}",
        'duty_today_room': "🔷 <b>BUGUN {room_num}-XONA NAVBATCHI:</b>",
        'duty_no_residents': "  • <i>Xonada hech kim yashamaydi</i>",
        'duty_task': "📌 <b>Vazifa:</b> 7-qavat oshxonasini tozalash va axlatni axlat qutisiga tashlash.",
        'duty_status_completed': "✅ <b>BAJARILDI</b>",
        'duty_status_pending': "⏳ <b>BAJARILISHI KUTILMOQDA</b>",
        'duty_btn_done': "✅ Biz navbatchilikni bajardik!",
        'duty_not_found': "⚠️ Navbatchilik ma'lumotlari topilmadi.",
        'duty_no_schedule_today': "⚠️ Bugunga tayinlangan navbatchi xona yo'q.",
        'group_linked': "✅ <b>Guruh muvaffaqiyatli ulandi!</b> Har kuni soat 09:00 da bu yerga navbatchilik jadvali yuboriladi.",
        'no_admin_perm': "⛔ Sizda yotoqxona admin paneliga kirish huquqi yo'q.",
        'duty_marked_done': "✅ Navbatchilik bajarildi deb belgilandi!",
        'btn_stats': "📊 Statistika",
        'btn_residents': "👥 Yashovchilar ro'yxati",
        'btn_change_duty': "🧹 Navbatchini almashtirish",
        'btn_logs': "📑 Audit jurnali",
        'btn_admins': "🔑 Adminlar ro'yxati",
        'btn_refresh': "🔄 Panelni yangilash",
        'btn_back': "⬅️ Asosiy menyuga qaytish",
        'btn_language': "🌐 Tilni o'zgartirish",
    }
}

def get_user_lang(chat_type, telegram_id):
    """
    Groups and supergroups are STRICTLY Russian ('ru').
    Private chats use stored preference (default 'ru').
    """
    if chat_type in ('group', 'supergroup'):
        return 'ru'
    return db.get_user_language(telegram_id)

def t(chat_type, telegram_id, key, **kwargs):
    lang = get_user_lang(chat_type, telegram_id)
    lang_dict = LOCALES.get(lang, LOCALES['ru'])
    template = lang_dict.get(key) or LOCALES['ru'].get(key, '')
    if kwargs:
        try:
            return template.format(**kwargs)
        except Exception:
            return template
    return template
