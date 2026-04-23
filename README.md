# AutoStream GenAI Sales Agent

A conversational AI sales assistant built for the ServiceHive Machine Learning / GenAI Internship Assignment.

---

# Project Objective

Build a real-world AI sales agent that can:

- Answer customer queries intelligently
- Retrieve business knowledge using RAG
- Detect customer intent
- Capture qualified leads
- Manage multi-step conversations
- Execute business actions
- Export leads for follow-up

---

# Key Features

## Conversational AI Support

Handles natural user queries such as:

- Pricing
- Plans
- Features
- Refund policy
- Support availability
- Purchase interest

## Intent Detection

Detects and routes user intent including:

- Pricing requests
- Plan comparison
- Feature questions
- Refund policy queries
- Support questions
- Purchase intent
- Negative / not interested intent

## RAG Knowledge Retrieval

Uses a structured local knowledge base (`kb.json`) containing:

- Product pricing
- Feature details
- Support policy
- Refund policy

Relevant information is retrieved dynamically to generate accurate responses.

## Stateful Workflow

When buying intent is detected, the system starts a lead capture flow:

1. Ask selected plan  
2. Ask customer name  
3. Validate email  
4. Ask creator platform  
5. Save lead

## Tool Execution

Qualified leads are stored automatically into CSV format for business use.

## Streamlit Dashboard

Includes:

- Interactive chat interface
- Lead analytics
- CSV export
- Clean deployment-ready UI

---

# Tech Stack

- Python
- Streamlit
- Pandas
- Google Gemini API
- Python Dotenv
- Regex Validation
- Session State Management

---

# Project Structure

```text
social-to-lead-agent/
│── app.py
│── main.py
│── kb.json
│── requirements.txt
│── README.md
│── leads.csv
```
# How to Run Locally

pip install -r requirements.txt
- streamlit run app.py

Then open:
http://localhost:8501

###  Example Queries
- What plans do you offer?  
- Tell me features of Pro plan  
- What is your refund policy?  
- Do you offer support?  
- I want to buy Pro plan  


# Architecture Explanation

This project was designed as a lightweight real-world AI agent workflow inspired by graph-based orchestration systems such as LangGraph.

Instead of adding unnecessary framework complexity, I implemented the workflow directly in Python to keep the solution fast, readable, reliable, and easy to deploy.

The system follows an agent pipeline:

User Query
→ Intent Detection
→ Knowledge Retrieval (RAG)
→ Response Generation
→ Lead Workflow States
→ Tool Execution

When a user sends a message, the system first detects intent such as:

- Pricing request
- Plan comparison
- Feature query
- Refund/support question
- Purchase intent
- Negative intent

For informational requests, the system retrieves relevant answers from the structured local knowledge base (kb.json). This acts as a lightweight Retrieval-Augmented Generation (RAG) system.

When purchase intent is detected, the agent transitions into a guided multi-step lead workflow:

- Collect name
- Validate email
- Collect creator platform
- Save lead to CSV

State is maintained using Streamlit Session State, which preserves conversation memory and workflow progress across messages.

This creates a deployable business automation agent rather than only a chatbot.

# Why LangGraph / AutoGen Approach

This solution is inspired by LangGraph concepts such as:

- Node-based workflow transitions
- Persistent state management
- Memory between steps
- Controlled business logic routing

Because the assignment scope was focused and time-limited, I implemented a custom lightweight state machine directly in Python instead of introducing additional framework overhead.

For larger production systems, LangGraph or AutoGen would be excellent choices for:

- Multi-agent collaboration
- Human-in-loop approval systems
- Advanced memory systems
- External tool orchestration
- Parallel task execution

# How State is Managed

The application uses st.session_state in Streamlit.

This stores:

- Chat history
- Current lead capture step
- Selected plan
- User name
- User email
- User platform
- Completed leads

This ensures users can continue the conversation naturally while preserving progress in the workflow.

# WhatsApp Deployment Using Webhooks

To deploy this agent on WhatsApp, I would integrate it using WhatsApp Business API (Meta Cloud API) or Twilio.

Deployment flow:

- User sends WhatsApp message
- WhatsApp forwards message to webhook endpoint
- Backend server (FastAPI / Flask) receives request
- Request is passed to agent logic
- Agent processes:
- Intent
- State
- Knowledge retrieval
- Lead workflow
- Response sent back via WhatsApp API
- Leads stored in database / CSV / CRM

Each phone number would act as a unique session ID to maintain separate user state.

This would make the solution production-ready for lead generation and customer support.

# Deliverables Checklist

✅ Agent logic
✅ RAG pipeline
✅ Intent detection
✅ Tool execution
✅ requirements.txt
✅ Local setup guide
✅ Architecture explanation
✅ State management explanation
✅ WhatsApp deployment plan

# Why This Is More Than a Chatbot

This system does more than generate replies.

It can:

- Understand intent
- Retrieve structured knowledge
- Maintain workflow state
- Collect qualified leads
- Validate user inputs
- Execute business actions
- Store outputs

That makes it an AI Agent.

# Future Improvements

- Vector database RAG
- CRM integrations
- Live WhatsApp deployment
- Human handoff mode
- Multi-language support
- Analytics dashboard
- Admin panel

# Author
Poonam Saini
