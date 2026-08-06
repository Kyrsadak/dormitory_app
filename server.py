import http.server
import socketserver
import json
import urllib.parse
import os
import sys
import io
import datetime

sys.path.append(os.path.dirname(__file__))
import db
import excel_sync

PORT = 8080
PUBLIC_DIR = os.path.join(os.path.dirname(__file__), "public")
EXCEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Лист Microsoft Excel.xlsx"))

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "yNjA7371OSuooFBm")
ADMIN_TOKEN = "admin_secret_token_dormitory_2026"

class DormitoryHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PUBLIC_DIR, **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-Admin-Token")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def _read_body_json(self):
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length == 0:
            return {}
        body = self.rfile.read(content_length).decode('utf-8')
        return json.loads(body)

    def _is_admin(self):
        token = self.headers.get("X-Admin-Token", "")
        if not token and "Authorization" in self.headers:
            auth = self.headers.get("Authorization", "")
            if auth.startswith("Bearer "):
                token = auth[7:]
        return token == ADMIN_TOKEN

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-Admin-Token")
        self.end_headers()

    def do_GET(self):
        try:
            parsed_url = urllib.parse.urlparse(self.path)
            path = parsed_url.path
            query_params = urllib.parse.parse_qs(parsed_url.query)

            if path == "/api/stats":
                stats = db.get_stats()
                self._send_json(stats)
                return

            elif path == "/api/floors":
                data = db.get_floors_data()
                self._send_json(data)
                return

            elif path == "/api/logs":
                if not self._is_admin():
                    self._send_json({"error": "Требуется авторизация администратора"}, status=401)
                    return
                logs = db.get_activity_logs()
                self._send_json(logs)
                return

            elif path == "/api/duty/today":
                today_duty = db.get_today_duty()
                self._send_json(today_duty)
                return

            elif path == "/api/duty/calendar":
                now = datetime.date.today()
                year = int(query_params.get("year", [now.year])[0])
                month = int(query_params.get("month", [now.month])[0])
                floor = int(query_params.get("floor", [7])[0])

                schedule = db.get_duty_schedule_for_month(year, month, floor=floor)
                self._send_json(schedule)
                return

            elif path == "/api/download-excel":
                wb = excel_sync.generate_excel_workbook(db.DB_PATH)
                output = io.BytesIO()
                wb.save(output)
                excel_bytes = output.getvalue()

                self.send_response(200)
                self.send_header("Content-Type", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                self.send_header("Content-Disposition", 'attachment; filename="Dormitory_Report.xlsx"')
                self.send_header("Content-Length", str(len(excel_bytes)))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(excel_bytes)
                return

            elif path == "/" or path == "":
                self.path = "/index.html"

            return super().do_GET()
        except Exception as e:
            print("Error in do_GET:", e)
            self._send_json({"error": str(e)}, status=500)

    def do_POST(self):
        try:
            parsed_url = urllib.parse.urlparse(self.path)
            path = parsed_url.path

            if path == "/api/admin/login":
                body = self._read_body_json()
                password = body.get("password", "").strip()

                if password == ADMIN_PASSWORD:
                    self._send_json({"success": True, "token": ADMIN_TOKEN, "message": "Авторизация успешна"})
                else:
                    self._send_json({"success": False, "error": "Неверный пароль администратора"}, status=401)
                return

            elif path == "/api/residents":
                if not self._is_admin():
                    self._send_json({"error": "Требуются права администратора"}, status=401)
                    return
                body = self._read_body_json()
                full_name = body.get("full_name", "").strip()
                nickname = body.get("nickname", "").strip()
                profile_url = body.get("profile_url", "").strip()
                gender = body.get("gender", "M")
                room_number = body.get("room_number", "")
                status = body.get("status", "permanent")
                notes = body.get("notes", "").strip()

                if not full_name:
                    self._send_json({"error": "ФИО обязательно к заполнению"}, status=400)
                    return

                res_id = db.add_resident(full_name, nickname, profile_url, gender, room_number, status, notes)
                excel_sync.export_db_to_excel(db.DB_PATH, EXCEL_PATH)
                self._send_json({"success": True, "id": res_id, "message": "Жилец успешно добавлен"})
                return

            elif path == "/api/duty/assign":
                if not self._is_admin():
                    self._send_json({"error": "Требуются права администратора"}, status=401)
                    return
                body = self._read_body_json()
                duty_date = body.get("duty_date")
                floor = 7
                room_number = str(body.get("room_number")).strip()
                status = body.get("status", "pending")
                notes = body.get("notes", "").strip()

                db.set_manual_duty(duty_date, floor, room_number, status, notes)
                excel_sync.export_db_to_excel(db.DB_PATH, EXCEL_PATH)
                self._send_json({"success": True, "message": "Дежурство успешно переназначено"})
                return

            elif path == "/api/duty/status":
                # Duty completion is allowed for admin AND via telegram bot / residents
                body = self._read_body_json()
                duty_date = body.get("duty_date")
                floor = 7
                status = body.get("status", "completed")
                notes = body.get("notes", "").strip()

                db.mark_duty_status(duty_date, floor, status, notes)
                excel_sync.export_db_to_excel(db.DB_PATH, EXCEL_PATH)
                self._send_json({"success": True, "message": "Статус дежурства обновлен"})
                return

            elif path == "/api/export-excel":
                success, msg = excel_sync.export_db_to_excel(db.DB_PATH, EXCEL_PATH)
                self._send_json({"success": success, "message": msg})
                return

            self._send_json({"error": "Not Found"}, status=404)
        except Exception as e:
            print("Error in do_POST:", e)
            self._send_json({"error": str(e)}, status=500)

    def do_PUT(self):
        try:
            parsed_url = urllib.parse.urlparse(self.path)
            path = parsed_url.path

            if path.startswith("/api/residents/"):
                if not self._is_admin():
                    self._send_json({"error": "Требуются права администратора"}, status=401)
                    return
                res_id = int(path.split("/")[-1])
                body = self._read_body_json()

                full_name = body.get("full_name", "").strip()
                nickname = body.get("nickname", "").strip()
                profile_url = body.get("profile_url", "").strip()
                gender = body.get("gender", "M")
                room_number = body.get("room_number", "")
                status = body.get("status", "permanent")
                notes = body.get("notes", "").strip()

                db.update_resident(res_id, full_name, nickname, profile_url, gender, room_number, status, notes)
                excel_sync.export_db_to_excel(db.DB_PATH, EXCEL_PATH)
                self._send_json({"success": True, "message": "Данные жильца обновлены"})
                return

            self._send_json({"error": "Not Found"}, status=404)
        except Exception as e:
            print("Error in do_PUT:", e)
            self._send_json({"error": str(e)}, status=500)

    def do_DELETE(self):
        try:
            parsed_url = urllib.parse.urlparse(self.path)
            path = parsed_url.path

            if path.startswith("/api/residents/"):
                if not self._is_admin():
                    self._send_json({"error": "Требуются права администратора"}, status=401)
                    return
                res_id = int(path.split("/")[-1])
                db.evict_resident(res_id)
                excel_sync.export_db_to_excel(db.DB_PATH, EXCEL_PATH)
                self._send_json({"success": True, "message": "Жилец выселен"})
                return

            self._send_json({"error": "Not Found"}, status=404)
        except Exception as e:
            print("Error in do_DELETE:", e)
            self._send_json({"error": str(e)}, status=500)

import telegram_bot

def run_server():
    db.init_db()
    excel_sync.export_db_to_excel(db.DB_PATH, EXCEL_PATH)
    
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if bot_token:
        telegram_bot.start_bot_in_background(bot_token)
    elif os.path.exists(telegram_bot.CONFIG_FILE):
        cfg = telegram_bot.load_config()
        if cfg.get("chat_id"):
            telegram_bot.start_bot_in_background()

    handler = DormitoryHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Dormitory Production Server running at http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Server stopped.")

if __name__ == "__main__":
    run_server()

