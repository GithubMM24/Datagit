import streamlit as st
import pandas as pd
from agent import DataAgent


# Page Config
st.set_page_config(
    page_title="Smart Data Query Agent",
    layout="wide"
)

# Sidebar and File Upload
st.sidebar.header("📂 Upload CSV File")

uploaded_file = st.sidebar.file_uploader(
    "Drag & drop a CSV file",
    type=["csv"]
)


# Load Data
def load_data(file):
    return pd.read_csv(file)


# Handle Dataset Load / Reload
if uploaded_file is not None:
    df = load_data(uploaded_file)

    # Reset session state on new upload
    if "current_file" not in st.session_state or st.session_state.current_file != uploaded_file.name:
        st.session_state.current_file = uploaded_file.name
        st.session_state.agent = DataAgent(df)
        st.session_state.messages = []

else:
    st.warning("Please upload a CSV file to begin.")
    st.stop()

agent = st.session_state.agent


# Sidebar Dataset Info section
st.sidebar.markdown("---")
st.sidebar.header("Dataset Info")
st.sidebar.write("Rows:", df.shape[0])
st.sidebar.write("Columns:", df.shape[1])
st.sidebar.write(df.columns.tolist())

# st.sidebar.markdown("---")
# st.sidebar.markdown("### Sample Queries")
# # st.sidebar.code("""
# # Show channel LinkedIn
# # Average resume_score
# # resume_score between 60 and 90
# # resume_score descending
# # count records
# # What's going on in dataset
# # """)

# Header
st.markdown(
    "<h1 style='text-align:center;'> Smart Data Query Agent</h1>"
    "<p style='text-align:center;color:gray;'>Chat with your dataset using natural language</p>",
    unsafe_allow_html=True
)


#  Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["type"] == "dataframe":
            st.dataframe(msg["content"], use_container_width=True)
        else:
            st.write(msg["content"])


# Chat Input
user_query = st.chat_input("Ask something about the dataset...")

if user_query:
    # User message
    st.session_state.messages.append({
        "role": "user",
        "type": "text",
        "content": user_query
    })

    with st.chat_message("user"):
        st.write(user_query)

    # Agent response
    response = agent.process_query(user_query)

    intent_msg = f"**Intent:** `{response['intent']}`"

    st.session_state.messages.append({
        "role": "assistant",
        "type": "text",
        "content": intent_msg
    })

    with st.chat_message("assistant"):
        st.markdown(intent_msg)

        result = response["result"]

        if isinstance(result, pd.DataFrame):
            st.session_state.messages.append({
                "role": "assistant",
                "type": "dataframe",
                "content": result
            })
            st.dataframe(result, use_container_width=True)

        elif isinstance(result, dict):
            st.session_state.messages.append({
                "role": "assistant",
                "type": "text",
                "content": result
            })
            st.json(result)

        else:
            st.session_state.messages.append({
                "role": "assistant",
                "type": "text",
                "content": result
            })
            st.write(result)

