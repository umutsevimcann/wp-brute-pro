"""State tracking — tried passwords, resume support"""
import json
import os
from datetime import datetime


class Tracker:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.state_file = os.path.join(output_dir, "state.json")
        self.tried_file = os.path.join(output_dir, "tried.txt")
        self.state = self._load_state()
        self.tried = self._load_tried()

    def _load_state(self):
        if os.path.exists(self.state_file):
            with open(self.state_file, "r") as f:
                return json.load(f)
        return {
            "target": None,
            "started": datetime.now().isoformat(),
            "users": {},
            "total_tried": 0,
            "total_generated": 0,
            "found": [],
        }

    def _load_tried(self):
        tried = set()
        if os.path.exists(self.tried_file):
            with open(self.tried_file, "r", encoding="utf-8") as f:
                for line in f:
                    tried.add(line.strip())
        return tried

    def set_target(self, url):
        self.state["target"] = url

    def is_tried(self, username, password):
        return f"{username}:{password}" in self.tried

    def mark_tried(self, username, passwords):
        with open(self.tried_file, "a", encoding="utf-8") as f:
            for pwd in passwords:
                key = f"{username}:{pwd}"
                if key not in self.tried:
                    self.tried.add(key)
                    f.write(key + "\n")
                    self.state["total_tried"] += 1

    def filter_new(self, username, passwords):
        return [p for p in passwords if f"{username}:{p}" not in self.tried]

    def mark_found(self, username, password):
        entry = {"username": username, "password": password, "time": datetime.now().isoformat()}
        self.state["found"].append(entry)
        found_file = os.path.join(self.output_dir, "found.txt")
        with open(found_file, "a") as f:
            f.write(f"{username}:{password}\n")
        self.save_state()

    def update_user(self, username, tried_count, status="in_progress"):
        if username not in self.state["users"]:
            self.state["users"][username] = {"tried": 0, "status": "pending"}
        self.state["users"][username]["tried"] = tried_count
        self.state["users"][username]["status"] = status

    def set_generated(self, count):
        self.state["total_generated"] = count

    def save_state(self):
        with open(self.state_file, "w") as f:
            json.dump(self.state, f, indent=2, ensure_ascii=False)

    def get_tried_count(self, username=None):
        if username:
            return sum(1 for t in self.tried if t.startswith(f"{username}:"))
        return len(self.tried)

    def summary(self):
        return (f"  Toplam denenen: {self.state['total_tried']}\n"
                f"  Toplam uretilen: {self.state['total_generated']}\n"
                f"  Bulunan: {len(self.state['found'])}")
