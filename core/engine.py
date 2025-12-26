import os, json, time
from datetime import datetime

class GuardianEngine:
    def __init__(self, data_dir="data/system"):
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)
        self.state_file = os.path.join(self.data_dir, "state.json")
        self.state = self._load_state()

    def _load_state(self):
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"risk_level": 1, "l4_active": False, "pause_until": 0, "last_update": ""}

    def save_state(self):
        self.state["last_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, indent=4)

    def set_risk(self, level, pause_hours=0):
        self.state["risk_level"] = level
        if level >= 4:
            self.state["l4_active"] = True
            self.state["pause_until"] = time.time() + (pause_hours * 3600)
        else:
            self.state["l4_active"] = False
        self.save_state()

    def is_paused(self):
        if self.state["l4_active"]:
            if time.time() < self.state["pause_until"]: return True
            self.state["l4_active"] = False # 自動解除 L4
            self.save_state()
        return False

    def can_attack(self):
        return self.state["risk_level"] < 3 and not self.is_paused()
