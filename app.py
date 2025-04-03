import streamlit as st
from utils.theme import apply_theme
from utils.chat_handler import handle_ai_response
import uuid
import requests

# Page setup
st.set_page_config(page_title="ODYN Ai", layout="centered", initial_sidebar_state="collapsed")

# Custom styling (Scandinavian minimalism)
st.markdown("""
    <style>
        html, body {
            background-color: #F9FAFB;
            color: #111827;
            font-family: 'Helvetica Neue', sans-serif;
        }
        .block-container {
            padding-top: 2rem;
        }
        .chat-bubble {
            padding: 1rem;
            border-radius: 12px;
            margin-bottom: 0.5rem;
            font-size: 15px;
            line-height: 1.6;
        }
        .user {
            background-color: #E5E7EB;
            text-align: right;
        }
        .bot {
            background-color: #F3F4F6;
            text-align: left;
        }
        .chat-wrapper {
            max-width: 720px;
            margin: auto;
        }
        .odyn-header h1 {
            margin-bottom: 0;
        }
        .odyn-header p {
            color: #6B7280;
            font-size: 14px;
            margin-top: 4px;
        }
    </style>
""", unsafe_allow_html=True)

# Session state init
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "is_thinking" not in st.session_state:
    st.session_state.is_thinking = False

# Header
st.markdown("""
    <div class="odyn-header" style="text-align: center; padding-bottom: 2rem;">
        <img src='https://images.prismic.io/icelandic/dca19f53-0f5e-4a8c-857e-c4a14211aa40_icelandic_corporate_logo_01.png?auto=compress,format' width='200'>
        <h1>ODYN Ai</h1>
        <p>Know what the state of your stock is</p>
    </div>
""", unsafe_allow_html=True)

# 📬 Subscription form
with st.expander("📬 Subscribe to Weekly Stock Updates"):
    with st.form("email_form", clear_on_submit=True):
        email = st.text_input("Enter your email")
        subscribed = st.form_submit_button("Subscribe")
        if subscribed and email:
            subscribe_url = st.secrets.get("subscribe_url")
            if subscribe_url:
                try:
                    r = requests.post(subscribe_url, json={"email": email})
                    if r.ok:
                        st.success("You're subscribed! ✅")
                    else:
                        st.error("Something went wrong. Try again later.")
                except Exception as e:
                    st.error(f"Failed to reach the subscription server: {str(e)}")
            else:
                st.warning("No subscription webhook configured.")

# 💬 Display messages
st.markdown("<div class='chat-wrapper'>", unsafe_allow_html=True)
for role, msg in st.session_state.messages:
    if role == "user":
        st.markdown(f"<div class='chat-bubble user'>{msg}</div>", unsafe_allow_html=True)
    elif role == "bot":
        st.markdown(f"<div class='chat-bubble bot'>🤖 <strong>ODY:</strong><br>{msg}</div>", unsafe_allow_html=True)
    elif role == "card":
        st.markdown(msg, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# 📝 Input form
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input(
        "Ask Odyn...",
        placeholder="e.g. ESG score of Marel or inventory in China",
        label_visibility="collapsed"
    )
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    st.session_state.messages.append(("user", user_input))
    st.session_state.is_thinking = True
    st.rerun()

# 🤖 ODY replies
if st.session_state.is_thinking:
    with st.spinner("ODY is thinking..."):
        try:
            handle_ai_response()
        except Exception as e:
            st.session_state.is_thinking = False
            st.error(f"💥 Error talking to ODY: {str(e)}")
