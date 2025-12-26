import os
import json
import time
from datetime import datetime, timedelta

class GuardianEngine:
    def __init__(self, data_dir="data/system"):
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)
        self.state_file = os.path.join(self.data_dir, "state.json")
        self.state = self._load_state()

    def _load_state(self):
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                return json.load(f)
        return {
            "risk_level": 1,
            "l4_active": False,
            "pause_until": 0,
            "l3_events": [],
            "last_update": ""
        }

    def save_state(self):
        self.state["last_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=4)

    def update_risk(self, level, pause_hours=0):
        self.state["risk_level"] = level
        if level >= 4:
            self.state["l4_active"] = True
            self.state["pause_until"] = time.time() + (pause_hours * 3600)
        self.save_state()

    def is_paused(self):
        # 檢查 L4 是否還在冷卻期
        if self.state["l4_active"] and time.time() < self.state["pause_until"]:
            return True
        if self.state["l4_active"] and time.time() >= self.state["pause_until"]:
            self.state["l4_active"] = False # 自動解除
            self.save_state()
        return False

    def can_attack(self):
        # L3 警告或 L4 暫停時，不執行進攻 (不寫入歷史)
        return self.state["risk_level"] < 3 and not self.is_paused()
