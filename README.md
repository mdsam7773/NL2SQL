# NL2SQL Chatbot using Vanna AI + FastAPI

## 📌 Project Description

This project is a Natural Language to SQL (NL2SQL) chatbot built using Vanna AI. It allows users to ask questions in plain English and automatically converts them into SQL queries, executes them on a SQLite database, and returns the results.

The system is designed with a FastAPI backend and includes SQL validation, memory-based learning, and structured API responses.

---

## ⚙️ Tech Stack

- Python
- FastAPI
- Vanna AI
- SQLite
- Groq (LLM - LLaMA 3)

---

## 🚀 Setup Instructions

i create app using vannafastapiserver so please run main.py file for running the app. 
the application is started using :
python main.py

since VannaFastApiServer internally runs a FastAPi server, uvicorn is not required.

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <project-folder>

#for running the app

#run command-> 
#python main.py