import streamlit as st
from utils.theme import apply_theme
from utils.chat_handler import handle_ai_response
import uuid
import requests

# Page setup
st.set_page_config(page_title="ODYN Ai", layout="centered", initial_sidebar_state="collapsed")
apply_theme()

# ✨ Custom CSS for Scandinavian-style minimalism
st.markdown("""
    <style>
        html, body {
            font-family: 'Helvetica Neue', sans-serif;
            background-color: var(--bg);
            color: var(--text);
        }
        h1, h2, h3, h4 {
            font-weight: 500;
            margin-bottom: 0.25em;
        }
        .message-block {
            border-radius: 12px;
            padding: 16px;
            margin: 10px 0;
            line-height: 1.6;
        }
        .user {
            background-color: var(--user-bg);
            text-align: right;
        }
        .bot {
            background-color: var(--bot-bg);
            text-align: left;
        }
        .app-title {
            text-align: center;
            padding: 2em 0 0.5em 0;
        }
        .app-subtitle {
            text-align: center;
            color: #888;
            font-size: 0.95em;
            margin-bottom: 2em;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="app-title">
        <img src="https://images.prismic.io/icelandic/dca19f53-0f5e-4a8c-857e-c4a14211aa40_icelandic_corporate_logo_01.png?auto=compress,format" width="280">
        <h1>ODYN Ai</h1>
    </div>
    <div class="app-subtitle">Know what the state of your stock is.</div>
""", unsafe_allow_html=True)

# Session state init
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "is_thinking" not in st.session_state:
    st.session_state.is_thinking = False

# 📬 Subscription form (still minimal)
with st.expander("Subscribe to Weekly Stock Updates"):
    with st.form("email_form", clear_on_submit=True):
        email = st.text_input("Enter your email", placeholder="name@example.com")
        subscribed = st.form_submit_button("Subscribe")
        if subscribed and email:
            subscribe_url = st.secrets.get("subscribe_url")
            if subscribe_url:
                try:
                    r = requests.post(subscribe_url, json={"email": email})
                    if r.ok:
                        st.success("You're subscribed.")
                    else:
                        st.error("Something went wrong. Try again later.")
                except Exception as e:
                    st.error(f"Subscription error: {str(e)}")
            else:
                st.warning("Subscription endpoint not configured.")

# Display chat messages
for role, msg in st.session_state.messages:
    if role == "user":
        st.markdown(f"<div class='message-block user'>{msg}</div>", unsafe_allow_html=True)
    elif role == "bot":
        st.markdown(f"<div class='message-block bot'>{msg}</div>", unsafe_allow_html=True)

# Input form
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input(
        "Ask ODYN something...",
        placeholder="e.g. ESG score of Marel",
        label_visibility="collapsed"
    )
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    st.session_state.messages.append(("user", user_input))
    st.session_state.is_thinking = True
    st.rerun()

# Trigger bot thinking
if st.session_state.is_thinking:
    with st.spinner("ODY is analyzing..."):
        try:
            handle_ai_response()
        except Exception as e:
            st.session_state.messages.append(("bot", f"💥 Error talking to ODY: {str(e)}"))
        finally:
            st.session_state.is_thinking = False
