import sqlite3
import os
import datetime
import calendar

DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

DB_DIR = os.path.join(os.path.dirname(__file__), "database")
DB_PATH = os.path.join(DB_DIR, "dormitory.db")


class DictRow(dict):
    """Dictionary subclass supporting column name and index access."""
    def __getitem__(self, key):
        if isinstance(key, int):
            return list(self.values())[key]
        return super().__getitem__(key)


class UnifiedCursor:
    def __init__(self, cursor, is_postgres=False):
        self.cursor = cursor
        self.is_postgres = is_postgres
        self.lastrowid = None

    def execute(self, sql, params=None):
        if self.is_postgres:
            # Convert SQLite placeholders (?) to PostgreSQL placeholders (%s)
            sql = sql.replace('?', '%s')
            # Convert SQLite AUTOINCREMENT to Postgres SERIAL syntax
            sql = sql.replace('INTEGER PRIMARY KEY AUTOINCREMENT', 'SERIAL PRIMARY KEY')
            
            is_insert = sql.strip().upper().startswith('INSERT')
            if is_insert and 'RETURNING' not in sql.upper() and 'SELECT' not in sql.upper():
                try:
                    sql_ret = sql.rstrip('; ') + ' RETURNING id'
                    if params:
                        self.cursor.execute(sql_ret, params)
                    else:
                        self.cursor.execute(sql_ret)
                    row = self.cursor.fetchone()
                    if row:
                        if isinstance(row, dict):
                            self.lastrowid = row.get('id', list(row.values())[0])
                        elif hasattr(row, '__getitem__'):
                            self.lastrowid = row[0]
                    return self
                except Exception:
                    pass

        if params:
            self.cursor.execute(sql, params)
        else:
            self.cursor.execute(sql)

        if not self.is_postgres:
            self.lastrowid = self.cursor.lastrowid
        return self

    def fetchone(self):
        row = self.cursor.fetchone()
        if row is None:
            return None
        if isinstance(row, dict):
            return DictRow(row)
        if hasattr(row, 'keys'):
            return DictRow({k: row[k] for k in row.keys()})
        if isinstance(row, tuple):
            colnames = [desc[0] for desc in self.cursor.description]
            return DictRow(dict(zip(colnames, row)))
        return row

    def fetchall(self):
        rows = self.cursor.fetchall()
        if not rows:
            return []
        res = []
        for r in rows:
            if isinstance(r, dict):
                res.append(DictRow(r))
            elif hasattr(r, 'keys'):
                res.append(DictRow({k: r[k] for k in r.keys()}))
            elif isinstance(r, tuple):
                colnames = [desc[0] for desc in self.cursor.description]
                res.append(DictRow(dict(zip(colnames, r))))
            else:
                res.append(r)
        return res


class UnifiedConnection:
    def __init__(self, conn, is_postgres=False):
        self.conn = conn
        self.is_postgres = is_postgres

    def cursor(self):
        if self.is_postgres:
            import psycopg2.extras
            cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        else:
            cur = self.conn.cursor()
        return UnifiedCursor(cur, is_postgres=self.is_postgres)

    def execute(self, sql, params=None):
        cur = self.cursor()
        cur.execute(sql, params)
        return cur

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()


