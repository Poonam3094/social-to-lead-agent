import streamlit as st
import pandas as pd
import re
import os
from datetime import datetime
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AutoStream AI Agent",
    page_icon="🤖",
    layout="wide"
)

# ---------------- SESSION ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "stage" not in st.session_state:
    st.session_state.stage = "chat"

if "lead" not in st.session_state:
    st.session_state.lead = {}

if "leads" not in st.session_state:
    st.session_state.leads = []

# ---------------- KNOWLEDGE BASE (RAG) ----------------
knowledge = {
    "basic": "Basic Plan: $29/month | 10 videos/month | 720p resolution.",
    "pro": "Pro Plan: $79/month | Unlimited videos | 4K resolution | AI captions.",
    "price": "Basic Plan = $29/month | Pro Plan = $79/month.",
    "refund": "Refund policy: No refunds after 7 days of purchase.",
    "support": "24/7 support is available only on the Pro Plan.",
    "features": "Features include AI captions, automated video creation, analytics dashboard, social scheduling, and multi-platform publishing.",
    "plans": "We offer two plans:\n\n1. Basic Plan ($29/month)\n2. Pro Plan ($79/month)"
}

# ---------------- HELPERS ----------------
def valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def save_lead():
    st.session_state.lead["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.leads.append(st.session_state.lead.copy())


# ---------------- AGENT ----------------
def ask_gemini(user_query, context):

    prompt = f"""
You are AutoStream AI Sales Agent.

Use ONLY this business knowledge:

{context}

Answer clearly, professionally, and briefly.

Customer question:
{user_query}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception:
        return context

def run_agent(user):

    msg = user.lower().strip()

    # -------- Negative Intent --------
    negative_words = [
        "not interested",
        "dont want",
        "don't want",
        "no thanks",
        "not now",
        "later",
        "maybe later",
        "not buying"
    ]

    if any(x in msg for x in negative_words):
        st.session_state.stage = "chat"
        st.session_state.lead = {}
        return "No problem. I'm here if you'd like pricing, features, or plans later."

    # -------- Greeting --------
    if any(x in msg for x in ["hi", "hello", "hey"]):
        return "Hello! Welcome to AutoStream AI Agent. Ask me about pricing, plans, support, or features."

    # -------- Buy Intent --------
    positive_words = [
        "buy",
        "purchase",
        "subscribe",
        "signup",
        "sign up",
        "interested"
    ]

    if any(x in msg for x in positive_words):

        if "pro" in msg:
            st.session_state.lead["plan"] = "Pro Plan"
        elif "basic" in msg:
            st.session_state.lead["plan"] = "Basic Plan"
        else:
            st.session_state.lead["plan"] = "Unknown"

        st.session_state.stage = "name"
        return "Great choice. What is your name?"

    # -------- Features FIRST --------
    if "feature" in msg:

        if "basic" in msg:
            return "Basic Plan includes 10 videos/month, 720p exports, starter automation tools."

        if "pro" in msg:
            return "Pro Plan includes unlimited videos, 4K exports, AI captions, priority support."

        if "each" in msg or "both" in msg:
            return """Basic Plan:
- 10 videos/month
- 720p exports

Pro Plan:
- Unlimited videos
- 4K exports
- AI captions
- Priority support"""

        return knowledge["features"]

    # -------- Plans --------
    if "plan" in msg:

        if "basic" in msg:
            return knowledge["basic"]

        if "pro" in msg:
            return knowledge["pro"]

        return ask_gemini(user, knowledge["plans"])

    # -------- Pricing --------
    if any(x in msg for x in ["price", "pricing", "cost"]):
        return ask_gemini(user, knowledge["price"])

    # -------- Support --------
    if "support" in msg:
        return knowledge["support"]

    # -------- Refund --------
    if "refund" in msg:
        return knowledge["refund"]

    # -------- Exact Short Inputs --------
    if msg == "basic":
        return knowledge["basic"]

    if msg == "pro":
        return knowledge["pro"]

    return "I can help with pricing, plans, refund policy, support, features, or sign-up."
# ---------------- LEAD FLOW ----------------
def process_input(user):

    stage = st.session_state.stage

    if stage == "name":
        st.session_state.lead["name"] = user
        st.session_state.stage = "email"
        return "Please share your email address."

    elif stage == "email":
        if valid_email(user):
            st.session_state.lead["email"] = user
            st.session_state.stage = "platform"
            return "Which creator platform do you use? (YouTube / Instagram etc.)"
        else:
            return "Please enter a valid email address."

    elif stage == "platform":
        st.session_state.lead["platform"] = user
        save_lead()
        st.session_state.stage = "chat"
        st.session_state.lead = {}
        return "✅ Thank you. Your lead has been captured successfully."

    else:
        return run_agent(user)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("📊 Business Dashboard")

    st.metric("Total Leads", len(st.session_state.leads))

    if len(st.session_state.leads) > 0:
        df = pd.DataFrame(st.session_state.leads)

        if "plan" in df.columns:
            popular = df["plan"].mode()[0]
        else:
            popular = "N/A"
    else:
        popular = "N/A"

    st.metric("Popular Plan", popular)

    st.markdown("---")
    st.subheader("📦 Plans")
    st.write("Basic Plan - $29/month")
    st.write("Pro Plan - $79/month")

    st.markdown("---")

    # ONLY SHOW IF LEADS EXIST
    if len(st.session_state.leads) > 0:
        csv = pd.DataFrame(st.session_state.leads).to_csv(index=False)

        st.download_button(
            "⬇ Download Leads CSV",
            csv,
            file_name="leads.csv",
            mime="text/csv"
        )

# ---------------- MAIN UI ----------------
st.title("🤖 AutoStream AI Sales Agent")
st.caption("Lead generation + support automation using local RAG + stateful workflow")

# Chat display
for role, msg in st.session_state.messages:
    with st.chat_message(role):
        st.write(msg)

# Input
user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.messages.append(("user", user_input))

    reply = process_input(user_input)

    st.session_state.messages.append(("assistant", reply))

    st.rerun()