import streamlit as st
import requests
import uuid

# Page config (Call this ONLY ONCE at the very top)
st.set_page_config(page_title="ODY Chatbot", layout="centered")

# Custom CSS for refined UI
custom_css = """
<style>
body, .stApp {
    background-color: #FFFFFF;
    color: #333333;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

h1, h2, h3 {
    color: #0A2540;
}

.logo {
    width: 50px;
    margin-bottom: 15px;
}

.user-message {
    background-color: #DCF8C6;
    color: #333333;
    border-radius: 18px;
    padding: 10px 15px;
    margin: 8px 0;
    max-width: 75%;
    align-self: flex-end;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.bot-message {
    background-color: #F1F0F0;
    color: #333333;
    border-radius: 18px;
    padding: 10px 15px;
    margin: 8px 0;
    max-width: 75%;
    align-self: flex-start;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.message-container {
    display: flex;
    flex-direction: column;
}

.stTextInput input {
    border-radius: 15px;
    border: 2px solid #0A2540;
    padding: 12px;
    font-size: 15px;
    color: #333333;
}

.stForm .stTextInput {
    flex-grow: 1;
    margin-right: 10px;
}

.stForm .stButton button {
    background-color: #ffffff;
    color: #333333;
    border: 2px solid #0A2540;
    border-radius: 15px;
    padding: 10px 20px;
    font-size: 15px;
    cursor: pointer;
    transition: background-color 0.3s ease, color 0.3s ease;
}

.stForm .stButton button:hover {
    background-color: #0A2540;
    color: white;
}

.stForm {
    display: flex;
    gap: 10px;
    align-items: center;
    justify-content: space-between;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Generate a unique session key if not exists
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Header with ODY logo
st.markdown(
    "<img class='logo' src='https://companiesmarketcap.com/img/company-logos/256/IHC.AE.png'>",
    unsafe_allow_html=True
)
st.title("ODY Chatbot")
st.caption("Powered by AI | Ask anything about IHC companies")

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display chat history clearly aligned
chat_container = st.container()
with chat_container:
    for sender, message in st.session_state.messages:
        if sender == "user":
            st.markdown(f"<div class='message-container'><div class='user-message'>{message}</div></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='message-container'><div class='bot-message'>{message}</div></div>", unsafe_allow_html=True)

# User input form
with st.form(key='chat_form', clear_on_submit=True):
    cols = st.columns([5, 1])
    user_query = cols[0].text_input("", placeholder="Ask ODY...", label_visibility="collapsed")
    submit_button = cols[1].form_submit_button(label='Send ➤')

if submit_button and user_query:
    st.session_state.messages.append(("user", user_query))

    with st.spinner("ODY is typing..."):
        AI_ENDPOINT_URL = "https://timoleon.app.n8n.cloud/webhook/fc4d4829-f74d-42d9-9dd7-103fd2ecdb1c"

        try:
            response = requests.post(AI_ENDPOINT_URL, json={
                "query": user_query,
                "session_id": st.session_state.session_id
            })

            if response.ok:
                ai_output = response.text.strip()
                st.session_state.messages.append(("bot", ai_output))
                st.rerun()
            else:
                st.error(f"Failed to fetch details: Status code {response.status_code}")
                st.write(response.text)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
