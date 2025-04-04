import streamlit as st
from utils.chat_handler import handle_ai_response
import uuid
import requests

# Page config
st.set_page_config(page_title="ODYN Ai", layout="centered", initial_sidebar_state="collapsed")

# Init session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "is_thinking" not in st.session_state:
    st.session_state.is_thinking = False

# Styles + Fonts
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;600&display=swap" rel="stylesheet">
<style>
    html, body, .stApp {
        background-color: #154069 !important;
        color: #F4F7FA !important;
        font-family: 'Noto Sans', sans-serif !important;
    }

    .top-bar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 60px;
        background-color: #1e507c;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 24px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.25);
        z-index: 10000;
    }

    .top-bar .left {
        font-weight: bold;
    }

    .top-bar .right {
        font-size: 14px;
        opacity: 0.8;
    }

    .block-container {
        padding-top: 100px !important;
        padding-bottom: 100px;
        max-width: 720px;
        margin: auto;
    }

    .hero {
        text-align: center;
        margin-top: 40px;
        margin-bottom: 30px;
    }

    .hero h1 {
        margin: 0;
        color: white;
    }

    .hero p {
        color: #B0C4D9;
    }

    .message-block {
        margin: 20px 0;
        line-height: 1.65;
        font-size: 16px;
    }

    .you {
        background-color: #DCE6F2;
        color: #0D1C2E;
        border-radius: 12px;
        padding: 18px 20px;
        text-align: right;
    }

    .odyn {
        color: #F4F7FA;
        text-align: left;
    }

    .label {
        font-size: 0.85rem;
        font-weight: 600;
        opacity: 0.7;
        margin-bottom: 6px;
    }

    .chat-input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: #154069;
        padding: 1rem 2rem;
        box-shadow: 0 -2px 8px rgba(0,0,0,0.2);
        z-index: 999;
    }

    .chat-form input {
        background-color: #fff !important;
        color: #111 !important;
        border-radius: 6px;
        padding: 12px 14px;
        font-size: 15px;
        width: 100%;
    }

    .chat-form button {
        border-radius: 6px;
        background-color: #0b2e4d;
        color: white;
        font-weight: 600;
        padding: 10px 16px;
        margin-top: 10px;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# ✅ Top Nav Bar
st.markdown("""
<div class="top-bar">
    <div class="left">Menu</div>
    <div class="right">🧠 Inventory Intelligence</div>
</div>
""", unsafe_allow_html=True)

# ✅ SVG Logo + Hero Title
st.markdown("""
<div class="hero">
    <div style="margin-bottom: 20px;">
        <!-- SVG LOGO -->
        <svg xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 273.42 72.21" style="width: 260px; height: auto; margin: auto;">
            <g id="Layer_2" data-name="Layer 2">
                <g id="Layer_1-2" data-name="Layer 1">
                    <path fill="#fff" d="M0,70l1.44-1.71A6.3,6.3,0,0,0,5.75,70c1.48,0,2.42-.68,2.42-1.71v0c0-1-.55-1.5-3.08-2.09C2.18,65.5.55,64.64.55,62.13v0c0-2.34,2-4,4.66-4a7.55,7.55,0,0,1,5,1.71L8.87,61.66a6.17,6.17,0,0,0-3.7-1.41c-1.41,0-2.23.73-2.23,1.62v0c0,1.05.63,1.52,3.24,2.15,2.89.7,4.39,1.73,4.39,4v0c0,2.56-2,4.08-4.88,4.08A8.38,8.38,0,0,1,0,70Z"/>
                    <path fill="#fff" d="M32.36,23.12c-5.07,0-8.74-4.24-8.74-9.46s3.67-9.39,8.74-9.39a10.54,10.54,0,0,1,7.42,3.3l3-3.45A13.83,13.83,0,0,0,32.4,0,13.41,13.41,0,0,0,18.74,13.73,13.33,13.33,0,0,0,32.21,27.39,13.67,13.67,0,0,0,43,22.7l-3-3c-2.27,2.12-4.35,3.45-7.61,3.45Z"/>
                </g>
            </g>
        </svg>
    </div>
    <h1>ODYN Ai</h1>
    <p>Know what the state of your stock is.</p>
</div>
""", unsafe_allow_html=True)

# ✅ Main content container
with st.container():
    st.markdown('<div class="block-container">', unsafe_allow_html=True)

    # 💬 Render chat messages
    for role, msg in st.session_state.messages:
        if role == "user":
            st.markdown(f"""
                <div class="message-block you">
                    <div class="label">You</div>
                    <div class="message-text">{msg}</div>
                </div>
            """, unsafe_allow_html=True)
        elif role == "bot":
            st.markdown(f"""
                <div class="message-block odyn">
                    <div class="label">Odyn</div>
            """, unsafe_allow_html=True)
            st.markdown(msg)
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ✏️ Input form (floating bottom)
with st.container():
    st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input(
            "", placeholder="Let me help you find the right information...",
            label_visibility="collapsed"
        )
        submitted = st.form_submit_button("Send")
    st.markdown("</div>", unsafe_allow_html=True)

# ⏎ Handle submission
if submitted and user_input:
    st.session_state.messages.append(("user", user_input))
    st.session_state.is_thinking = True
    st.rerun()

# 🤖 Trigger ODYN reply
if st.session_state.is_thinking:
    with st.spinner("Odyn is thinking..."):
        try:
            handle_ai_response()
        except Exception as e:
            st.session_state.messages.append(("bot", f"💥 Error talking to Odyn: {str(e)}"))
        finally:
            st.session_state.is_thinking = False

# ⬇️ Auto scroll
st.markdown("""
<script>
    const container = window.parent.document.querySelector('.block-container');
    if (container) {
        container.scrollTo({ top: container.scrollHeight, behavior: 'smooth' });
    }
</script>
""", unsafe_allow_html=True)
