# AutoStream GenAI Sales Agent

A conversational AI sales assistant built for the ServiceHive Machine Learning / GenAI Internship Assignment.

## Project Objective

Build a real-world AI sales agent that can:

- Answer customer queries intelligently
- Retrieve product knowledge using local RAG
- Detect purchase intent
- Capture qualified leads
- Manage multi-step conversations
- Export leads for business use

---

## Key Features

### Conversational AI Agent
Handles natural customer queries about plans, pricing, support, features, and policies.

### Intent Detection
Understands:

- Pricing requests
- Plan comparisons
- Feature queries
- Refund/support questions
- Purchase intent
- Negative / not interested intent

### Local RAG Knowledge Base
Uses structured product/company knowledge from a local dataset (`kb.json`) to provide accurate answers.

### Stateful Workflow
Guides users through lead capture process:

1. Plan selection  
2. Name collection  
3. Email validation  
4. Platform collection  
5. Lead submission

### Gemini API Integration
Uses Google Gemini for natural language responses with fallback logic for reliability.

### Tool Execution
Stores captured leads into CSV file for CRM / sales usage.

### Streamlit Dashboard
Includes:

- Chat interface
- Total leads count
- Popular plan summary
- CSV download

---

## Tech Stack

- Python
- Streamlit
- Pandas
- Google Gemini API
- Python Dotenv
- Regex Validation
- Stateful Session Management

---

## Project Structure

```text
social-to-lead-agent/
│── app.py
│── main.py
│── kb.json
│── requirements.txt
│── README.md
│── leads.csv
