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
        duty_today_card: "Дежурные на сегодня ({date})",
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
        footer_copyright: "Система Управления Общежитием v2.0 • Все права защищены"
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

        duty_sec_title: "Kitchen Duty Schedule (7th Floor)",
        duty_today_card: "Today's Duty ({date})",
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

        footer_copyright: "Dormitory Management System v2.0 • All rights reserved"
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

        duty_sec_title: "Oshxona navbatchilik jadvali (7-Qavat)",
        duty_today_card: "Bugungi navbatchilar ({date})",
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

        footer_copyright: "Yotoqxona Boshqaruv Tizimi v2.0 • Barcha huquqlar himoyalangan"
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
