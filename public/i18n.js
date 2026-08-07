const I18N_TRANSLATIONS = {
    ru: {
        // App header & brand
        app_title: "Система Управления Общежитием",
        prod_badge: "PROD v2.0",
        
        // Navigation / Tabs
        nav_dashboard: "Дашборд & Схема",
        nav_residents: "Список Жильцов",
        nav_duty: "График Дежурств",
        nav_audit: "Журнал Аудита",
        btn_add_resident: "+ Заселить жильца",
        btn_export_excel: "📥 Экспорт в Excel",

        // Stats Cards
        stat_total_residents: "Всего проживающих",
        stat_total_sub: "Постоянные и временные жильцы",
        stat_floor2: "2 Этаж (Девушки)",
        stat_floor2_sub: "Проживает на этаже",
        stat_floor7: "7 Этаж (Парни)",
        stat_floor7_sub: "Проживает на этаже",
        stat_free_beds: "Свободные койки",
        stat_free_beds_sub: "из {total_capacity} мест в здании",

        // Section Headers & Filters
        sec_rooms_map: "Схема комнат и заселения",
        filter_all_floors: "Все этажи",
        filter_floor2: "2 Этаж (Женский)",
        filter_floor7: "7 Этаж (Мужской)",
        filter_all_status: "Все статусы",
        filter_permanent: "Постоянные",
        filter_14_days: "Временные (14 дней)",
        filter_waiting: "В очереди",

        // Floor labels & Room cards
        floor2_title: "🌸 2 ЭТАЖ (ЖЕНСКИЙ БЛОК)",
        floor7_title: "🔷 7 ЭТАЖ (МУЖСКОЙ БЛОК)",
        unassigned_title: "⏳ В ОЧЕРЕДИ / БЕЗ КОМНАТЫ",
        room_label: "Комната {room_num}",
        beds_label: "{occupied}/{capacity} мест",
        room_empty: "Комната пуста",
        btn_add_short: "+ Заселить",
        
        // Residents Table
        sec_residents_title: "Реестр проживающих студентов",
        search_placeholder: "🔍 Поиск по ФИО, нику или комнате...",
        col_code: "№ Кода",
        col_fullname: "ФИО Студента",
        col_nickname: "Никнейм",
        col_gender: "Пол",
        col_room: "Комната",
        col_status: "Статус",
        col_actions: "Действия",
        gender_male: "Мужской",
        gender_female: "Женский",
        status_permanent: "Постоянный",
        status_14_days: "14 дней",
        status_waiting: "В очереди",
        btn_move: "Переселить",
        btn_evict: "Выселить",

        // Duty Schedule Tab
        duty_sec_title: "График дежурства по кухне (7 Этаж)",
        duty_today_card: "Дежурные на сегодня:",
        duty_room_num: "Комната {room}",
        duty_status_completed: "✅ ВЫПОЛНЕНО",
        duty_status_pending: "⏳ ОЖИДАЕТ ВЫПОЛНЕНИЯ",
        btn_mark_duty_done: "✅ Отметить выполненным",
        btn_change_duty_room: "✏️ Сменить комнату",
        duty_list_title: "Календарь дежурств на текущий месяц",

        // Audit Log Tab
        audit_sec_title: "Журнал аудита действий (Audit Logs)",
        col_time: "Время",
        col_action: "Действие",
        col_details: "Детали",

        // Modals
        modal_add_title: "Заселение нового жильца",
        label_fullname: "ФИО Студента *",
        label_code: "Числовой код (№)",
        label_nickname: "Никнейм Platform 21",
        label_profile: "Ссылка на профиль",
        label_gender: "Пол *",
        label_room: "Номер комнаты",
        label_status: "Статус проживания *",
        btn_cancel: "Отмена",
        btn_save: "Заселить жильца",

        modal_move_title: "Переселение жильца",
        label_new_room: "Выберите новую комнату",
        btn_save_move: "Сохранить изменения",

        modal_change_duty_title: "Назначение дежурной комнаты",
        label_duty_date: "Дата дежурства",
        label_duty_room: "Выберите дежурную комнату",
        btn_save_duty: "Назначить дежурного",

        // Footer & Toast
        footer_copyright: "Система Управления Общежитием v2.0 • Все права защищены",

        // Admin auth buttons
        btn_admin_login: "Вход для админа",
        btn_admin_logout: "Выйти из админа",
        admin_login_label: "Введите пароль администратора *",
        admin_login_btn: "Войти",
        admin_modal_title: "Вход Администратора",
        admin_require_msg: "🔒 Эта функция доступна только Администратору. Пожалуйста, войдите с помощью пароля администратора.",
        err_wrong_password: "Неверный пароль администратора",
        err_connection: "Ошибка соединения с сервером",
        err_save: "Ошибка сохранения данных.",
        err_duty_save: "Ошибка сохранения дежурства.",
        err_evict: "Ошибка выселения.",
        err_not_found: "Жилец не найден.",

        // Floor / Room rendering (app.js)
        floor_label: "{floor} Этаж",
        floor2_badge: "Женский блок",
        floor7_badge: "Мужской блок",
        rooms_count: "(14 комнат)",
        waiting_section_title: "В очереди / Без комнаты",
        waiting_badge: "Список ожидания ({count} чел.)",
        waiting_empty: "В очереди никого нет",
        waiting_icon_label: "Ожидающие",
        people_count: "{count} чел.",
        occ_count: "{occ} / {cap} чел.",
        cap_6: "6 мест",
        cap_4: "4 места",

        // Resident item
        tag_14days: "14 дней",
        confirm_evict: "Вы действительно хотите выселить жильца \"{name}\"?",

        // Room options in select
        room_option_queue: "-- В очередь (Без комнаты) --",
        room_option_label: "Комната {room} ({occ}/{cap} чел.) {extra}",
        room_option_6beds: "[6-местная]",
        duty_room_option: "Комната {room} ({count} чел.) {empty}",
        duty_room_empty_tag: "[Пустая]",

        // Modal titles / labels (dynamic)
        modal_add_title_dynamic: "Заселение нового жильца",
        modal_edit_title_dynamic: "Редактирование: {name}",
        duty_modal_title_dynamic: "Дежурство на {date}",
        duty_floor_display: "{date} (7 этаж)",

        // Calendar
        cal_today_label: "СЕГОДНЯ",
        cal_no_residents: "Без жильцов",
        cal_status_completed: "✅ Выполнено",
        cal_status_pending: "⏳ Запланировано",
        cal_status_skipped: "⚠️ Пропущено",
        cal_status_replaced: "🔄 Заменено",
        cal_day_header_7floor: "🔷 Комн. {room}",
        btn_prev: "Назад",
        btn_next: "Вперед",

        // Header subtitle
        header_subtitle: "База данных SQLite (PROD) • Дежурства по кухне (7 Этаж)",

        // Duty banner
        banner_floor7: "🔷 7 Этаж:",
        banner_room: "Комната {room}",
        banner_no_residents: "Нет жильцов",

        // Logs modal
        logs_modal_title: "Журнал действий аудита",
        col_time_log: "Время",
        col_action_log: "Действие",
        col_details_log: "Подробности",
        btn_close: "Закрыть",

        // Form labels & placeholders (modal)
        ph_fullname: "Например: Иванов Иван Иванович",
        ph_nickname: "Например: ivanov_i",
        ph_profile: "https://platform.21-school.ru/admin/profile/...",
        ph_notes: "Дополнительная информация...",
        ph_duty_notes: "Причина смены или заметка...",
        label_notes: "Заметки / Примечание",
        label_profile_opt: "Ссылка на профиль (опционально)",
        label_duty_room_required: "Дежурная Комната *",
        label_duty_status: "Статус дежурства",
        label_duty_notes: "Примечание",
        duty_status_scheduled: "⏳ Запланировано",
        duty_status_completed_opt: "✅ Выполнено",
        duty_status_skipped_opt: "⚠️ Пропущено",
        duty_status_replaced_opt: "🔄 Перенесено / Заменено",
        select_male: "Мужской",
        select_female: "Женский",
        select_permanent: "Постоянный жилец",
        select_14days: "Временное проживание (14 дней)",
        select_waiting: "В очереди",
        btn_save_resident: "Сохранить",

        // Calendar days of week
        cal_dow_mon: "Пн",
        cal_dow_tue: "Вт",
        cal_dow_wed: "Ср",
        cal_dow_thu: "Чт",
        cal_dow_fri: "Пт",
        cal_dow_sat: "Сб",
        cal_dow_sun: "Вс",

        // Application form
        btn_apply_form: "📝 Подать заявку",
        apply_modal_title: "Заявка на проживание — School 21 2026",
        apply_conditions_title: "Об общежитии",
        apply_cond_text: (
            "📍 Манзес: ул. Каландар, 24 (10 мин. от кампуса). " +
            "❗ Для жителей Кибрая и Урта Чирчик места не предоставляются. " +
            "❗ Только 18+. ❗ Оплата 1 050 000 сум/мес за рансо. ❗ Для пиров основного обучения."
        ),
        apply_label_date: "Дата заселения *",
        apply_label_name: "ФИО по документам *",
        apply_label_login: "Login School 21 *",
        apply_label_comments: "Комментарий (необязательно)",
        apply_label_consent: "Даю согласие на обработку персональных данных",
        apply_ph_date: "Например: 01.09.2026",
        apply_ph_name: "Фамилия Имя Отчество",
        apply_ph_login: "your_login",
        apply_ph_comments: "Дополнительная информация",
        apply_btn_submit: "✅ Отправить заявку",
        apply_btn_cancel: "Отмена",
        apply_success_msg: "✅ Заявка отправлена! Мы уведомим вас о решении.",
        apply_err_required: "Пожалуйста, заполните все обязательные поля",
        apply_err_consent: "Необходимо ваше согласие на обработку данных",
        apply_required_note: "* Обязательные поля",
    },
    en: {
        app_title: "Dormitory Management System",
        prod_badge: "PROD v2.0",
        
        nav_dashboard: "Dashboard & Map",
        nav_residents: "Resident List",
        nav_duty: "Duty Schedule",
        nav_audit: "Audit Logs",
        btn_add_resident: "+ Add Resident",
        btn_export_excel: "📥 Export to Excel",

        stat_total_residents: "Total Residents",
        stat_total_sub: "Permanent and temporary residents",
        stat_floor2: "2nd Floor (Female)",
        stat_floor2_sub: "Living on this floor",
        stat_floor7: "7th Floor (Male)",
        stat_floor7_sub: "Living on this floor",
        stat_free_beds: "Available Beds",
        stat_free_beds_sub: "out of {total_capacity} total beds",

        sec_rooms_map: "Room Occupancy Map",
        filter_all_floors: "All Floors",
        filter_floor2: "2nd Floor (Female)",
        filter_floor7: "7th Floor (Male)",
        filter_all_status: "All Statuses",
        filter_permanent: "Permanent",
        filter_14_days: "Temporary (14 days)",
        filter_waiting: "Waiting List",

        floor2_title: "🌸 2ND FLOOR (FEMALE BLOCK)",
        floor7_title: "🔷 7TH FLOOR (MALE BLOCK)",
        unassigned_title: "⏳ WAITING LIST / NO ROOM",
        room_label: "Room {room_num}",
        beds_label: "{occupied}/{capacity} beds",
        room_empty: "Room is empty",
        btn_add_short: "+ Add",
        
        sec_residents_title: "Student Resident Directory",
        search_placeholder: "🔍 Search by name, nickname, or room...",
        col_code: "Code #",
        col_fullname: "Student Full Name",
        col_nickname: "Nickname",
        col_gender: "Gender",
        col_room: "Room",
        col_status: "Status",
        col_actions: "Actions",
        gender_male: "Male",
        gender_female: "Female",
        status_permanent: "Permanent",
        status_14_days: "14 days",
        status_waiting: "Waiting",
        btn_move: "Relocate",
        btn_evict: "Evict",

        // Duty Schedule Tab
        duty_sec_title: "Kitchen Duty Schedule (7th Floor)",
        duty_today_card: "On duty today:",
        duty_room_num: "Room {room}",
        duty_status_completed: "✅ COMPLETED",
        duty_status_pending: "⏳ PENDING",
        btn_mark_duty_done: "✅ Mark as Completed",
        btn_change_duty_room: "✏️ Change Room",
        duty_list_title: "Monthly Duty Calendar",

        audit_sec_title: "System Audit Logs",
        col_time: "Time",
        col_action: "Action",
        col_details: "Details",

        modal_add_title: "Check-in New Resident",
        label_fullname: "Student Full Name *",
        label_code: "Numeric Code (#)",
        label_nickname: "Platform 21 Nickname",
        label_profile: "Profile Link",
        label_gender: "Gender *",
        label_room: "Room Number",
        label_status: "Residence Status *",
        btn_cancel: "Cancel",
        btn_save: "Check-in Resident",

        modal_move_title: "Relocate Resident",
        label_new_room: "Select New Room",
        btn_save_move: "Save Changes",

        modal_change_duty_title: "Assign Duty Room",
        label_duty_date: "Duty Date",
        label_duty_room: "Select Duty Room",
        btn_save_duty: "Assign Duty",

        footer_copyright: "Dormitory Management System v2.0 • All rights reserved",

        btn_admin_login: "Admin Login",
        btn_admin_logout: "Logout Admin",
        admin_login_label: "Enter admin password *",
        admin_login_btn: "Login",
        admin_modal_title: "Administrator Login",
        admin_require_msg: "🔒 This feature is available to Administrators only. Please log in with the admin password.",
        err_wrong_password: "Wrong admin password",
        err_connection: "Server connection error",
        err_save: "Error saving data.",
        err_duty_save: "Error saving duty.",
        err_evict: "Error evicting resident.",
        err_not_found: "Resident not found.",

        floor_label: "Floor {floor}",
        floor2_badge: "Female block",
        floor7_badge: "Male block",
        rooms_count: "(14 rooms)",
        waiting_section_title: "Waiting List / No Room",
        waiting_badge: "Waiting list ({count})",
        waiting_empty: "No one in the waiting list",
        waiting_icon_label: "Waiting",
        people_count: "{count} people",
        occ_count: "{occ} / {cap} beds",
        cap_6: "6 beds",
        cap_4: "4 beds",

        tag_14days: "14 days",
        confirm_evict: "Are you sure you want to evict \"{name}\"?",

        room_option_queue: "-- Waiting list (No room) --",
        room_option_label: "Room {room} ({occ}/{cap}) {extra}",
        room_option_6beds: "[6-bed]",
        duty_room_option: "Room {room} ({count}) {empty}",
        duty_room_empty_tag: "[Empty]",

        modal_add_title_dynamic: "Check-in New Resident",
        modal_edit_title_dynamic: "Editing: {name}",
        duty_modal_title_dynamic: "Duty on {date}",
        duty_floor_display: "{date} (7th floor)",

        cal_today_label: "TODAY",
        cal_no_residents: "No residents",
        cal_status_completed: "✅ Completed",
        cal_status_pending: "⏳ Scheduled",
        cal_status_skipped: "⚠️ Skipped",
        cal_status_replaced: "🔄 Replaced",
        cal_day_header_7floor: "🔷 Room {room}",
        btn_prev: "Back",
        btn_next: "Next",

        header_subtitle: "SQLite Database (PROD) • Kitchen Duty (7th Floor)",
        banner_floor7: "🔷 7th Floor:",
        banner_room: "Room {room}",
        banner_no_residents: "No residents",

        logs_modal_title: "System Audit Logs",
        col_time_log: "Time",
        col_action_log: "Action",
        col_details_log: "Details",
        btn_close: "Close",

        ph_fullname: "e.g. Ivan Ivanov",
        ph_nickname: "e.g. ivanov_i",
        ph_profile: "https://platform.21-school.ru/admin/profile/...",
        ph_notes: "Additional info...",
        ph_duty_notes: "Reason for change or note...",
        label_notes: "Notes / Remarks",
        label_profile_opt: "Profile link (optional)",
        label_duty_room_required: "Duty Room *",
        label_duty_status: "Duty Status",
        label_duty_notes: "Note",
        duty_status_scheduled: "⏳ Scheduled",
        duty_status_completed_opt: "✅ Completed",
        duty_status_skipped_opt: "⚠️ Skipped",
        duty_status_replaced_opt: "🔄 Rescheduled / Replaced",
        select_male: "Male",
        select_female: "Female",
        select_permanent: "Permanent resident",
        select_14days: "Temporary (14 days)",
        select_waiting: "Waiting list",
        btn_save_resident: "Save",

        cal_dow_mon: "Mon",
        cal_dow_tue: "Tue",
        cal_dow_wed: "Wed",
        cal_dow_thu: "Thu",
        cal_dow_fri: "Fri",
        cal_dow_sat: "Sat",
        cal_dow_sun: "Sun",

        // Application form
        btn_apply_form: "📝 Apply for Residence",
        apply_modal_title: "Residence Application — School 21 2026",
        apply_conditions_title: "About the Dormitory",
        apply_cond_text: (
            "📍 Address: Qalandar St., 24 (10 min from campus). " +
            "❗ No places for Kibray / Urta Chirchiq residents. " +
            "❗ 18+ only. " +
            "❗ 1,050,000 UZS/month prepaid. " +
            "❗ Main-track peers only."
        ),
        apply_label_date: "Move-in date *",
        apply_label_name: "Full name (as in documents) *",
        apply_label_login: "School 21 Login *",
        apply_label_comments: "Comment (optional)",
        apply_label_consent: "I consent to personal data processing",
        apply_ph_date: "e.g. 01.09.2026",
        apply_ph_name: "Last First Middle",
        apply_ph_login: "your_login",
        apply_ph_comments: "Additional information",
        apply_btn_submit: "✅ Submit Application",
        apply_btn_cancel: "Cancel",
        apply_success_msg: "✅ Application submitted! We will notify you of the decision.",
        apply_err_required: "Please fill in all required fields",
        apply_err_consent: "Your consent to data processing is required",
        apply_required_note: "* Required fields",
    },
    uz: {
        app_title: "Yotoqxona Boshqaruv Tizimi",
        prod_badge: "PROD v2.0",
        
        nav_dashboard: "Boshqaruv & Xarita",
        nav_residents: "Yashovchilar Ro'yxati",
        nav_duty: "Navbatchilik Jadvali",
        nav_audit: "Audit Jurnali",
        btn_add_resident: "+ Talabani joylashtirish",
        btn_export_excel: "📥 Excelga eksport",

        stat_total_residents: "Jami yashovchilar",
        stat_total_sub: "Doimiy va vaqtinchalik yashovchilar",
        stat_floor2: "2-Qavat (Qizlar)",
        stat_floor2_sub: "Qavatda yashaydi",
        stat_floor7: "7-Qavat (Yigitlar)",
        stat_floor7_sub: "Qavatda yashaydi",
        stat_free_beds: "Bo'sh o'rinlar",
        stat_free_beds_sub: "{total_capacity} ta o'rindan",

        sec_rooms_map: "Xonalar va joylashuv xaritasi",
        filter_all_floors: "Barcha qavatlar",
        filter_floor2: "2-Qavat (Qizlar)",
        filter_floor7: "7-Qavat (Yigitlar)",
        filter_all_status: "Barcha maqomlar",
        filter_permanent: "Doimiy",
        filter_14_days: "Vaqtinchalik (14 kun)",
        filter_waiting: "Navbatda",

        floor2_title: "🌸 2-QAVAT (QIZLAR BLOKI)",
        floor7_title: "🔷 7-QAVAT (YIGITLAR BLOKI)",
        unassigned_title: "⏳ NAVBATDA / XONASIZ",
        room_label: "{room_num}-Xona",
        beds_label: "{occupied}/{capacity} o'rin",
        room_empty: "Xona bo'sh",
        btn_add_short: "+ Joylashtirish",
        
        sec_residents_title: "Yashovchi talabalar reyestri",
        search_placeholder: "🔍 F.I.Sh., nik yoki xona bo'yicha qidiruv...",
        col_code: "Kod №",
        col_fullname: "Talaba F.I.Sh.",
        col_nickname: "Nikneym",
        col_gender: "Jinsi",
        col_room: "Xona",
        col_status: "Maqomi",
        col_actions: "Amallar",
        gender_male: "Erkak",
        gender_female: "Ayol",
        status_permanent: "Doimiy",
        status_14_days: "14 kunlik",
        status_waiting: "Navbatda",
        btn_move: "Ko'chirish",
        btn_evict: "Chiqarish",

        // Duty Schedule Tab
        duty_sec_title: "Oshxona navbatchilik jadvali (7-qavat)",
        duty_today_card: "Bugungi navbatchilar:",
        duty_room_num: "{room}-Xona",
        duty_status_completed: "✅ BAJARILDI",
        duty_status_pending: "⏳ BAJARILISHI KUTILMOQDA",
        btn_mark_duty_done: "✅ Bajarildi deb belgilash",
        btn_change_duty_room: "✏️ Xonani almashtirish",
        duty_list_title: "Joriy oy uchun navbatchilik kalendari",

        audit_sec_title: "Tizim harakatlari jurnali (Audit)",
        col_time: "Vaqt",
        col_action: "Harakat",
        col_details: "Tafsilotlar",

        modal_add_title: "Yangi talabani joylashtirish",
        label_fullname: "Talaba F.I.Sh. *",
        label_code: "Soniya kodi (№)",
        label_nickname: "Platform 21 Nikneymi",
        label_profile: "Profil havolasi",
        label_gender: "Jinsi *",
        label_room: "Xona raqami",
        label_status: "Yashash maqomi *",
        btn_cancel: "Bekor qilish",
        btn_save: "Talabani joylashtirish",

        modal_move_title: "Talabani ko'chirish",
        label_new_room: "Yangi xonani tanlang",
        btn_save_move: "O'zgarishlarni saqlash",

        modal_change_duty_title: "Navbatchi xonani tayinlash",
        label_duty_date: "Navbatchilik sanasi",
        label_duty_room: "Navbatchi xonani tanlang",
        btn_save_duty: "Navbatchini tayinlash",

        footer_copyright: "Yotoqxona Boshqaruv Tizimi v2.0 • Barcha huquqlar himoyalangan",

        btn_admin_login: "Admin kirish",
        btn_admin_logout: "Admindan chiqish",
        admin_login_label: "Admin parolini kiriting *",
        admin_login_btn: "Kirish",
        admin_modal_title: "Administrator Kirishi",
        admin_require_msg: "🔒 Bu funksiya faqat Administratorlar uchun mavjud. Iltimos, admin paroli bilan kiring.",
        err_wrong_password: "Noto'g'ri admin paroli",
        err_connection: "Server bilan ulanish xatosi",
        err_save: "Ma'lumotlarni saqlashda xato.",
        err_duty_save: "Navbatchilikni saqlashda xato.",
        err_evict: "Talabani chiqarishda xato.",
        err_not_found: "Talaba topilmadi.",

        floor_label: "{floor}-Qavat",
        floor2_badge: "Qizlar bloki",
        floor7_badge: "Yigitlar bloki",
        rooms_count: "(14 xona)",
        waiting_section_title: "Navbatda / Xonasiz",
        waiting_badge: "Kutish ro'yxati ({count} kishi)",
        waiting_empty: "Navbatda hech kim yo'q",
        waiting_icon_label: "Kutayotganlar",
        people_count: "{count} kishi",
        occ_count: "{occ} / {cap} kishi",
        cap_6: "6 o'rin",
        cap_4: "4 o'rin",

        tag_14days: "14 kun",
        confirm_evict: "\"{name}\" talabani chiqarishni tasdiqlaysizmi?",

        room_option_queue: "-- Navbatga (Xonasiz) --",
        room_option_label: "{room}-Xona ({occ}/{cap} kishi) {extra}",
        room_option_6beds: "[6-o'rinli]",
        duty_room_option: "{room}-Xona ({count} kishi) {empty}",
        duty_room_empty_tag: "[Bo'sh]",

        modal_add_title_dynamic: "Yangi talabani joylashtirish",
        modal_edit_title_dynamic: "Tahrirlash: {name}",
        duty_modal_title_dynamic: "{date} sanasidagi navbatchilik",
        duty_floor_display: "{date} (7-qavat)",

        cal_today_label: "BUGUN",
        cal_no_residents: "Yashovchi yo'q",
        cal_status_completed: "✅ Bajarildi",
        cal_status_pending: "⏳ Rejalashtirilgan",
        cal_status_skipped: "⚠️ O'tkazib yuborildi",
        cal_status_replaced: "🔄 Almashtirildi",
        cal_day_header_7floor: "🔷 {room}-Xona",
        btn_prev: "Orqaga",
        btn_next: "Oldinga",

        header_subtitle: "SQLite Ma'lumotlar Bazasi (PROD) • Oshxona Navbatchiligi (7-Qavat)",
        banner_floor7: "🔷 7-Qavat:",
        banner_room: "{room}-Xona",
        banner_no_residents: "Yashovchi yo'q",

        logs_modal_title: "Tizim audit jurnali",
        col_time_log: "Vaqt",
        col_action_log: "Harakat",
        col_details_log: "Tafsilotlar",
        btn_close: "Yopish",

        ph_fullname: "Masalan: Ivanov Ivan",
        ph_nickname: "Masalan: ivanov_i",
        ph_profile: "https://platform.21-school.ru/admin/profile/...",
        ph_notes: "Qo'shimcha ma'lumot...",
        ph_duty_notes: "Almashtirish sababi yoki izoh...",
        label_notes: "Izohlar / Eslatmalar",
        label_profile_opt: "Profil havolasi (ixtiyoriy)",
        label_duty_room_required: "Navbatchi Xona *",
        label_duty_status: "Navbatchilik holati",
        label_duty_notes: "Izoh",
        duty_status_scheduled: "⏳ Rejalashtirilgan",
        duty_status_completed_opt: "✅ Bajarildi",
        duty_status_skipped_opt: "⚠️ O'tkazib yuborildi",
        duty_status_replaced_opt: "🔄 Ko'chirildi / Almashtirildi",
        select_male: "Erkak",
        select_female: "Ayol",
        select_permanent: "Doimiy yashovchi",
        select_14days: "Vaqtinchalik (14 kun)",
        select_waiting: "Navbatda",
        btn_save_resident: "Saqlash",

        cal_dow_mon: "Du",
        cal_dow_tue: "Se",
        cal_dow_wed: "Ch",
        cal_dow_thu: "Pa",
        cal_dow_fri: "Ju",
        cal_dow_sat: "Sh",
        cal_dow_sun: "Ya",

        // Application form
        btn_apply_form: "📝 Ariza topshirish",
        apply_modal_title: "Yashash uchun ariza — School 21 2026",
        apply_conditions_title: "Yotoqxona haqida",
        apply_cond_text: (
            "📍 Manzil: Qalandar ko'chasi, 24 (kampusdan 10 daqiqa). " +
            "❗ Qibray/O'rta Chirchiq aholisiga joy yo'q. " +
            "❗ 18+. ❗ 1 050 000 so'm/oy. ❗ Asosiy o'qitish piyonlari uchun."
        ),
        apply_label_date: "Ko'chib kirish sanasi *",
        apply_label_name: "Hujjatlardagi F.I.Sh. *",
        apply_label_login: "School 21 Login *",
        apply_label_comments: "Izoh (ixtiyoriy)",
        apply_label_consent: "Shaxsiy ma'lumotlarni qayta ishlashga roziman",
        apply_ph_date: "Masalan: 01.09.2026",
        apply_ph_name: "Familiya Ism Otasining ismi",
        apply_ph_login: "your_login",
        apply_ph_comments: "Qo'shimcha ma'lumot",
        apply_btn_submit: "✅ Arizani yuborish",
        apply_btn_cancel: "Bekor qilish",
        apply_success_msg: "✅ Ariza yuborildi! Qaror haqida xabar beramiz.",
        apply_err_required: "Iltimos barcha majburiy maydonlarni to'ldiring",
        apply_err_consent: "Shaxsiy ma'lumotlarni qayta ishlashga rozilik kerak",
        apply_required_note: "* Majburiy maydonlar",
    }
};

