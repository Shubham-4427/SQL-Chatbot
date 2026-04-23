# SQL-Chatbot
An interactive Streamlit-based AI application that allows users to chat with SQL databases (SQLite / MySQL) using natural language. Powered by LangChain + Groq LLM, this app converts user queries into SQL and returns meaningful results instantly.

🚀 Features

  🧠 Natural Language → SQL Query conversion

  📊 Supports SQLite (local DB) and MySQL (remote DB)

  ⚡ Fast responses using Groq LLM (LLaMA 3)

  💬 Chat-style interface using Streamlit

  🔐 Secure API key input

  🛠 Modular and extendable architecture


🏗️ Tech Stack

  Frontend: Streamlit

  LLM: Groq (llama3-8b-instant)

  Framework: LangChain

  Database: SQLite / MySQL

  ORM/Connector: SQLAlchemy

  Language: Python


📂 Project Structure

   SQL_chat/
    
    │── app.py              # Main Streamlit app
    
    │── sqlite.py          # SQLite DB handling
    
    │── student.db         # Sample database
    
    │── requirements.txt   # Dependencies
    
    │── .env               # Environment variables (optional)


🧑‍💻 Usage

  Select database option:

  SQLite (default: student.db)

  MySQL (enter credentials)

  Enter your Groq API Key

  Ask questions like:
   “Show all students”
   “What is the average marks?”
   “List top 5 performers”

  Get instant results 🎯


🧠 How It Works

  User inputs a natural language query

  LangChain agent processes the query

  Converts it into SQL using schema understanding

  Executes query via SQLAlchemy

  Returns formatted response


🔮 Future Improvements

  Add PostgreSQL support
  
  Query history & caching

  Visualization (charts/graphs)

  Role-based access control

  Deployment (Streamlit Cloud / Docker)


👨‍💻 Author

  Shubham Kumar

  AI/ML Engineer