def get_db_connection():
    if DATABASE_URL:
        try:
            import psycopg2
            pg_conn = psycopg2.connect(DATABASE_URL)
            return UnifiedConnection(pg_conn, is_postgres=True)
        except Exception as e:
            print(f"[DB Warning] Could not connect to PostgreSQL: {e}. Falling back to SQLite.")

    os.makedirs(DB_DIR, exist_ok=True)
    sqlite_conn = sqlite3.connect(DB_PATH)
    sqlite_conn.row_factory = sqlite3.Row
    return UnifiedConnection(sqlite_conn, is_postgres=False)

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rooms (
        room_number TEXT PRIMARY KEY,
        floor INTEGER NOT NULL,
        gender TEXT NOT NULL,
        capacity INTEGER NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS residents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        num_code INTEGER,
        full_name TEXT NOT NULL,
        nickname TEXT,
        profile_url TEXT,
        gender TEXT NOT NULL,
        room_number TEXT,
        status TEXT NOT NULL DEFAULT 'permanent',
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (room_number) REFERENCES rooms (room_number)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS activity_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        action TEXT NOT NULL,
        details TEXT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS duty_schedule (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        duty_date TEXT NOT NULL,
        floor INTEGER NOT NULL DEFAULT 7,
        room_number TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'pending',
        assigned_by TEXT NOT NULL DEFAULT 'auto',
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(duty_date, floor)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bot_user_settings (
        telegram_id INTEGER PRIMARY KEY,
        language TEXT NOT NULL DEFAULT 'ru'
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS housing_applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER,
        telegram_username TEXT,
        full_name TEXT NOT NULL,
        school21_login TEXT NOT NULL,
        move_in_date TEXT NOT NULL,
        gender TEXT,
        comments TEXT,
        consent INTEGER DEFAULT 1,
        lang TEXT DEFAULT 'ru',
        status TEXT NOT NULL DEFAULT 'pending',
        admin_comment TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)


    # Populate default rooms if empty
    cursor.execute("SELECT COUNT(*) as count FROM rooms")
    if cursor.fetchone()["count"] == 0:
        for r in range(1, 15):
            r_num = f"2{r:02d}"
            cap = 6 if r in (13, 14) else 4
            cursor.execute("INSERT INTO rooms (room_number, floor, gender, capacity) VALUES (?, ?, ?, ?)",
                           (r_num, 2, "F", cap))

        for r in range(1, 15):
            r_num = f"7{r:02d}"
            cap = 6 if r in (13, 14) else 4
            cursor.execute("INSERT INTO rooms (room_number, floor, gender, capacity) VALUES (?, ?, ?, ?)",
                           (r_num, 7, "M", cap))

    # Seed Initial Residents if table is empty
    cursor.execute("SELECT COUNT(*) as count FROM residents")
    if cursor.fetchone()["count"] == 0:
        initial_residents = [
            (23, "Mingbayeva Diyoraxon Baxtiyorjon Qizi", "signusda", "", "F", "206", "permanent"),
            (24, "Ibragimova Gulisa Nuriddin qizi", "donelbol", "", "F", "206", "permanent"),
            (25, "Olimjonova Robiyaxon Shavkat Qizi", "detraebo", "", "F", "206", "permanent"),
            (26, "Abduqodirova Mohinur Shavkat qizi", "viktorer", "", "F", "207", "permanent"),
            (27, "Shoyakubova Ruxshona Suxrob Qizi", "thaliach", "", "F", "207", "permanent"),
            (1, "Tohirov Javlonbek Kamolbek o'g'li", "brianabr", "", "M", "701", "permanent"),
            (2, "Amanov Sardorbek Alisher og'l", "imyankat", "https://platform.21-school.ru/admin/profile/imyankat", "M", "701", "permanent"),
            (3, "Farxodov Shohruhbek Farrux o'g'li", "helaenat", "", "M", "701", "permanent"),
            (4, "Xamidov Javohir Mo'minjon o'g'li", "harmacor", "https://platform.21-school.ru/admin/profile/harmacor", "M", "701", "permanent"),
            (5, "Sulaymonov Sohibjon Adhamjon o'g'li", "plankcla", "", "M", "702", "permanent"),
            (6, "Quddusov Iskandar Alisher O'g'li", "mauveken", "https://platform.21-school.ru/admin/profile/mauveken", "M", "702", "permanent"),
            (7, "Maxmudov Sharifjon Shuxrat Ogli", "tamicari", "https://platform.21-school.ru/admin/profile/keturahp", "M", "702", "permanent"),
            (8, "Suyunov Sanjar Muhammad og'li", "mireyase", "", "M", "703", "permanent"),
            (9, "O'ngarov Berdiyor Qilichbek o'g'li", "foetidpa", "", "M", "703", "permanent"),
            (10, "Xolmo'minov Baxtiyor Abdugappar o'g'li", "terisada", "", "M", "703", "permanent"),
            (None, "Бухарский Макс Бахадырович", "14 kunlik", "", "M", "703", "14_days"),
            (11, "Rejavaliyev Boymirza Dilshodjon o'g'li", "antlionb", "", "M", "704", "permanent"),
            (12, "Eraliyev Behruzbek Muhammadali o'g'li", "timeonme", "", "M", "704", "permanent"),
            (13, "Raimqulov O'razali Xakim O'g'li", "loretten", "", "M", "704", "permanent"),
            (14, "Rasulmatov Diyorbek Dilmurod O'g'li", "pennygar", "", "M", "704", "permanent"),
            (15, "Sanayev Rustam Ismailovich", "deloissy", "", "M", "705", "permanent"),
            (16, "Djumanov Sharyarbek Tolibayevich", "olinmorg", "", "M", "705", "permanent"),
            (17, "Amirov Shahzod Akmal oʻgʻli", "suziecar", "", "M", "705", "permanent"),
            (18, "Samatov Elfat Rinatovich", "moaneyin", "", "M", "705", "permanent"),
            (19, "Abdullayev Komronbek Anvar o'g'li", "papererr", "", "M", "706", "permanent"),
            (20, "Maxsudov Muhammadyusuf Rasuljon o'g'li", "donitafr", "", "M", "706", "permanent"),
            (21, "Turg'unbayev Daulet Muxtor O'g'li", "alvinamy", "", "M", "706", "permanent"),
            (22, "Kenesbaev Begzad Akilbek Uli", "stockcol", "https://platform.21-school.ru/admin/profile/stockcol", "M", "706", "permanent"),
            (28, "Xamdamov Ayyubxon Akromjon o'g'li", "", "", "M", "709", "permanent"),
            (29, "Yuldashev Timur Bakhodirovich", "nakitave", "", "M", "711", "permanent"),
            (30, "Shaxrulloyev Shohjahon Sherali O'g'li", "marissaj", "", "M", "712", "permanent"),
            (31, "Sim Andrey Aleksandrovich", "merilyni", "", "M", "712", "permanent"),
            (32, "Abduraxmonov Abdujabbor Abdumavlon O'g'li", "ninfacat", "", "M", "712", "permanent"),
            (33, "Oybekov Asilbek Otabek O'g'li", "kaminome", "", "M", "714", "permanent"),
            (34, "Qirgizboyev Nurulloh Muhammadjon Ogli", "gladdend", "", "M", "714", "permanent"),
            (None, "Shamsiyev Shaxzod Husniddin O'g'li", "14 kunlik", "", "M", "714", "14_days"),
            (35, "Qudratov Shaxbos Avazbek O'g'li", "patrinaq", "", "M", None, "waiting")
        ]

        for num_code, full_name, nick, p_url, g, rm, st in initial_residents:
            cursor.execute("""
            INSERT INTO residents (num_code, full_name, nickname, profile_url, gender, room_number, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (num_code, full_name, nick, p_url, g, rm, st))

        log_activity(conn, "Инициализация системы", "База данных успешно создана")

    conn.commit()
    conn.close()

def clear_old_duty_test_data():
    """Clear duty schedule table so sequence is 100% clean auto-calculated."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM duty_schedule")
    conn.commit()
    conn.close()

def log_activity(conn, action, details):
    conn.execute("INSERT INTO activity_logs (action, details) VALUES (?, ?)", (action, details))

# --- Stats & Basic Data ---
def get_stats():
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) as total FROM residents WHERE status != 'evicted'")
    total_residents = c.fetchone()["total"]

    c.execute("SELECT COUNT(*) as floor2 FROM residents WHERE room_number LIKE '2%' AND status != 'evicted'")
    floor2_count = c.fetchone()["floor2"]

    c.execute("SELECT COUNT(*) as floor7 FROM residents WHERE room_number LIKE '7%' AND status != 'evicted'")
    floor7_count = c.fetchone()["floor7"]

    c.execute("SELECT COUNT(*) as temp FROM residents WHERE status = '14_days'")
    temp_count = c.fetchone()["temp"]

    c.execute("SELECT COUNT(*) as waiting FROM residents WHERE (status = 'waiting' OR room_number IS NULL OR room_number = '') AND status != 'evicted'")
    waiting_count = c.fetchone()["waiting"]

    c.execute("SELECT SUM(capacity) as total_cap FROM rooms")
    total_capacity = c.fetchone()["total_cap"]

    conn.close()
    return {
        "total_residents": total_residents,
        "floor2_count": floor2_count,
        "floor7_count": floor7_count,
        "temp_count": temp_count,
        "waiting_count": waiting_count,
        "total_capacity": total_capacity,
        "free_beds": total_capacity - (total_residents - waiting_count)
    }

def get_floors_data():
    conn = get_db_connection()
    c = conn.cursor()

    c.execute("SELECT * FROM rooms ORDER BY floor ASC, room_number ASC")
    rooms = [dict(r) for r in c.fetchall()]

    c.execute("SELECT * FROM residents WHERE status != 'evicted'")
    residents = [dict(r) for r in c.fetchall()]
    conn.close()

    rooms_map = {rm["room_number"]: {**rm, "residents": []} for rm in rooms}

    unassigned = []
    for res in residents:
        r_num = res["room_number"]
        if r_num and r_num in rooms_map:
            rooms_map[r_num]["residents"].append(res)
        else:
            unassigned.append(res)

    floors = {}
    for rm in rooms:
        fl = rm["floor"]
        if fl not in floors:
            floors[fl] = []
        floors[fl].append(rooms_map[rm["room_number"]])

    return {
        "floors": floors,
        "unassigned": unassigned
    }

def add_resident(full_name, nickname, profile_url, gender, room_number, status, notes=""):
    conn = get_db_connection()
    c = conn.cursor()
    if room_number == "": room_number = None

    c.execute("""
    INSERT INTO residents (full_name, nickname, profile_url, gender, room_number, status, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (full_name, nickname, profile_url, gender, room_number, status, notes))
    
    res_id = c.lastrowid
    rm_str = f"комнату {room_number}" if room_number else "список ожидания"
    log_activity(conn, "Заселение жильца", f"Добавлен жилец {full_name} в {rm_str}")

    conn.commit()
    conn.close()
    return res_id

def update_resident(res_id, full_name, nickname, profile_url, gender, room_number, status, notes=""):
    conn = get_db_connection()
    c = conn.cursor()
    if room_number == "": room_number = None

    c.execute("SELECT * FROM residents WHERE id = ?", (res_id,))
    prev = c.fetchone()

    c.execute("""
    UPDATE residents
    SET full_name = ?, nickname = ?, profile_url = ?, gender = ?, room_number = ?, status = ?, notes = ?
    WHERE id = ?
    """, (full_name, nickname, profile_url, gender, room_number, status, notes, res_id))

    details = f"Обновлен жилец ID #{res_id} ({full_name})."
    if prev and prev["room_number"] != room_number:
        details += f" Переселен: {prev['room_number']} -> {room_number}."
    log_activity(conn, "Изменение жильца", details)

    conn.commit()
    conn.close()
    return True

def evict_resident(res_id):
    conn = get_db_connection()
    c = conn.cursor()

    c.execute("SELECT full_name, room_number FROM residents WHERE id = ?", (res_id,))
    res = c.fetchone()
    if res:
        c.execute("UPDATE residents SET status = 'evicted', room_number = NULL WHERE id = ?", (res_id,))
        log_activity(conn, "Выселение жильца", f"Жилец {res['full_name']} выселен из комнаты {res['room_number']}")

    conn.commit()
    conn.close()
    return True

def get_activity_logs(limit=50):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM activity_logs ORDER BY timestamp DESC LIMIT ?", (limit,))
    logs = [dict(r) for r in c.fetchall()]
    conn.close()
    return logs

# --- DUTY SCHEDULE LOGIC (FLOOR 7 ONLY, ANCHORED TO ROOM 705 ON 2026-08-07) ---

def get_active_male_rooms(conn):
    """Get sorted list of occupied male rooms on Floor 7: [701, 702, 703, 704, 705, 706, 709, 711, 712, 714]."""
    c = conn.cursor()
    c.execute("""
    SELECT rm.room_number, COUNT(r.id) as res_count
    FROM rooms rm
    JOIN residents r ON r.room_number = rm.room_number
    WHERE rm.floor = 7 AND r.status != 'evicted'
    GROUP BY rm.room_number
    HAVING res_count > 0
    ORDER BY rm.room_number ASC
    """)
    rooms = [r["room_number"] for r in c.fetchall()]
    if not rooms:
        rooms = ["701", "702", "703", "704", "705", "706", "709", "711", "712", "714"]
    return rooms

def get_duty_schedule_for_month(year, month, floor=7):
    """
    Returns Floor 7 duty schedule.
    Sequence:
      2026-08-07 (Today) -> Room 705
      2026-08-08          -> Room 706
      2026-08-09          -> Room 709
      2026-08-10          -> Room 711
      2026-08-11          -> Room 712
      2026-08-12          -> Room 714
      2026-08-13          -> Room 701
      2026-08-14          -> Room 702
      2026-08-15          -> Room 703
      2026-08-16          -> Room 704
      2026-08-17          -> Room 705 ...
    """
    conn = get_db_connection()
    c = conn.cursor()

    active_rooms = get_active_male_rooms(conn)
    
    # Anchor: 2026-08-07 -> Room 705
    anchor_date = datetime.date(2026, 8, 7)
    anchor_room = "705"
    anchor_idx = active_rooms.index(anchor_room) if anchor_room in active_rooms else 0

    num_days = calendar.monthrange(year, month)[1]

    # Explicit manual DB entries
    start_date = f"{year:04d}-{month:02d}-01"
    end_date = f"{year:04d}-{month:02d}-{num_days:02d}"

    c.execute("""
    SELECT * FROM duty_schedule 
    WHERE floor = 7 AND duty_date >= ? AND duty_date <= ?
    """, (start_date, end_date))
    
    explicit_entries = {row["duty_date"]: dict(row) for row in c.fetchall()}

    fl_schedule = []
    for day in range(1, num_days + 1):
        date_str = f"{year:04d}-{month:02d}-{day:02d}"
        dt = datetime.date(year, month, day)

        if date_str in explicit_entries:
            entry = explicit_entries[date_str]
            room_num = entry["room_number"]
            status = entry["status"]
            assigned_by = entry["assigned_by"]
            notes = entry["notes"] or ""
        else:
            # Auto rotation relative to 2026-08-07 (705)
            days_diff = (dt - anchor_date).days
            room_idx = (anchor_idx + days_diff) % len(active_rooms)
            room_num = active_rooms[room_idx]
            status = "pending"
            assigned_by = "auto"
            notes = ""

        # Fetch current residents of this room
        c.execute("""
        SELECT full_name, nickname, status FROM residents
        WHERE room_number = ? AND status != 'evicted'
        """, (room_num,))
        residents = [dict(r) for r in c.fetchall()]

        fl_schedule.append({
            "date": date_str,
            "day": day,
            "day_of_week": dt.strftime("%a"),
            "floor": 7,
            "room_number": room_num,
            "status": status,
            "assigned_by": assigned_by,
            "notes": notes,
            "residents": residents
        })

    conn.close()
    return {7: fl_schedule}

def set_manual_duty(duty_date, floor, room_number, status="pending", notes=""):
    conn = get_db_connection()
    c = conn.cursor()

    c.execute("""
    INSERT INTO duty_schedule (duty_date, floor, room_number, status, assigned_by, notes)
    VALUES (?, 7, ?, ?, 'manual', ?)
    ON CONFLICT(duty_date, floor) DO UPDATE SET
        room_number = excluded.room_number,
        status = excluded.status,
        assigned_by = 'manual',
        notes = excluded.notes
    """, (duty_date, room_number, status, notes))

    log_activity(conn, "Изменение дежурства", f"Дежурство на {duty_date} (7 Этаж) назначено на комнату {room_number}")

    conn.commit()
    conn.close()
    return True

def mark_duty_status(duty_date, floor, status, notes=""):
    conn = get_db_connection()
    c = conn.cursor()

    c.execute("SELECT room_number FROM duty_schedule WHERE duty_date = ? AND floor = 7", (duty_date,))
    row = c.fetchone()
    
    if not row:
        dt = datetime.datetime.strptime(duty_date, "%Y-%m-%d").date()
        today_data = get_duty_schedule_for_month(dt.year, dt.month, floor=7)
        day_items = today_data.get(7, [])
        target_item = next((item for item in day_items if item["date"] == duty_date), None)
        room_num = target_item["room_number"] if target_item else "705"
    else:
        room_num = row["room_number"]

    c.execute("""
    INSERT INTO duty_schedule (duty_date, floor, room_number, status, assigned_by, notes)
    VALUES (?, 7, ?, ?, 'manual', ?)
    ON CONFLICT(duty_date, floor) DO UPDATE SET
        status = excluded.status,
        notes = excluded.notes
    """, (duty_date, room_num, status, notes))

    log_activity(conn, "Статус дежурства", f"Дежурство {duty_date} (Комната {room_num}) помечено как '{status}'")

    conn.commit()
    conn.close()
    return True

def get_today_duty():
    now = datetime.date.today()
    today_str = now.strftime("%Y-%m-%d")
    schedule = get_duty_schedule_for_month(now.year, now.month, floor=7)
    
    day_items = schedule.get(7, [])
    today_item = next((item for item in day_items if item["date"] == today_str), None)
    return {7: today_item}

def get_user_language(telegram_id):
    if not telegram_id:
        return 'ru'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT language FROM bot_user_settings WHERE telegram_id = ?", (telegram_id,))
    row = c.fetchone()
    conn.close()
    if row and row["language"]:
        return row["language"]
    return 'ru'

def set_user_language(telegram_id, language):
    if not telegram_id or language not in ('ru', 'en', 'uz'):
        return False
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
    INSERT INTO bot_user_settings (telegram_id, language)
    VALUES (?, ?)
    ON CONFLICT(telegram_id) DO UPDATE SET language = excluded.language
    """, (telegram_id, language))
    conn.commit()
    conn.close()
    return True

# ─────────────── Housing Applications ───────────────

def add_application(telegram_id, telegram_username, full_name, school21_login,
                    move_in_date, comments='', consent=1, lang='ru'):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
    INSERT INTO housing_applications
        (telegram_id, telegram_username, full_name, school21_login,
         move_in_date, comments, consent, lang, status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'pending')
    """, (telegram_id, telegram_username, full_name, school21_login,
           move_in_date, comments, consent, lang))
    app_id = c.lastrowid
    conn.commit()
    conn.close()
    return app_id

def get_all_applications(status=None):
    conn = get_db_connection()
    c = conn.cursor()
    if status:
        c.execute("SELECT * FROM housing_applications WHERE status = ? ORDER BY created_at DESC", (status,))
    else:
        c.execute("SELECT * FROM housing_applications ORDER BY created_at DESC")
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

def get_application_by_id(app_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM housing_applications WHERE id = ?", (app_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

def update_application_status(app_id, status, admin_comment=''):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
    UPDATE housing_applications
    SET status = ?, admin_comment = ?
    WHERE id = ?
    """, (status, admin_comment, app_id))
    conn.commit()
    conn.close()
    return True

if __name__ == "__main__":
    init_db()
    clear_old_duty_test_data()
    print("Database initialized & duty schedule cleared!")