class I18nEngine {
    constructor() {
        this.currentLang = localStorage.getItem("dormitory_lang") || "ru";
    }

    setLanguage(lang) {
        if (I18N_TRANSLATIONS[lang]) {
            this.currentLang = lang;
            localStorage.setItem("dormitory_lang", lang);
            this.applyTranslations();
            if (window.onLanguageChange) {
                window.onLanguageChange(lang);
            }
        }
    }

    getLanguage() {
        return this.currentLang;
    }

    t(key, params = {}) {
        let dict = I18N_TRANSLATIONS[this.currentLang] || I18N_TRANSLATIONS.ru;
        let text = dict[key] || I18N_TRANSLATIONS.ru[key] || key;
        
        for (const [k, v] of Object.entries(params)) {
            text = text.replace(new RegExp(`\\{${k}\\}`, 'g'), v);
        }
        return text;
    }

    applyTranslations() {
        const elements = document.querySelectorAll("[data-i18n]");
        elements.forEach(el => {
            const key = el.getAttribute("data-i18n");
            const translation = this.t(key);
            if (el.tagName === "INPUT" && el.hasAttribute("placeholder")) {
                el.placeholder = translation;
            } else {
                el.textContent = translation;
            }
        });

        // Translate placeholder-only elements (inputs, textareas)
        const phElements = document.querySelectorAll("[data-i18n-placeholder]");
        phElements.forEach(el => {
            const key = el.getAttribute("data-i18n-placeholder");
            el.placeholder = this.t(key);
        });

        // Update select / button states if present
        const langBtns = document.querySelectorAll(".lang-btn");
        langBtns.forEach(btn => {
            if (btn.getAttribute("data-lang") === this.currentLang) {
                btn.classList.add("active");
            } else {
                btn.classList.remove("active");
            }
        });
    }
}

window.i18n = new I18nEngine();
document.addEventListener("DOMContentLoaded", () => {
    window.i18n.applyTranslations();
});
