# AutoStream GenAI Sales Agent

A conversational AI sales assistant built for the ServiceHive Machine Learning / GenAI Internship Assignment.

---

## Project Objective

Build a real-world AI sales agent that can:

* Answer customer queries intelligently
* Retrieve business knowledge using RAG
* Detect customer intent
* Capture qualified leads
* Manage multi-step conversations
* Execute business actions
* Export leads for follow-up

---

## Key Features

### Conversational AI Support

Handles user queries about:

* Pricing
* Plans
* Features
* Refund policy
* Support availability
* Purchase interest

### Intent Detection

Detects:

* Pricing requests
* Plan comparison
* Feature questions
* Refund/support queries
* Purchase intent
* Negative / not interested intent

### RAG Knowledge Retrieval

Uses a structured local knowledge base (`kb.json`) containing:

* Product pricing
* Feature details
* Support policy
* Refund policy

### Stateful Workflow

When purchase intent is detected:

1. Ask selected plan
2. Ask customer name
3. Validate email
4. Ask creator platform
5. Save lead

### Tool Execution

Stores captured leads into CSV for business follow-up.

### Streamlit Dashboard

Includes:

* Chat interface
* Lead analytics
* CSV export
* Deployment-ready UI

---

## Tech Stack

* Python
* Streamlit
* Pandas
* Google Gemini API
* Python Dotenv
* Regex Validation
* Session State Management

---

## Project Structure

```text
social-to-lead-agent/
│── app.py
│── main.py
│── kb.json
│── requirements.txt
│── README.md
│── .gitignore
```

---

## How to Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open:

```text
http://localhost:8501
```

---

## Example Queries

* What plans do you offer?
* Tell me features of Pro plan
* What is your refund policy?
* Do you offer support?
* I want to buy Pro plan

---

## Architecture Explanation

This project uses a lightweight AI agent workflow inspired by LangGraph-style orchestration.

Flow:

**User Query → Intent Detection → RAG Retrieval → Response → Lead Workflow → CSV Tool Action**

Informational queries are answered using a local structured knowledge base (`kb.json`).

When buying intent is detected, the system enters a guided multi-step lead capture workflow.

Conversation state is managed through Streamlit Session State, preserving chat history and lead progress across interactions.

This makes the project a deployable business automation agent rather than a simple chatbot.

---

## Why LangGraph / AutoGen Approach

This solution is inspired by LangGraph concepts:

* Node-based transitions
* Persistent state
* Controlled routing
* Memory across steps

For this assignment, a custom lightweight Python implementation was chosen to keep the system simple, fast, and easy to deploy.

For larger systems, LangGraph / AutoGen would help with:

* Multi-agent workflows
* Human approvals
* Parallel tasks
* Advanced tool orchestration

---

## How State is Managed

Using `st.session_state`, the app stores:

* Chat history
* Current lead step
* Selected plan
* Name
* Email
* Platform

This ensures conversation continuity.

---

## WhatsApp Deployment Using Webhooks

Production deployment can be done using WhatsApp Business API or Twilio.

Flow:

1. User sends WhatsApp message
2. Webhook receives message
3. Backend sends input to agent
4. Agent processes intent/state/RAG
5. Response sent back via API
6. Leads saved to CRM/database

Each phone number acts as a unique session ID.

---

## Deliverables Checklist

* ✅ Agent logic
* ✅ RAG pipeline
* ✅ Intent detection
* ✅ Tool execution
* ✅ requirements.txt
* ✅ Local setup guide
* ✅ Architecture explanation
* ✅ State management explanation
* ✅ WhatsApp deployment plan

---

## Why This Is More Than a Chatbot

This system can:

* Understand intent
* Retrieve structured knowledge
* Manage workflows
* Capture leads
* Validate inputs
* Execute actions

That makes it an AI Agent.

---

## Future Improvements

* Vector DB RAG
* CRM Integration
* Live WhatsApp deployment
* Multi-language support
* Analytics dashboard

---

## Author

**Poonam Saini**
