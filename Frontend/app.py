import streamlit as st
import requests

st.set_page_config(page_title="Email Triage System", layout="wide")
st.title("📧 Email Triage System")

BACKEND_URL = "https://shubhampalde1-email-triage-env.hf.space"

# Reset Button
if st.button("🔄 RESET", use_container_width=True):
    try:
        r = requests.post(f"{BACKEND_URL}/reset", timeout=10)
        if r.status_code == 200:
            st.success("✅ Reset झाला!")
        else:
            st.error(f"❌ Reset failed: {r.status_code}")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

st.markdown("---")

# Email input
email_text = st.text_area("📧 Email Text:", height=100)

col1, col2, col3 = st.columns(3)
with col1:
    category = st.selectbox("Category:", ["urgent", "billing", "bug_report", "spam", "general"])
with col2:
    priority = st.slider("Priority:", 1, 5, 3)
with col3:
    route = st.selectbox("Route:", ["engineering", "billing_team", "spam_filter", "support"])

if st.button("✅ SUBMIT", use_container_width=True):
    if not email_text.strip():
        st.error("❌ Email text रिकामं आहे!")
    else:
        try:
            payload = {
                "category": category,
                "priority": int(priority),
                "route": route
            }
            r = requests.post(f"{BACKEND_URL}/step", json=payload, timeout=10)
            if r.status_code == 200:
                result = r.json()
                reward = result.get("reward", 0)
                
                st.markdown("---")
                c1, c2, c3 = st.columns(3)
                c1.metric("🏆 Reward", reward)
                c2.metric("📊 Score", result.get("info", {}).get("score", 0))
                c3.metric("📈 Steps", result.get("info", {}).get("steps", 0))
                
                if reward == 1.0:
                    st.success("✅ PERFECT! reward = 1.0")
                else:
                    st.error(f"❌ Wrong! reward = {reward}")
                
                st.json(result)
            else:
                st.error(f"❌ Backend error: {r.status_code}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

st.markdown("---")
st.subheader("📚 Correct Test Values:")
st.markdown("""
| Test | Email | Category | Priority | Route |
|------|-------|----------|----------|-------|
| 1 | Our production server is completely down. Critical emergency! | urgent | 5 | engineering |
| 2 | Your invoice for January is ready. Payment due in 7 days | billing | 3 | billing_team |
| 3 | There is a bug in the login page. App keeps crashing on mobile. | bug_report | 4 | engineering |
| 4 | Congratulations! You won a free iPhone. Click here to claim your prize. | spam | 1 | spam_filter |
| 5 | Here are the notes from Monday meeting. Please review. | general | 2 | support |
""")
