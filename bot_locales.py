import db

LOCALES = {
    # ─────────────── RUSSIAN ───────────────
    'ru': {
        'lang_name': '🇷🇺 Русский',

        # /start, /help
        'welcome': (
            "🏢 <b>Добро пожаловать в официальный бот Общежития School 21!</b>\n\n"
            "📍 Ул. Каландар, 24 (10 мин. от кампуса)\n\n"
            "📌 <b>Что делает этот бот:</b>\n"
            "• 🧹 Отображает график дежурств по кухне (7 этаж)\n"
            "• 📊 Показывает актуальную статистику проживающих\n"
            "• 📝 Принимает заявки на проживание в общежитии (2026)\n\n"
            "📌 <b>Основные команды:</b>\n"
            "• /apply — 📝 Подать заявку на проживание в общежитии\n"
            "• /duty — Кто сегодня дежурит (7 этаж)\n"
            "• /language — Сменить язык интерфейса\n"
            "• /setgroup — Привязать групповой чат для уведомлений\n"
            "{admin_text}\n\n"
            "🌐 Веб-сайт: school21dorm.onrender.com\n"
            "<i>Все данные мгновенно синхронизируются с веб-сайтом!</i>"
        ),
        'welcome_apply': (
            "📝 <b>Заявка на проживание — School 21 2026</b>\n\n"
            "Отправьте /apply чтобы начать заполнение заявки."
        ),
        'app_rules_sent': "📎 Выше прикреплены <b>Правила проживания в общежитии</b>. Пожалуйста, ознакомьтесь!",
        'admin_privilege': "\n\n👑 <b>Вам доступна Панель Администратора!</b> Отправьте /admin для входа.",

        # language
        'select_language': "🌐 <b>Выберите язык интерфейса / Select language / Tilni tanlang:</b>",
        'lang_changed': "✅ <b>Язык успешно изменен на Русский!</b>",
        'groups_lang_fixed': "ℹ️ В групповых чатах язык всегда Русский.",

        # duty messages
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
        'duty_marked_done': "✅ Дежурство отмечено выполненным!",
        'duty_done_updated': "🎉 <b>ОТМЕЧЕНО ВЫПОЛНЕННЫМ:</b> {user_name} в Telegram!\n<i>Статус мгновенно синхронизирован с веб-сайтом!</i>",

        # group linking
        'group_linked': "✅ <b>Группа успешно привязана!</b> Каждый день в 09:00 сюда будет приходить график дежурств.",

        # access denied
        'no_admin_perm': "⛔ У вас нет доступа к административной панели общежития.",
        'no_access': "⛔ Нет доступа",

        # admin panel buttons
        'btn_stats': "📊 Статистика",
        'btn_residents': "👥 Список жильцов",
        'btn_change_duty': "🧹 Сменить дежурного",
        'btn_logs': "📑 Журнал аудита",
        'btn_admins': "🔑 Список Админов",
        'btn_refresh': "🔄 Обновить панель",
        'btn_back': "⬅️ Вернуться в Главное Меню",
        'btn_language': "🌐 Сменить язык",
        'btn_back_to_menu': "⬅️ Назад в Меню",

        # admin panel main text
        'admin_menu': (
            "👑 <b>ПАНЕЛЬ АДМИНИСТРАТОРА ОБЩЕЖИТИЯ</b>\n\n"
            "Вы вошли как Администратор приложения.\n"
            "Выберите интересующий раздел с помощью инлайн-кнопок ниже:\n\n"
            "📌 <b>Доступные быстрые команды:</b>\n"
            "• <code>/add ФИО | Ник | M/F | Комната</code> — Заселить жильца\n"
            "• <code>/evict ID</code> — Выселить жильца\n"
            "• <code>/move ID НоваяКомната</code> — Переселить жильца\n"
            "• <code>/setduty YYYY-MM-DD Комната</code> — Сменить дежурного\n"
            "• <code>/addadmin TelegramID</code> — Добавить нового админа\n"
            "• <code>/deladmin TelegramID</code> — Удалить админа"
        ),

        # stats
        'stats_title': "📊 <b>АКТУАЛЬНАЯ СТАТИСТИКА ОБЩЕЖИТИЯ (PROD)</b>\n\n",
        'stats_total': "👥 Всего жильцов: <b>{total}</b> чел.\n",
        'stats_floor2': "🌸 2 Этаж (Женский): <b>{count}</b> чел.\n",
        'stats_floor7': "🔷 7 Этаж (Мужской): <b>{count}</b> чел.\n",
        'stats_temp': "⏳ Временные (14 дней): <b>{count}</b> чел.\n",
        'stats_waiting': "🛑 В очереди / Без комнаты: <b>{count}</b> чел.\n",
        'stats_free_beds': "🛏️ Свободных койко-мест: <b>{free}</b> из {total_cap}",
        'stats_footer': "\n\n<i>Данные мгновенно синхронизированы с SQLite и сайтом!</i>",

        # residents list
        'residents_title': "👥 <b>СПИСОК ПРОЖИВАЮЩИХ ПО КОМНАТАМ:</b>\n\n",
        'residents_floor': "<b>{floor} ЭТАЖ:</b>\n",
        'residents_room': "  • <b>Комн. {room}:</b> {names}\n",

        # logs
        'logs_title': "📑 <b>ЖУРНАЛ ПОСЛЕДНИХ ДЕЙСТВИЙ (АУДИТ):</b>\n\n",

        # admins list
        'admins_title': "🔑 <b>СПИСОК АДМИНИСТРАТОРОВ БОТА:</b>\n\n",
        'admins_owner_label': "(👑 Главный Владелец)",
        'admins_add_hint': "📌 <b>Чтобы добавить нового админа, отправьте:</b>\n<code>/addadmin TelegramID</code>",
        'admins_del_hint': "📌 <b>Чтобы удалить админа, отправьте:</b>\n<code>/deladmin TelegramID</code>",

        # duty assignment panel
        'duty_rooms_title': "🧹 <b>ВЫБЕРИТЕ КОМНАТУ ДЛЯ НАЗНАЧЕНИЯ ДЕЖУРНОЙ НА СЕГОДНЯ:</b>",
        'duty_room_btn': "📍 Комн. {room}",
        'duty_assigned_alert': "✅ Комната {room} назначена дежурной на сегодня ({date})!",
        'duty_assigned_msg': "✅ <b>Дежурная комната на сегодня ({date}) успешно изменена на Комнату {room}!</b>\n\nДанные мгновенно обновлены на сайте.",

        # /add command
        'add_success': "✅ <b>Жилец успешно заселен!</b>\nID: #{res_id}\nФИО: {name}\nКомната: {room}",
        'add_waiting': "В очереди",
        'add_error': "⚠️ <b>Формат команды:</b>\n<code>/add ФИО | Ник | M/F | НомерКомнаты</code>\n\n<i>Пример:</i>\n<code>/add Иванов Иван | ivanov_i | M | 705</code>",

        # /evict command
        'evict_success': "✅ <b>Жилец ID #{res_id} успешно выселен!</b> Данные обновлены на сайте и в Excel.",
        'evict_error': "⚠️ <b>Формат команды:</b>\n<code>/evict ID_жильца</code>\n\n<i>Пример:</i> <code>/evict 15</code>",

        # /move command
        'move_success': "✅ <b>Жилец {name} переселен в комнату {room}!</b>",
        'move_not_found': "⚠️ Жилец с таким ID не найден.",
        'move_error': "⚠️ <b>Формат команды:</b>\n<code>/move ID_жильца НоваяКомната</code>\n\n<i>Пример:</i> <code>/move 15 706</code>",

        # /setduty command
        'setduty_success': "✅ <b>Дежурство на {date} назначено на комнату {room}!</b> Данные обновлены на сайте.",
        'setduty_error': "⚠️ <b>Формат команды:</b>\n<code>/setduty ГГГГ-ММ-ДД НомерКомнаты</code>\n\n<i>Пример:</i> <code>/setduty 2026-08-10 706</code>",

        # /addadmin command
        'addadmin_success': "✅ <b>Пользователь Telegram ID <code>{uid}</code> успешно добавлен в список Администраторов бота!</b>",
        'addadmin_already': "ℹ️ Пользователь ID <code>{uid}</code> уже является администратором.",
        'addadmin_error': "⚠️ <b>Формат команды:</b>\n<code>/addadmin TelegramID</code>\n\n<i>Пример:</i> <code>/addadmin 123456789</code>",

        # /deladmin command
        'deladmin_success': "✅ <b>Пользователь Telegram ID <code>{uid}</code> удален из списка Администраторов.</b>",
        'deladmin_owner': "⚠️ Нельзя удалить главного владельца бота.",
        'deladmin_not_found': "ℹ️ Пользователь ID <code>{uid}</code> не найден в списке админов.",
        'deladmin_error': "⚠️ <b>Формат команды:</b>\n<code>/deladmin TelegramID</code>\n\n<i>Пример:</i> <code>/deladmin 123456789</code>",

        # ===== APPLICATION / ЗАЯВКА НА ПРОЖИВАНИЕ =====
        'btn_apply': "📝 Подать заявку на проживание",
        'btn_applications': "📋 Заявки на заселение",
        'apply_conditions': (
            "🏢 <b>ОБЩЕЖИТИЕ SCHOOL 21 — 2026</b>\n\n"
            "📍 Адрес: ул. Каландар, 24 (всего 10 минут от кампуса)\n\n"
            "Мы проводим предварительный опрос для желающих проживать в общежитии.\n\n"
            "❗ Для проживающих дедлайн по проектам сокращается на 20%\n"
            "❗ Для жителей Кибрая и Урта Чирчик места не предоставляются\n"
            "❗ Только участники старше 18 лет\n"
            "❗ Школа не дает временную регистрацию\n"
            "❗ Количество мест ограничено\n\n"
            "💸 <b>Цена:</b> 1 050 000 сум/мес. Оплата за 1 месяц вперёд (не возвращается)\n"
            "🏢 Комнаты на 4 или 6 человек\n"
            "📌 Только для пиров основного обучения.\n\n"
            "Чтобы подать заявку, нажмите кнопку ниже:"
        ),
        'apply_conditions_btn': "📝 Заполнить заявку",
        'apply_cancel_btn': "❌ Отмена",
        'apply_step1': "📅 Шаг 1/4. Укажите <b>желаемую дату заселения</b>:\n<i>Формат: ДД.ММ.ГГГГ (например: 01.09.2026)</i>",
        'apply_step2': "👤 Шаг 2/4. Введите <b>ФИО по документам</b>:",
        'apply_step3': "🏫 Шаг 3/4. Введите ваш <b>Login School 21</b>:",
        'apply_step4': "💬 Шаг 4/4. Дополнительный комментарий (\u043dеобязательно):\n<i>За вас дают согласие на обработку персональных данных.</i>",
        'apply_skip_btn': "➡️ Пропустить",
        'apply_confirm': (
            "✅ <b>Проверьте данные заявки:</b>\n\n"
            "📅 Дата заселения: <b>{date}</b>\n"
            "👤 ФИО: <b>{name}</b>\n"
            "🏫 Login: <b>{login}</b>\n"
            "💬 Комментарий: <i>{comment}</i>\n\n"
            "Все данные верны?"
        ),
        'apply_confirm_btn': "✅ Отправить заявку",
        'apply_edit_btn': "✏️ Изменить",
        'apply_success': (
            "✅ <b>Ваша заявка успешно отправлена!</b>\n\n"
            "📊 Номер заявки: <b>#{app_id}</b>\n"
            "⏳ Статус: <b>На рассмотрении</b>\n\n"
            "Мы уведомим вас о решении администрации."
        ),
        'apply_cancelled': "❌ Подача заявки отменена.",
        'apply_invalid_date': "⚠️ Неверный формат даты. Пожалуйста, введите в формате ДД.ММ.ГГГГ (01.09.2026):",

        # admin application management
        'admin_new_app': (
            "📥 <b>НОВАЯ ЗАЯВКА #{app_id}</b>\n\n"
            "👤 ФИО: <b>{name}</b>\n"
            "🏫 Login: <code>{login}</code>\n"
            "📅 Дата заселения: <b>{date}</b>\n"
            "💬 Комментарий: <i>{comment}</i>\n"
            "📱 Telegram: {tg}\n"
            "🕑 Подано: {created}"
        ),
        'app_approve_btn': "✅ Одобрить",
        'app_reject_btn': "❌ Отклонить",
        'app_comment_prompt': "✏️ Введите комментарий для заявителя (\u0438ли напишите \u2018-\u2018 чтобы не оставлять):",
        'app_approved_notify': (
            "🎉 <b>Ваша заявка на проживание ОДОБРЕНА!</b>\n\n"
            "🏢 Вы добавлены в список очереди на комнату.\n"
            "💬 Комментарий админа: <i>{comment}</i>\n\n"
            "Свяжитесь с АДМ Шахнозой для дальнейших деталей."
        ),
        'app_rejected_notify': (
            "❌ <b>Ваша заявка на проживание была отклонена.</b>\n"
            "💬 Причина: <i>{comment}</i>"
        ),
        'app_already_decided': "ℹ️ Данная заявка уже обработана (статус: {status}).",
        'app_done_label_approve': "✅ Одобрено",
        'app_done_label_reject': "❌ Отклонено",
        'applications_title': "📋 <b>ЗАЯВКИ НА ПРОЖИВАНИЕ:</b>\n\n",
        'app_list_item': "🔷 #{id} | {name} | {login} | {status}\n",
        'app_no_pending': "ℹ️ Нет ожидающих заявок.",
        'app_added_to_waiting': "✅ {name} автоматически добавлен в список очереди на сайте.",
    },

    # ─────────────── ENGLISH ───────────────
    'en': {
        'lang_name': '🇬🇧 English',

        'welcome': (
            "🏢 <b>Welcome to the Official School 21 Dormitory Bot!</b>\n\n"
            "📍 Address: Qalandar St., 24 (10 min from campus)\n\n"
            "📌 <b>What this bot does:</b>\n"
            "• 🧹 Kitchen duty schedule (7th floor)\n"
            "• 📊 Live resident statistics\n"
            "• 📝 Housing applications for dormitory (2026)\n\n"
            "📌 <b>Main commands:</b>\n"
            "• /apply — 📝 Apply for residence in the dormitory\n"
            "• /duty — Today's duty room (7th floor)\n"
            "• /language — Change bot language\n"
            "• /setgroup — Link group chat for morning reminders\n"
            "{admin_text}\n\n"
            "🌐 Website: school21dorm.onrender.com\n"
            "<i>All data is instantly synced with the website!</i>"
        ),
        'welcome_apply': (
            "📝 <b>Housing Application — School 21 2026</b>\n\n"
            "Send /apply to start filling in your application."
        ),
        'app_rules_sent': "📎 The <b>Dormitory Rules</b> are attached above. Please read them carefully!",
        'admin_privilege': "\n\n👑 <b>Admin Panel is available to you!</b> Send /admin to access it.",

        'select_language': "🌐 <b>Select language / Выберите язык / Tilni tanlang:</b>",
        'lang_changed': "✅ <b>Language successfully changed to English!</b>",
        'groups_lang_fixed': "ℹ️ In group chats, the language is always Russian.",

        'duty_title': "🧹 <b>KITCHEN DUTY SCHEDULE (7TH FLOOR)</b>",
        'duty_date': "📅 <b>Date:</b> {date_str}",
        'duty_status': "📍 <b>Status:</b> {status_icon}",
        'duty_today_room': "🔷 <b>ROOM {room_num} IS ON DUTY TODAY:</b>",
        'duty_no_residents': "  • <i>No one lives in this room</i>",
        'duty_task': "📌 <b>Duty:</b> Clean the 7th-floor kitchen and take out the trash.",
        'duty_status_completed': "✅ <b>COMPLETED</b>",
        'duty_status_pending': "⏳ <b>PENDING</b>",
        'duty_btn_done': "✅ We completed our duty!",
        'duty_not_found': "⚠️ Duty data not found.",
        'duty_no_schedule_today': "⚠️ No room assigned for duty today.",
        'duty_marked_done': "✅ Duty marked as completed!",
        'duty_done_updated': "🎉 <b>MARKED AS COMPLETED:</b> {user_name} via Telegram!\n<i>Status instantly synced with the website!</i>",

        'group_linked': "✅ <b>Group successfully linked!</b> Daily duty schedule will be sent here at 09:00 AM.",

        'no_admin_perm': "⛔ You don't have access to the dormitory admin panel.",
        'no_access': "⛔ No access",

        'btn_stats': "📊 Statistics",
        'btn_residents': "👥 Residents List",
        'btn_change_duty': "🧹 Change Duty Room",
        'btn_logs': "📑 Audit Logs",
        'btn_admins': "🔑 Admin List",
        'btn_refresh': "🔄 Refresh Panel",
        'btn_back': "⬅️ Back to Main Menu",
        'btn_language': "🌐 Change Language",
        'btn_back_to_menu': "⬅️ Back to Menu",

        'admin_menu': (
            "👑 <b>DORMITORY ADMIN PANEL</b>\n\n"
            "You are logged in as Administrator.\n"
            "Choose a section using the inline buttons below:\n\n"
            "📌 <b>Quick commands:</b>\n"
            "• <code>/add Full Name | Nick | M/F | Room</code> — Check in resident\n"
            "• <code>/evict ID</code> — Evict resident\n"
            "• <code>/move ID NewRoom</code> — Relocate resident\n"
            "• <code>/setduty YYYY-MM-DD Room</code> — Set duty room\n"
            "• <code>/addadmin TelegramID</code> — Add new admin\n"
            "• <code>/deladmin TelegramID</code> — Remove admin"
        ),

        'stats_title': "📊 <b>DORMITORY CURRENT STATISTICS (PROD)</b>\n\n",
        'stats_total': "👥 Total residents: <b>{total}</b>\n",
        'stats_floor2': "🌸 2nd Floor (Female): <b>{count}</b>\n",
        'stats_floor7': "🔷 7th Floor (Male): <b>{count}</b>\n",
        'stats_temp': "⏳ Temporary (14 days): <b>{count}</b>\n",
        'stats_waiting': "🛑 Waiting / No room: <b>{count}</b>\n",
        'stats_free_beds': "🛏️ Available beds: <b>{free}</b> out of {total_cap}",
        'stats_footer': "\n\n<i>Data instantly synced with SQLite and the website!</i>",

        'residents_title': "👥 <b>RESIDENTS BY ROOM:</b>\n\n",
        'residents_floor': "<b>FLOOR {floor}:</b>\n",
        'residents_room': "  • <b>Room {room}:</b> {names}\n",

        'logs_title': "📑 <b>RECENT ACTION LOGS (AUDIT):</b>\n\n",

        'admins_title': "🔑 <b>BOT ADMIN LIST:</b>\n\n",
        'admins_owner_label': "(👑 Main Owner)",
        'admins_add_hint': "📌 <b>To add a new admin, send:</b>\n<code>/addadmin TelegramID</code>",
        'admins_del_hint': "📌 <b>To remove an admin, send:</b>\n<code>/deladmin TelegramID</code>",

        'duty_rooms_title': "🧹 <b>SELECT A ROOM TO ASSIGN AS TODAY'S DUTY ROOM:</b>",
        'duty_room_btn': "📍 Room {room}",
        'duty_assigned_alert': "✅ Room {room} assigned as today's duty room ({date})!",
        'duty_assigned_msg': "✅ <b>Today's duty room ({date}) successfully changed to Room {room}!</b>\n\nData instantly updated on the website.",

        'add_success': "✅ <b>Resident successfully checked in!</b>\nID: #{res_id}\nName: {name}\nRoom: {room}",
        'add_waiting': "Waiting list",
        'add_error': "⚠️ <b>Command format:</b>\n<code>/add Full Name | Nick | M/F | RoomNumber</code>\n\n<i>Example:</i>\n<code>/add Ivan Ivanov | ivanov_i | M | 705</code>",

        'evict_success': "✅ <b>Resident ID #{res_id} successfully evicted!</b> Data updated on website and Excel.",
        'evict_error': "⚠️ <b>Command format:</b>\n<code>/evict ResidentID</code>\n\n<i>Example:</i> <code>/evict 15</code>",

        'move_success': "✅ <b>Resident {name} relocated to room {room}!</b>",
        'move_not_found': "⚠️ Resident with this ID not found.",
        'move_error': "⚠️ <b>Command format:</b>\n<code>/move ResidentID NewRoom</code>\n\n<i>Example:</i> <code>/move 15 706</code>",

        'setduty_success': "✅ <b>Duty on {date} assigned to room {room}!</b> Data updated on website.",
        'setduty_error': "⚠️ <b>Command format:</b>\n<code>/setduty YYYY-MM-DD RoomNumber</code>\n\n<i>Example:</i> <code>/setduty 2026-08-10 706</code>",

        'addadmin_success': "✅ <b>Telegram ID <code>{uid}</code> successfully added to the bot admin list!</b>",
        'addadmin_already': "ℹ️ User ID <code>{uid}</code> is already an admin.",
        'addadmin_error': "⚠️ <b>Command format:</b>\n<code>/addadmin TelegramID</code>\n\n<i>Example:</i> <code>/addadmin 123456789</code>",

        'deladmin_success': "✅ <b>Telegram ID <code>{uid}</code> removed from the admin list.</b>",
        'deladmin_owner': "⚠️ Cannot remove the main bot owner.",
        'deladmin_not_found': "ℹ️ User ID <code>{uid}</code> not found in admin list.",
        'deladmin_error': "⚠️ <b>Command format:</b>\n<code>/deladmin TelegramID</code>\n\n<i>Example:</i> <code>/deladmin 123456789</code>",

        # ===== APPLICATION =====
        'btn_apply': "📝 Apply for Residence",
        'btn_applications': "📋 Residence Applications",
        'apply_conditions': (
            "🏢 <b>SCHOOL 21 DORMITORY — 2026</b>\n\n"
            "📍 Address: Qalandar St., 24 (10 min from campus)\n\n"
            "We are conducting a preliminary survey for those wishing to live in the dormitory.\n\n"
            "❗ Project deadlines are reduced by 20% for residents\n"
            "❗ No places for residents of Kibray and Urta Chirchiq\n"
            "❗ Only participants 18+ years old\n"
            "❗ School does not provide temporary registration\n"
            "❗ Limited spots available\n\n"
            "💸 <b>Price:</b> 1,050,000 UZS/month. 1 month advance payment (non-refundable)\n"
            "🏢 Rooms for 4 or 6 people\n"
            "📌 Only for main-track peers.\n\n"
            "To apply, press the button below:"
        ),
        'apply_conditions_btn': "📝 Fill in Application",
        'apply_cancel_btn': "❌ Cancel",
        'apply_step1': "📅 Step 1/4. Enter your <b>desired move-in date</b>:\n<i>Format: DD.MM.YYYY (e.g. 01.09.2026)</i>",
        'apply_step2': "👤 Step 2/4. Enter your <b>Full Name (as in documents)</b>:",
        'apply_step3': "🏫 Step 3/4. Enter your <b>School 21 Login</b>:",
        'apply_step4': "💬 Step 4/4. Additional comment (optional):\n<i>By submitting you consent to personal data processing.</i>",
        'apply_skip_btn': "➡️ Skip",
        'apply_confirm': (
            "✅ <b>Review your application:</b>\n\n"
            "📅 Move-in date: <b>{date}</b>\n"
            "👤 Full name: <b>{name}</b>\n"
            "🏫 Login: <b>{login}</b>\n"
            "💬 Comment: <i>{comment}</i>\n\n"
            "Is all data correct?"
        ),
        'apply_confirm_btn': "✅ Submit Application",
        'apply_edit_btn': "✏️ Edit",
        'apply_success': (
            "✅ <b>Your application has been submitted!</b>\n\n"
            "📊 Application #: <b>#{app_id}</b>\n"
            "⏳ Status: <b>Under review</b>\n\n"
            "We will notify you of the administration's decision."
        ),
        'apply_cancelled': "❌ Application cancelled.",
        'apply_invalid_date': "⚠️ Invalid date format. Please enter as DD.MM.YYYY (01.09.2026):",

        'admin_new_app': (
            "📥 <b>NEW APPLICATION #{app_id}</b>\n\n"
            "👤 Name: <b>{name}</b>\n"
            "🏫 Login: <code>{login}</code>\n"
            "📅 Move-in date: <b>{date}</b>\n"
            "💬 Comment: <i>{comment}</i>\n"
            "📱 Telegram: {tg}\n"
            "🕑 Submitted: {created}"
        ),
        'app_approve_btn': "✅ Approve",
        'app_reject_btn': "❌ Reject",
        'app_comment_prompt': "✏️ Enter a comment for the applicant (or type '-' to skip):",
        'app_approved_notify': (
            "🎉 <b>Your dormitory application has been APPROVED!</b>\n\n"
            "🏢 You have been added to the room waiting list.\n"
            "💬 Admin comment: <i>{comment}</i>\n\n"
            "Contact ADM Shakhnoza for further details."
        ),
        'app_rejected_notify': (
            "❌ <b>Your dormitory application has been rejected.</b>\n"
            "💬 Reason: <i>{comment}</i>"
        ),
        'app_already_decided': "ℹ️ This application has already been processed (status: {status}).",
        'app_done_label_approve': "✅ Approved",
        'app_done_label_reject': "❌ Rejected",
        'applications_title': "📋 <b>RESIDENCE APPLICATIONS:</b>\n\n",
        'app_list_item': "🔷 #{id} | {name} | {login} | {status}\n",
        'app_no_pending': "ℹ️ No pending applications.",
        'app_added_to_waiting': "✅ {name} automatically added to the waiting list on website.",
    },

    # ─────────────── UZBEK ───────────────
    'uz': {
        'lang_name': "🇺🇿 O'zbekcha",

        'welcome': (
            "🏢 <b>School 21 Yotoqxonasi rasmiy botiga xush kelibsiz!</b>\n\n"
            "📍 Manzil: Qalandar ko'chasi, 24 (kampusdan 10 daqiqa)\n\n"
            "📌 <b>Bot imkoniyatlari:</b>\n"
            "• 🧹 Oshxona navbatchilik jadvali (7-qavat)\n"
            "• 📊 Yashovchilar statistikasi\n"
            "• 📝 Yotoqxonada yashash uchun arizalar topshirish (2026)\n\n"
            "📌 <b>Asosiy buyruqlar:</b>\n"
            "• /apply — 📝 Yotoqxonaga ariza topshirish\n"
            "• /duty — Bugungi navbatchilik jadvali (7-qavat)\n"
            "• /language — Tilni o'zgartirish\n"
            "• /setgroup — Guruh chatini ulash\n"
            "{admin_text}\n\n"
            "🌐 Veb-sayt: school21dorm.onrender.com\n"
            "<i>Barcha ma'lumotlar veb-sayt bilan zumda sinxronlanadi!</i>"
        ),
        'welcome_apply': (
            "📝 <b>Yashash uchun ariza — School 21 2026</b>\n\n"
            "Arizani to'ldirishni boshlash uchun /apply yuboring."
        ),
        'app_rules_sent': "📎 Yuqorida <b>Yotoqxonada yashash qoidalari</b> biriktirilgan. Iltimos, танишиб чиқинг!",
        'admin_privilege': "\n\n👑 <b>Siz uchun Admin Paneli mavjud!</b> Kirish uchun /admin yuboring.",

        'select_language': "🌐 <b>Tilni tanlang / Select language / Выберите язык:</b>",
        'lang_changed': "✅ <b>Til muvaffaqiyatli O'zbek tiliga o'zgartirildi!</b>",
        'groups_lang_fixed': "ℹ️ Guruh chatlarida til har doim Ruscha.",

        'duty_title': "🧹 <b>OSHXONA NAVBATCHILIK JADVALI (7-QAVAT)</b>",
        'duty_date': "📅 <b>Sana:</b> {date_str}",
        'duty_status': "📍 <b>Holat:</b> {status_icon}",
        'duty_today_room': "🔷 <b>BUGUN {room_num}-XONA NAVBATCHI:</b>",
        'duty_no_residents': "  • <i>Bu xonada hech kim yashamaydi</i>",
        'duty_task': "📌 <b>Vazifa:</b> 7-qavat oshxonasini tozalash va axlatni axlat qutisiga tashlash.",
        'duty_status_completed': "✅ <b>BAJARILDI</b>",
        'duty_status_pending': "⏳ <b>BAJARILISHI KUTILMOQDA</b>",
        'duty_btn_done': "✅ Biz navbatchilikni bajardik!",
        'duty_not_found': "⚠️ Navbatchilik ma'lumotlari topilmadi.",
        'duty_no_schedule_today': "⚠️ Bugunga tayinlangan navbatchi xona yo'q.",
        'duty_marked_done': "✅ Navbatchilik bajarildi deb belgilandi!",
        'duty_done_updated': "🎉 <b>BAJARILDI DEGAN BELGI QO'YILDI:</b> {user_name} Telegram orqali!\n<i>Holat veb-sayt bilan zumda sinxronlandi!</i>",

        'group_linked': "✅ <b>Guruh muvaffaqiyatli ulandi!</b> Har kuni soat 09:00 da navbatchilik jadvali yuboriladi.",

        'no_admin_perm': "⛔ Sizda yotoqxona admin paneliga kirish huquqi yo'q.",
        'no_access': "⛔ Ruxsat yo'q",

        'btn_stats': "📊 Statistika",
        'btn_residents': "👥 Yashovchilar ro'yxati",
        'btn_change_duty': "🧹 Navbatchini almashtirish",
        'btn_logs': "📑 Audit jurnali",
        'btn_admins': "🔑 Adminlar ro'yxati",
        'btn_refresh': "🔄 Panelni yangilash",
        'btn_back': "⬅️ Asosiy menyuga qaytish",
        'btn_language': "🌐 Tilni o'zgartirish",
        'btn_back_to_menu': "⬅️ Menyuga qaytish",

        'admin_menu': (
            "👑 <b>YOTOQXONA ADMIN PANELI</b>\n\n"
            "Siz Administrator sifatida kirdinggiz.\n"
            "Quyidagi inline tugmalar orqali bo'limni tanlang:\n\n"
            "📌 <b>Tezkor buyruqlar:</b>\n"
            "• <code>/add F.I.Sh | Nik | M/F | Xona</code> — Talabani joylashtirish\n"
            "• <code>/evict ID</code> — Talabani chiqarish\n"
            "• <code>/move ID YangiXona</code> — Talabani ko'chirish\n"
            "• <code>/setduty YYYY-MM-DD Xona</code> — Navbatchini tayinlash\n"
            "• <code>/addadmin TelegramID</code> — Yangi admin qo'shish\n"
            "• <code>/deladmin TelegramID</code> — Adminni o'chirish"
        ),

        'stats_title': "📊 <b>YOTOQXONA JORIY STATISTIKASI (PROD)</b>\n\n",
        'stats_total': "👥 Jami yashovchilar: <b>{total}</b> kishi\n",
        'stats_floor2': "🌸 2-Qavat (Qizlar): <b>{count}</b> kishi\n",
        'stats_floor7': "🔷 7-Qavat (Yigitlar): <b>{count}</b> kishi\n",
        'stats_temp': "⏳ Vaqtinchalik (14 kun): <b>{count}</b> kishi\n",
        'stats_waiting': "🛑 Navbatda / Xonasiz: <b>{count}</b> kishi\n",
        'stats_free_beds': "🛏️ Bo'sh o'rinlar: <b>{free}</b> ta {total_cap} tadan",
        'stats_footer': "\n\n<i>Ma'lumotlar SQLite va sayt bilan zumda sinxronlandi!</i>",

        'residents_title': "👥 <b>YASHOVCHILAR XONALAR BO'YICHA:</b>\n\n",
        'residents_floor': "<b>{floor}-QAVAT:</b>\n",
        'residents_room': "  • <b>{room}-Xona:</b> {names}\n",

        'logs_title': "📑 <b>SO'NGGI HARAKATLAR JURNALI (AUDIT):</b>\n\n",

        'admins_title': "🔑 <b>BOT ADMINLARI RO'YXATI:</b>\n\n",
        'admins_owner_label': "(👑 Bosh Egasi)",
        'admins_add_hint': "📌 <b>Yangi admin qo'shish uchun yuboring:</b>\n<code>/addadmin TelegramID</code>",
        'admins_del_hint': "📌 <b>Adminni o'chirish uchun yuboring:</b>\n<code>/deladmin TelegramID</code>",

        'duty_rooms_title': "🧹 <b>BUGUNGI NAVBATCHI XONANI TANLANG:</b>",
        'duty_room_btn': "📍 {room}-Xona",
        'duty_assigned_alert': "✅ {room}-Xona bugungi navbatchi ({date}) etib tayinlandi!",
        'duty_assigned_msg': "✅ <b>Bugungi ({date}) navbatchi xona {room}-Xonaga muvaffaqiyatli o'zgartirildi!</b>\n\nMa'lumotlar saytda zumda yangilandi.",

        'add_success': "✅ <b>Talaba muvaffaqiyatli joylashtirildi!</b>\nID: #{res_id}\nF.I.Sh.: {name}\nXona: {room}",
        'add_waiting': "Navbatda",
        'add_error': "⚠️ <b>Buyruq formati:</b>\n<code>/add F.I.Sh | Nik | M/F | XonaRaqami</code>\n\n<i>Misol:</i>\n<code>/add Ivanov Ivan | ivanov_i | M | 705</code>",

        'evict_success': "✅ <b>ID #{res_id} talaba muvaffaqiyatli chiqarildi!</b> Ma'lumotlar sayt va Excelda yangilandi.",
        'evict_error': "⚠️ <b>Buyruq formati:</b>\n<code>/evict TalabaID</code>\n\n<i>Misol:</i> <code>/evict 15</code>",

        'move_success': "✅ <b>{name} {room}-xonaga ko'chirildi!</b>",
        'move_not_found': "⚠️ Bu ID bilan talaba topilmadi.",
        'move_error': "⚠️ <b>Buyruq formati:</b>\n<code>/move TalabaID YangiXona</code>\n\n<i>Misol:</i> <code>/move 15 706</code>",

        'setduty_success': "✅ <b>{date} sanasidagi navbatchilik {room}-xonaga tayinlandi!</b> Ma'lumotlar saytda yangilandi.",
        'setduty_error': "⚠️ <b>Buyruq formati:</b>\n<code>/setduty YYYY-MM-DD XonaRaqami</code>\n\n<i>Misol:</i> <code>/setduty 2026-08-10 706</code>",

        'addadmin_success': "✅ <b>Telegram ID <code>{uid}</code> bot adminlari ro'yxatiga muvaffaqiyatli qo'shildi!</b>",
        'addadmin_already': "ℹ️ ID <code>{uid}</code> foydalanuvchi allaqachon admin.",
        'addadmin_error': "⚠️ <b>Buyruq formati:</b>\n<code>/addadmin TelegramID</code>\n\n<i>Misol:</i> <code>/addadmin 123456789</code>",

        'deladmin_success': "✅ <b>Telegram ID <code>{uid}</code> adminlar ro'yxatidan o'chirildi.</b>",
        'deladmin_owner': "⚠️ Botning bosh egasini o'chirib bo'lmaydi.",
        'deladmin_not_found': "ℹ️ ID <code>{uid}</code> foydalanuvchi adminlar ro'yxatida topilmadi.",
        'deladmin_error': "⚠️ <b>Buyruq formati:</b>\n<code>/deladmin TelegramID</code>\n\n<i>Misol:</i> <code>/deladmin 123456789</code>",

        # ===== ARIZA / APPLICATION =====
        'btn_apply': "📝 Yashash uchun ariza topshirish",
        'btn_applications': "📋 Joylashish arizalari",
        'apply_conditions': (
            "🏢 <b>SCHOOL 21 YOTOQXONASI — 2026</b>\n\n"
            "📍 Manzil: Qalandar ko'chasi, 24 (kampusdan 10 daqiqa)\n\n"
            "Yotoqxonada yashash istagi borlar uchun dastlabki so'rovnoma o'tkazmoqdamiz.\n\n"
            "❗ Yotoqxona yashovchilari uchun loyiha deadlayn 20% qisqartiriladi\n"
            "❗ Qibray va O'rta Chirchiq aholisiga joy berilmaydi\n"
            "❗ Faqat 18 yoshdan katta ishtirokchilar\n"
            "❗ Maktab ro'yxatdan o'tish yoki propiska bermaydi\n"
            "❗ Joylar soni cheklangan\n\n"
            "💸 <b>Narxi:</b> 1 050 000 so'm/oy. 1 oy uchun oldindan to'lov (qaytarib berilmaydi)\n"
            "🏢 Xonalar 4 yoki 6 kishilik\n"
            "📌 Faqat asosiy o'qitish piyonlari uchun.\n\n"
            "Ariza topshirish uchun quyidagi tugmani bosing:"
        ),
        'apply_conditions_btn': "📝 Arizani to'ldirish",
        'apply_cancel_btn': "❌ Bekor qilish",
        'apply_step1': "📅 1/4-qadam. <b>Ko'chib kirish sanasini</b> kiriting:\n<i>Format: KK.OO.YYYY (masalan: 01.09.2026)</i>",
        'apply_step2': "👤 2/4-qadam. <b>Hujjatlardagi F.I.Sh.</b>ni kiriting:",
        'apply_step3': "🏫 3/4-qadam. <b>School 21 loginingizni</b> kiriting:",
        'apply_step4': "💬 4/4-qadam. Qo'shimcha izoh (ixtiyoriy):\n<i>Yuborish bilan shaxsiy ma'lumotlarni qayta ishlashga rozilik bildirasiz.</i>",
        'apply_skip_btn': "➡️ O'tkazib yuborish",
        'apply_confirm': (
            "✅ <b>Ariza ma'lumotlarini tekshiring:</b>\n\n"
            "📅 Ko'chib kirish sanasi: <b>{date}</b>\n"
            "👤 F.I.Sh.: <b>{name}</b>\n"
            "🏫 Login: <b>{login}</b>\n"
            "💬 Izoh: <i>{comment}</i>\n\n"
            "Barcha ma'lumotlar to'g'rimi?"
        ),
        'apply_confirm_btn': "✅ Arizani yuborish",
        'apply_edit_btn': "✏️ O'zgartirish",
        'apply_success': (
            "✅ <b>Arizangiz muvaffaqiyatli yuborildi!</b>\n\n"
            "📊 Ariza raqami: <b>#{app_id}</b>\n"
            "⏳ Holat: <b>Ko'rib chiqilmoqda</b>\n\n"
            "Biz sizga ma'muriyat qarori haqida xabar beramiz."
        ),
        'apply_cancelled': "❌ Ariza bekor qilindi.",
        'apply_invalid_date': "⚠️ Noto'g'ri sana formati. Iltimos KK.OO.YYYY formatida kiriting (01.09.2026):",

        'admin_new_app': (
            "📥 <b>YANGI ARIZA #{app_id}</b>\n\n"
            "👤 F.I.Sh.: <b>{name}</b>\n"
            "🏫 Login: <code>{login}</code>\n"
            "📅 Ko'chib kirish sanasi: <b>{date}</b>\n"
            "💬 Izoh: <i>{comment}</i>\n"
            "📱 Telegram: {tg}\n"
            "🕑 Yuborildi: {created}"
        ),
        'app_approve_btn': "✅ Tasdiqlash",
        'app_reject_btn': "❌ Rad etish",
        'app_comment_prompt': "✏️ Ariza beruvchi uchun izoh kiriting (yoki '-' yozing o'tkazib yuborish uchun):",
        'app_approved_notify': (
            "🎉 <b>Yotoqxonada yashash arizangiz TASDIQLANDI!</b>\n\n"
            "🏢 Siz xona kutish ro'yxatiga qo'shildingiz.\n"
            "💬 Admin izohi: <i>{comment}</i>\n\n"
            "Batafsil ma'lumot uchun ADM Shakhnoza bilan bog'laning."
        ),
        'app_rejected_notify': (
            "❌ <b>Yotoqxonada yashash arizangiz rad etildi.</b>\n"
            "💬 Sabab: <i>{comment}</i>"
        ),
        'app_already_decided': "ℹ️ Bu ariza allaqachon ko'rib chiqilgan (holat: {status}).",
        'app_done_label_approve': "✅ Tasdiqlandi",
        'app_done_label_reject': "❌ Rad etildi",
        'applications_title': "📋 <b>JOYLASHISH ARIZALARI:</b>\n\n",
        'app_list_item': "🔷 #{id} | {name} | {login} | {status}\n",
        'app_no_pending': "ℹ️ Kutilayotgan arizalar yo'q.",
        'app_added_to_waiting': "✅ {name} saytda kutish ro'yxatiga avtomatik qo'shildi.",
    },
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
    """Return translated string for the given key."""
    lang = get_user_lang(chat_type, telegram_id)
    lang_dict = LOCALES.get(lang, LOCALES['ru'])
    template = lang_dict.get(key) or LOCALES['ru'].get(key, key)
    if kwargs:
        try:
            return template.format(**kwargs)
        except Exception:
            return template
    return template
