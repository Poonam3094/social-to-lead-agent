import json
import os
from dotenv import load_dotenv
from typing import TypedDict

from langgraph.graph import StateGraph, END
import warnings
warnings.filterwarnings("ignore")
import google.generativeai as genai

# ------------------------
# Load API Key
# ------------------------
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("models/gemini-3.1-flash-image-preview")

# ------------------------
# Load Knowledge Base
# ------------------------
with open("kb.json", "r") as f:
    KB = json.load(f)

# ------------------------
# State Schema
# ------------------------
class AgentState(TypedDict):
    user_input: str
    intent: str
    name: str
    email: str
    platform: str
    response: str

# ------------------------
# Mock Tool
# ------------------------
def mock_lead_capture(name, email, platform):
    print(f"\nLead captured successfully: {name}, {email}, {platform}")

# ------------------------
# Intent Detection
# ------------------------
def classify_intent(state):
    msg = state["user_input"].lower()

    greetings = ["hi", "hello", "hey"]
    high_intent = [
    "buy",
    "purchase",
    "subscribe",
    "interested",
    "want pro",
    "want basic",
    "take pro",
    "take basic",
    "i will take",
    "i'll take",
    "demo",
    "contact sales",
    "sign up",
    "start plan"
    ]

    if any(x in msg for x in greetings):
        return {"intent": "greeting"}

    elif any(x in msg for x in high_intent):
        return {"intent": "high_intent"}

    else:
        return {"intent": "inquiry"}
# ------------------------
# Router
# ------------------------
def route(state):
    return state["intent"]

# ------------------------
# Greeting Node
# ------------------------
def greeting_node(state):
    return {
        "response": "Hello! Welcome to AutoStream. Ask me about pricing, plans or features."
    }

# ------------------------
# RAG Node
# ------------------------
def rag_node(state):
    msg = state["user_input"].lower()

    if "feature" in msg:
        return {
            "response": "Features include AI captions, automated video creation, social scheduling, analytics dashboard, and multi-platform publishing."
        }

    elif "plan" in msg or "pricing" in msg or "price" in msg:
        return {
            "response": "Basic Plan: $29/month | Pro Plan: $79/month | Contact us for enterprise pricing."
        }

    elif "basic" in msg:
        return {
            "response": "Basic Plan includes 10 videos/month, 720p exports, starter automation tools."
        }

    elif "pro" in msg:
        return {
            "response": "Pro Plan includes unlimited videos, 4K exports, AI captions, priority support."
        }

    return {
        "response": "We offer Basic and Pro plans with automation tools for creators. Ask me about plans, pricing, or features."
    }
# ------------------------
# Lead Capture Node
# ------------------------
def lead_node(state):

    if not state["name"]:
        return {"response": "Great choice. What is your name?"}

    elif not state["email"]:
        email = state["user_input"].strip()

        if "@" not in email or "." not in email:
            return {"response": "Please enter a valid email address."}

        state["email"] = email
        return {"response": "Which creator platform do you use? (YouTube / Instagram etc.)"}

    elif not state["platform"]:
        state["platform"] = state["user_input"]

        mock_lead_capture(
            state["name"],
            state["email"],
            state["platform"]
        )

        # Reset state after success
        state["intent"] = ""
        state["name"] = ""
        state["email"] = ""
        state["platform"] = ""

        return {
            "response": "Thank you. Your lead has been captured successfully."
        }
# ------------------------
# Build Graph
# ------------------------
builder = StateGraph(AgentState)

builder.add_node("classify", classify_intent)
builder.add_node("greet", greeting_node)
builder.add_node("rag", rag_node)
builder.add_node("lead", lead_node)

builder.set_entry_point("classify")

builder.add_conditional_edges(
    "classify",
    route,
    {
        "greeting": "greet",
        "inquiry": "rag",
        "high_intent": "lead"
    }
)

builder.add_edge("greet", END)
builder.add_edge("rag", END)
builder.add_edge("lead", END)

graph = builder.compile()

# ------------------------
# Initial State
# ------------------------
state = {
    "user_input": "",
    "intent": "",
    "name": "",
    "email": "",
    "platform": "",
    "response": ""
}

print("AutoStream Agent Ready. Type quit to exit.\n")

# ------------------------
# Chat Loop
# ------------------------
while True:
    user = input("You: ")

    if user.lower() == "quit":
        break

    state["user_input"] = user

    if state["intent"] == "high_intent":

        if not state["name"]:
            state["name"] = user

        result = lead_node(state)
        state.update(result)

    else:
        result = graph.invoke(state)
        state.update(result)

    print("Bot:", state["response"])