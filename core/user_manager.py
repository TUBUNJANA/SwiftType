# core/user_manager.py
import os
import sys      # ✅ Added
import json
from datetime import datetime


class UserManager:
    def __init__(self, data_dir=None):
        """
        Choose a data directory that works in both dev mode and a
        PyInstaller‑onefile build.

        • When running from source (`python main.py`):
            ./data/users

        • When frozen (`swifttype.exe` from PyInstaller):
            <directory‑containing‑exe>/data/users
        """
        if data_dir is None:
            if getattr(sys, 'frozen', False):                 # ← if bundled
                base_dir = os.path.dirname(sys.executable)    # folder with the .exe
            else:                                             # ← normal dev run
                base_dir = os.path.abspath(".")
            data_dir = os.path.join(base_dir, "data", "users")

        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)

    # ---------- existing methods (unchanged) ----------

    def get_user_data_path(self, username):
        return os.path.join(self.data_dir, f"{username}.json")

    def load_user_data(self, username):
        path = self.get_user_data_path(username)
        if os.path.exists(path):
            with open(path, 'r') as file:
                return json.load(file)
        else:
            default_data = {
                "username": username,
                "history": []
            }
            with open(path, 'w') as file:
                json.dump(default_data, file, indent=4)
            return default_data

    def save_user_history(self, username, session_data):
        user_data = self.load_user_data(username)
        session_data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user_data["history"].append(session_data)
        with open(self.get_user_data_path(username), 'w') as file:
            json.dump(user_data, file, indent=4)

    def list_users(self):
        return [
            f[:-5] for f in os.listdir(self.data_dir)
            if f.endswith(".json")
        ]

    def delete_user(self, username):
        path = self.get_user_data_path(username)
        if os.path.exists(path):
            os.remove(path)

    def get_user_stats(self, username):
        user_data = self.load_user_data(username)
        data = user_data.get("history", [])
        if not data:
            return None

        total_wpm = sum(d['wpm'] for d in data)
        total_errors = sum(d['errors'] for d in data)
        total_accuracy = sum(d['accuracy'] for d in data)

        avg_wpm = total_wpm / len(data)
        avg_errors = total_errors / len(data)
        avg_accuracy = total_accuracy / len(data)

        return {
            'username': username,
            'avg_wpm': avg_wpm,
            'avg_errors': avg_errors,
            'avg_accuracy': avg_accuracy
        }

    def clear_user_history(self, username):
        path = self.get_user_data_path(username)
        if os.path.exists(path):
            with open(path, 'r') as file:
                data = json.load(file)
            data["history"] = []  # Clear history
            with open(path, 'w') as file:
                json.dump(data, file, indent=4)
