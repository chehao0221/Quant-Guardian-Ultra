import os
import json
import time
from datetime import datetime

class GuardianEngine:
    def __init__(self, data_dir="data/system"):
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)
        self.state_file = os.path.join(self.data_dir, "state.json")
        self.state = self._load_state()

    def _load_state(self):
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            except: pass
        return {
            "risk_level": 1,
            "l4_active": False,
            "pause_until": 0,
            "last_update": ""
        }

    def save_state(self):
        self.state["last_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.state_file, 'w') as f:
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
            if time.time() < self.state["pause_until"]:
                return True
            else:
                self.state["l4_active"] = False
                self.state["risk_level"] = 1
                self.save_state()
        return False

    def can_attack(self):
        # L3 以上不允許寫入正式交易歷史，L4 則完全停止
        return self.state["risk_level"] < 3 and not self.is_paused()
