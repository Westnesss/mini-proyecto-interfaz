import os
import psutil
import time
import datetime
from pymongo import MongoClient
import requests

class ProgramMonitor:
    def __init__(self, page_size=5):
        self.PROGRAMS_TO_LOG = []
        self.PREVIOUS_STATE = set()
        self.LOG_FILE_PATH = os.path.abspath("program_log.txt")

        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["program_monitor"]
        self.collection = self.db["program_logs"]

        self.ifttt_webhooks_key = "TU_CLAVE_DE_WEBHOOKS_DE_IFTTT"
        self.ifttt_event_name = "left_home"

        self.current_location = "Quito-Ecuador"
        self.notification_sent = False

        self.page_size = page_size

    def filter_inappropriate_programs(self, program_name):
        return program_name.lower() in [p.lower() for p in self.PROGRAMS_TO_LOG]

    def log_program_execution(self, program_name, username, action, cpu_percent, memory_percent):
        log_entry = {
            "timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "program_name": program_name,
            "username": username,
            "action": action,
            "cpu_percent": cpu_percent,
            "memory_percent": memory_percent
        }

        try:
            self.collection.insert_one(log_entry)
        except Exception as e:
            print(f"Error writing to MongoDB: {e}")

    def notify_left_home(self):
        webhook_url = f"https://maker.ifttt.com/trigger/{self.ifttt_event_name}/with/key/{self.ifttt_webhooks_key}"
        requests.post(webhook_url)
        print(f"Notificación enviada al salir de Quito a las {datetime.datetime.now()}.")

    def left_home_condition(self):
        self.current_location = "Fuera de Quito"
        if not self.notification_sent and self.current_location.lower() != "quito-ecuador":
            print(f"Cambio de ubicación a: {self.current_location}")
            self.notification_sent = True
            return True

        return False

    def monitor_programs(self):
        processes = list(psutil.process_iter(["name", "username", "cpu_percent", "memory_percent"]))

        for i in range(0, len(processes), self.page_size):
            page = processes[i:i + self.page_size]
            for process in page:
                program_name = process.info.get("name", "")
                username = process.info.get("username", "")
                cpu_percent = process.info.get("cpu_percent", 0.0)
                memory_percent = process.info.get("memory_percent", 0.0)

                if self.filter_inappropriate_programs(program_name):
                    if program_name.lower() not in self.PREVIOUS_STATE:
                        self.log_program_execution(program_name, username, "started", cpu_percent, memory_percent)
                        self.PREVIOUS_STATE.add(program_name.lower())
                    else:
                        self.log_program_execution(program_name, username, "running", cpu_percent, memory_percent)

        if self.left_home_condition():
            self.notify_left_home()

        time.sleep(10)

    def start_monitoring(self):
        try:
            while True:
                self.monitor_programs()
        except KeyboardInterrupt:
            print("Monitoring stopped.")
            self.client.close()

if __name__ == "__main__":
    program_monitor = ProgramMonitor(page_size=5)
    program_monitor.start_monitoring()
