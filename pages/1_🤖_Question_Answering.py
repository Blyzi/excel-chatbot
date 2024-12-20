import os
from langchain_mistralai import ChatMistralAI
import streamlit as st
from utils.question_answering import answer_question, get_graph
from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_community.utilities import SQLDatabase

# -------- Page state ------------

os.environ["MISTRAL_API_KEY"] = "<YOUR_MISTRAL_API_KEY>"

rate_limiter = InMemoryRateLimiter(
    requests_per_second=0.3, 
    check_every_n_seconds=0.1,
    max_bucket_size=10,
)

llm = ChatMistralAI(model_name='open-mistral-nemo', max_concurrent_requests=1, rate_limiter=rate_limiter)

# ---------------------------------

st.title('🤖 Question Answering Chatbot')

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask your question here"):

    db = SQLDatabase.from_uri("sqlite:///./data/storage.db", sample_rows_in_table_info=5)
    graph = get_graph(db, llm)

    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    generator = answer_question(graph, prompt)

    with st.chat_message("assistant"):
        response = st.write_stream(generator)

    st.session_state.messages.append({"role": "assistant", "content": response})