from flask import Flask, request, jsonify

app = Flask(__name__)

EMAILS = [
    {"email_id": "e001", "subject": "Server Down!", "body": "Our production server is completely down. Critical emergency!", "sender": "ops@company.com", "timestamp": "2024-01-01 09:00", "label": "urgent", "priority": 5, "route_to": "engineering"},
    {"email_id": "e002", "subject": "Invoice #1234", "body": "Your invoice for January is ready. Payment due in 7 days.", "sender": "billing@vendor.com", "timestamp": "2024-01-01 10:00", "label": "billing", "priority": 3, "route_to": "billing_team"},
    {"email_id": "e003", "subject": "Login Bug", "body": "There is a bug in the login page. App keeps crashing on mobile.", "sender": "user@gmail.com", "timestamp": "2024-01-01 11:00", "label": "bug_report", "priority": 4, "route_to": "engineering"},
    {"email_id": "e004", "subject": "You Won!", "body": "Congratulations! You won a free iPhone. Click here to claim your prize.", "sender": "spam@promo.com", "timestamp": "2024-01-01 12:00", "label": "spam", "priority": 1, "route_to": "spam_filter"},
    {"email_id": "e005", "subject": "Meeting Notes", "body": "Here are the notes from Monday meeting. Please review.", "sender": "team@company.com", "timestamp": "2024-01-01 13:00", "label": "general", "priority": 2, "route_to": "support"},
]

env_state = {"current_idx": 0, "score": 0.0, "task_id": "task_1_classify", "steps": 0}

def calculate_reward(action, email):
    if (action.get("category") == email["label"] and
        int(action.get("priority")) == int(email["priority"]) and
        action.get("route_to") == email["route_to"]):
        return 1.0
    return 0.0

@app.route("/reset", methods=["GET", "POST"])
def reset():
    env_state["current_idx"] = 0
    env_state["score"] = 0.0
    env_state["steps"] = 0
    email = EMAILS[0]
    return jsonify({"email_id": email["email_id"], "subject": email["subject"], "body": email["body"], "sender": email["sender"], "timestamp": email["timestamp"]})

@app.route("/step", methods=["POST"])
def step():
    data = request.get_json()
    action = {"category": data.get("category", "general"), "priority": data.get("priority", 1), "route_to": data.get("route", "support")}
    email = EMAILS[env_state["current_idx"]]
    reward = calculate_reward(action, email)
    env_state["score"] += reward
    env_state["steps"] += 1
    env_state["current_idx"] += 1
    done = env_state["current_idx"] >= len(EMAILS)
    next_obs = {}
    if not done:
        next_email = EMAILS[env_state["current_idx"]]
        next_obs = {"email_id": next_email["email_id"], "subject": next_email["subject"], "body": next_email["body"], "sender": next_email["sender"], "timestamp": next_email["timestamp"]}
    return jsonify({"observation": next_obs, "reward": round(reward, 4), "done": done, "info": {"score": round(env_state["score"], 4), "steps": env_state["steps"], "task_id": env_state["task_id"]}})

@app.route("/state", methods=["GET"])
def state():
    return jsonify({"current_idx": env_state["current_idx"], "score": round(env_state["score"], 4), "task_id": env_state["task_id"], "steps": env_state["steps"], "total_emails": len(EMAILS)})

@app.route("/", methods=["GET"])
def home():
    return jsonify({"name": "Email Triage Environment", "version": "1.0.0"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
