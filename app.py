import streamlit as st
from utils.theme import apply_theme
from utils.chat_handler import handle_ai_response
import uuid
import requests

# Page setup
st.set_page_config(page_title="ODYN Ai", layout="centered", initial_sidebar_state="collapsed")
apply_theme()

# Header
st.markdown("""
    <div style='text-align:center; padding:1em;'>
        <img src='https://images.prismic.io/icelandic/dca19f53-0f5e-4a8c-857e-c4a14211aa40_icelandic_corporate_logo_01.png?auto=compress,format' width='300'>
        <h1 style='margin-bottom:0;'>ODYN Ai</h1>
        <p style='color:gray;'>Know what the state of your stock is!</p>
    </div>
""", unsafe_allow_html=True)

# Session state init
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "is_thinking" not in st.session_state:
    st.session_state.is_thinking = False

# 📬 Subscription form (optional webhook)
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
                st.warning("Subscription webhook URL not configured yet.")

# 💬 Display chat messages
for role, msg in st.session_state.messages:
    if role == "user":
        st.markdown(f"<div style='text-align:right; padding:12px; border-radius:16px; background-color:var(--user-bg); color:var(--text); margin-bottom:10px;'>🧑‍💻 <strong>You:</strong><br>{msg}</div>", unsafe_allow_html=True)
    elif role == "bot":
        st.markdown(f"<div style='text-align:left; padding:12px; border-radius:16px; background-color:var(--bot-bg); color:var(--text); margin-bottom:10px;'>🤖 <strong>ODY:</strong><br>{msg}</div>", unsafe_allow_html=True)
    elif role == "card":
        st.markdown(msg, unsafe_allow_html=True)

# 💬 Chat input
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Ask Odyn, what the state of your stock is...", placeholder="e.g. ESG score of Marel", label_visibility="collapsed")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    st.session_state.messages.append(("user", user_input))
    st.session_state.is_thinking = True
    st.rerun()

# 🤖 AI response
if st.session_state.is_thinking:
    with st.spinner("🤔 ODY is thinking..."):
        try:
            handle_ai_response()
        except Exception as e:
            st.error(f"💥 Something went wrong with ODY: {str(e)}")
        finally:
            st.session_state.is_thinking = False

# ✅ DEBUGGING (safe to remove later)
if "ai_url" in st.secrets:
    st.write("✅ DEBUG: Using AI endpoint:", st.secrets["ai_url"])
else:
    st.warning("⚠️ AI URL is not set in secrets!")

if st.session_state.messages:
    st.write("✅ DEBUG: Last user message:", st.session_state.messages[-1][1])
