import streamlit as st
from pathlib import Path
import sqlite3
import os

from sqlalchemy import create_engine

from langchain.agents.agent_types import AgentType
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain_groq import ChatGroq


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="LangChain: Chat with SQL DB",
    page_icon="🦜",
    layout="wide"
)

st.title("🦜 LangChain: Chat with SQL DB")
st.caption("Ask questions about your database using natural language.")


# --------------------------------------------------
# DATABASE OPTIONS
# --------------------------------------------------

LOCALDB = "USE_LOCALDB"
MYSQL = "USE_MYSQL"

radio_opt = [
    "Use SQLite 3 Database - Student.db",
    "Connect to your MySQL Database"
]

selected_opt = st.sidebar.radio(
    label="Choose the database you want to chat with",
    options=radio_opt
)

if radio_opt.index(selected_opt) == 1:

    db_uri = MYSQL

    mysql_host = st.sidebar.text_input(
        "Provide MySQL Host"
    )

    mysql_user = st.sidebar.text_input(
        "MySQL User"
    )

    mysql_password = st.sidebar.text_input(
        "MySQL Password",
        type="password"
    )

    mysql_db = st.sidebar.text_input(
        "MySQL Database Name"
    )

else:

    db_uri = LOCALDB


# --------------------------------------------------
# GROQ API KEY
# --------------------------------------------------

api_key = st.sidebar.text_input(
    label="Groq API Key",
    type="password"
)

if not api_key:
    st.info("Please enter your Groq API key in the sidebar.")
    st.stop()


# --------------------------------------------------
# INITIALIZE LLM
# --------------------------------------------------

try:

    llm = ChatGroq(
        groq_api_key=api_key,
        model="llama-3.1-8b-instant",
        temperature=0,
        streaming=True
    )

except Exception as e:

    st.error(f"Error initializing Groq LLM: {e}")
    st.stop()


# --------------------------------------------------
# DATABASE CONFIGURATION
# --------------------------------------------------

@st.cache_resource(ttl=7200)
def configure_db(
    db_uri,
    mysql_host=None,
    mysql_user=None,
    mysql_password=None,
    mysql_db=None
):

    if db_uri == LOCALDB:

        dbfilepath = (
            Path(__file__).parent / "student.db"
        ).absolute()

        if not dbfilepath.exists():
            raise FileNotFoundError(
                f"Database file not found: {dbfilepath}"
            )

        creator = lambda: sqlite3.connect(
            f"file:{dbfilepath}?mode=ro",
            uri=True
        )

        engine = create_engine(
            "sqlite:///",
            creator=creator
        )

        return SQLDatabase(engine)

    elif db_uri == MYSQL:

        if not all([
            mysql_host,
            mysql_user,
            mysql_password,
            mysql_db
        ]):

            raise ValueError(
                "Please provide all MySQL connection details."
            )

        from sqlalchemy.engine import URL

        connection_url = URL.create(
            drivername="mysql+mysqlconnector",
            username=mysql_user,
            password=mysql_password,
            host=mysql_host,
            database=mysql_db
        )

        engine = create_engine(connection_url)

        return SQLDatabase(engine)


# --------------------------------------------------
# CONNECT TO DATABASE
# --------------------------------------------------

try:

    if db_uri == MYSQL:

        db = configure_db(
            db_uri,
            mysql_host,
            mysql_user,
            mysql_password,
            mysql_db
        )

    else:

        db = configure_db(db_uri)

    st.sidebar.success("Database connected successfully!")

except Exception as e:

    st.error(f"Database connection error: {e}")
    st.stop()


# --------------------------------------------------
# SQL DATABASE TOOLKIT
# --------------------------------------------------

try:

    toolkit = SQLDatabaseToolkit(
        db=db,
        llm=llm
    )

    agent = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        handle_parsing_errors=True
    )

except Exception as e:

    st.error(f"Error creating SQL agent: {e}")
    st.stop()


# --------------------------------------------------
# CHAT HISTORY
# --------------------------------------------------

if "messages" not in st.session_state:

    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": "Hello! 👋 How can I help you query your database?"
        }
    ]


if st.sidebar.button("Clear Message History"):

    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": "Hello! 👋 How can I help you query your database?"
        }
    ]

    st.rerun()


# --------------------------------------------------
# DISPLAY CHAT HISTORY
# --------------------------------------------------

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.write(msg["content"])


# --------------------------------------------------
# USER INPUT
# --------------------------------------------------

user_query = st.chat_input(
    placeholder="Ask anything about your database..."
)


# --------------------------------------------------
# PROCESS USER QUERY
# --------------------------------------------------

if user_query:

    # Store user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_query
        }
    )

    with st.chat_message("user"):
        st.write(user_query)

    # Generate assistant response
    with st.chat_message("assistant"):

        try:

            streamlit_callback = StreamlitCallbackHandler(
                st.container()
            )

            with st.spinner("Analyzing your database..."):

                response = agent.invoke(
                    {"input": user_query},
                    config={
                        "callbacks": [streamlit_callback]
                    }
                )

            answer = response.get(
                "output",
                "Sorry, I could not generate a response."
            )

            st.write(answer)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

        except Exception as e:

            error_message = f"An error occurred: {str(e)}"

            st.error(error_message)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": error_message
                }
            )
