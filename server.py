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
        self.wfile.write(json.dumps(data, default=str, ensure_ascii=False).encode("utf-8"))

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

            elif path == "/api/db-status":
                status_info = db.get_db_status()
                self._send_json(status_info)
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

            elif path == "/api/applications":
                if not self._is_admin():
                    self._send_json({"error": "Требуется авторизация администратора"}, status=401)
                    return
                apps = db.get_all_applications()
                self._send_json(apps)
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

            elif path == "/api/rooms/duty-exempt":
                if not self._is_admin():
                    self._send_json({"error": "Требуются права администратора"}, status=401)
                    return
                body = self._read_body_json()
                room_number = str(body.get("room_number", "")).strip()
                is_duty_exempt = bool(body.get("is_duty_exempt", False))

                if not room_number:
                    self._send_json({"error": "Номер комнаты обязателен"}, status=400)
                    return

                db.set_room_duty_exempt(room_number, is_duty_exempt)
                excel_sync.export_db_to_excel(db.DB_PATH, EXCEL_PATH)
                msg = f"Комната {room_number} {'освобождена от дежурств' if is_duty_exempt else 'возвращена в график дежурств'}"
                self._send_json({
                    "success": True,
                    "room_number": room_number,
                    "is_duty_exempt": is_duty_exempt,
                    "message": msg
                })
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

            elif path == "/api/applications":
                body = self._read_body_json()
                full_name = body.get("full_name", "").strip()
                school21_login = body.get("school21_login", "").strip()
                move_in_date = body.get("move_in_date", "").strip()
                comments = body.get("comments", "").strip()

                if not full_name or not school21_login or not move_in_date:
                    self._send_json({"error": "Заполните все обязательные поля"}, status=400)
                    return

                app_id = db.add_application(
                    telegram_id=None, telegram_username=None,
                    full_name=full_name, school21_login=school21_login,
                    move_in_date=move_in_date, comments=comments, lang='ru'
                )

                # Notify bot admins about new web application
                try:
                    import telegram_bot
                    telegram_bot.notify_admins_new_application(
                        app_id, full_name, school21_login, move_in_date, comments,
                        {'username': None, 'id': None}
                    )
                except Exception as e:
                    print(f"[Server] Could not notify admins: {e}")

                self._send_json({"success": True, "app_id": app_id,
                                 "message": "Заявка успешно отправлена"})
                return

            elif path.startswith("/api/applications/") and path.endswith("/status"):
                if not self._is_admin():
                    self._send_json({"error": "Требуются права администратора"}, status=401)
                    return
                try:
                    app_id = int(path.split("/")[-2])
                except Exception:
                    self._send_json({"error": "Неверный ID"}, status=400)
                    return
                body = self._read_body_json()
                status = body.get("status", "pending")
                admin_comment = body.get("admin_comment", "")

                app = db.get_application_by_id(app_id)
                if not app:
                    self._send_json({"error": "Заявка не найдена"}, status=404)
                    return

                db.update_application_status(app_id, status, admin_comment)

                if status == "approved" and app.get('telegram_id'):
                    try:
                        import telegram_bot
                        db.add_resident(
                            full_name=app['full_name'],
                            nickname=app.get('school21_login', ''),
                            profile_url='', gender=app.get('gender') or 'M',
                            room_number=None, status='waiting'
                        )
                        comment_disp = admin_comment if admin_comment else 'Одобрено'
                        import bot_locales as bl
                        notify_text = bl.t('private', app['telegram_id'], 'app_approved_notify', comment=comment_disp)
                        telegram_bot.send_message(app['telegram_id'], notify_text)
                    except Exception as e:
                        print(f"[Server] Approval notify error: {e}")
                elif status == "rejected" and app.get('telegram_id'):
                    try:
                        import telegram_bot, bot_locales as bl
                        comment_disp = admin_comment if admin_comment else '-'
                        notify_text = bl.t('private', app['telegram_id'], 'app_rejected_notify', comment=comment_disp)
                        telegram_bot.send_message(app['telegram_id'], notify_text)
                    except Exception as e:
                        print(f"[Server] Rejection notify error: {e}")

                self._send_json({"success": True, "message": "Статус заявки обновлен"})
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

    handler = DormitoryHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Dormitory Production Server running at http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Server stopped.")

if __name__ == "__main__":
    run_server()

