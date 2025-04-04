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
    <div class="left">Menu Placeholder</div>
    <div class="right">🧠 Inventory Intelligence</div>
</div>
""", unsafe_allow_html=True)

# ✅ SVG LOGO + TITLE CENTER
