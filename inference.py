from typing import Dict, Any, Tuple

SAMPLE_EMAILS = [
    {"email_id": "e001", "sender": "ops@company.com", "subject": "Server Down!", "body": "Our production server is completely down. Critical emergency!", "timestamp": "2024-01-01 09:00", "correct_category": "urgent", "correct_priority": 5, "correct_route": "engineering"},
    {"email_id": "e002", "sender": "billing@vendor.com", "subject": "Invoice #1234", "body": "Your invoice for January is ready. Payment due in 7 days", "timestamp": "2024-01-01 10:00", "correct_category": "billing", "correct_priority": 3, "correct_route": "billing_team"},
    {"email_id": "e003", "sender": "user@email.com", "subject": "Login Bug", "body": "There is a bug in the login page. App keeps crashing on mobile.", "timestamp": "2024-01-01 11:00", "correct_category": "bug_report", "correct_priority": 4, "correct_route": "engineering"},
    {"email_id": "e004", "sender": "spam@promo.com", "subject": "You Won!", "body": "Congratulations! You won a free iPhone. Click here to claim your prize.", "timestamp": "2024-01-01 12:00", "correct_category": "spam", "correct_priority": 1, "correct_route": "spam_filter"},
    {"email_id": "e005", "sender": "team@company.com", "subject": "Meeting Notes", "body": "Here are the notes from Monday meeting. Please review.", "timestamp": "2024-01-01 13:00", "correct_category": "general", "correct_priority": 2, "correct_route": "support"},
]

class EmailTriageEnv:
    def __init__(self):
        self.emails = SAMPLE_EMAILS.copy()
        self.current_idx = 0
        self.score = 0.0
        self.steps = 0
        self.task_id = "task_1_classify"
        self.total_emails = len(self.emails)

    def reset(self):
        self.current_idx = 0
        self.score = 0.0
        self.steps = 0
        return self._get_observation()

    def _get_observation(self):
        if self.current_idx >= len(self.emails):
            self.current_idx = 0
        email = self.emails[self.current_idx]
        return {"email_id": email["email_id"], "sender": email["sender"], "subject": email["subject"], "body": email["body"], "timestamp": email["timestamp"]}

    def _calculate_reward(self, email, user_category, user_priority, user_route):
        if (user_category.lower().strip() == email["correct_category"].lower().strip() and
            int(user_priority) == int(email["correct_priority"]) and
            user_route.lower().strip() == email["correct_route"].lower().strip()):
            return 1.0
        return 0.0

    def step(self, category, priority, route):
        email = self.emails[self.current_idx]
        reward = self._calculate_reward(email, category, priority, route)
        self.score += reward
        self.steps += 1
        self.current_idx += 1
        done = (self.current_idx >= len(self.emails))
        observation = self._get_observation() if not done else {}
        info = {"score": round(self.score, 2), "steps": self.steps, "task_id": self.task_id}
        return observation, reward, done, info

    def get_state(self):
        return {"current_idx": self.current_idx, "score": round(self.score, 2), "steps": self.steps, "task_id": self.task_id, "total_emails": self.total_emails}

env = EmailTriageEnv()

def reset_env():
    env.reset()
    return {"observation": env._get_observation(), "state": env.get_state()}

def step_env(category, priority, route):
    observation, reward, done, info = env.step(category, priority, route)
    return {"done": done, "info": info, "observation": observation, "reward": round(reward, 2)}

def get_state():
    return env.get_state()
