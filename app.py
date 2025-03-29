import streamlit as st
import requests
import uuid

# Page config (Call this ONLY ONCE at the very top)
st.set_page_config(page_title="ODY Chatbot", layout="centered")

# Insert custom CSS directly here
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

.user-message {
    background-color: #E0F0FF;
    border-radius: 15px;
    padding: 12px 18px;
    margin: 10px;
    text-align: right;
    display: inline-block;
    max-width: 80%;
}

.bot-message {
    background-color: #F4F4F8;
    border-radius: 15px;
    padding: 12px 18px;
    margin: 10px;
    text-align: left;
    display: inline-block;
    max-width: 80%;
}

.chat-container {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}

.user-container {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
}

.input-area {
    margin-top: 20px;
}

.stButton button {
    background-color: #0A2540;
    color: white;
    border-radius: 12px;
    padding: 10px 20px;
    font-size: 16px;
    border: none;
    cursor: pointer;
}

.stButton button:hover {
    background-color: #073763;
}

.stTextInput input {
    border-radius: 12px;
    padding: 10px;
    font-size: 16px;
    border: 1px solid #ccc;
}

.logo {
    width: 50px;
    height: auto;
    margin-bottom: 10px;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Generate a unique session key if not exists
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Header with logo
st.markdown(
    "<img class='logo' src='https://companiesmarketcap.com/img/company-logos/256/IHC.AE.png'>",
    unsafe_allow_html=True
)
st.title("ODY Chatbot")
st.caption("Powered by AI | Ask anything about IHC companies")

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display chat history
for sender, message in st.session_state.messages:
    if sender == "user":
        st.markdown(f"<div class='user-container'><div class='user-message'>{message}</div></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-container'><div class='bot-message'>{message}</div></div>", unsafe_allow_html=True)

# Input area
with st.form(key='chat_form', clear_on_submit=True):
    user_query = st.text_input("", placeholder="Ask ODY...")
    submit_button = st.form_submit_button(label='Send ➤')

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
