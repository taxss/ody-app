import streamlit as st
from utils.chat_handler import handle_ai_response
from utils.theme import apply_theme  # Optional: enable if using theme switcher
import uuid
import requests

# Page config
st.set_page_config(page_title="ORYN Ai", layout="centered", initial_sidebar_state="collapsed")

# Apply optional theme switch
# apply_theme()  # Uncomment if you want the light/dark mode switch

# Custom Styling
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;600&display=swap" rel="stylesheet">
    <style>
        html, body, .stApp {
            background-color: #154069 !important;
            color: #F4F7FA !important;
            font-family: 'Noto Sans', sans-serif !important;
            font-size: 15px !important;
        }

        .block-container {
            padding: 3rem 2rem 8rem 2rem;
            max-width: 720px;
            margin: auto;
        }

        .app-title {
            text-align: center;
            padding: 2.5em 0 0.5em 0;
        }

        .app-subtitle {
            text-align: center;
            color: #B0C4D9;
            font-size: 0.95em;
            margin-bottom: 2em;
        }

        .message-block {
            margin: 20px 0;
            line-height: 1.65;
        }

        .you {
            background-color: #DCE6F2;
            color: #0D1C2E;
            border-radius: 12px;
            padding: 16px 18px;
            text-align: right;
        }

        .odyn {
            color: #F4F7FA;
            text-align: left;
        }

        .label {
            font-size: 14px;
            font-weight: 600;
            opacity: 0.65;
            margin-bottom: 6px;
        }

        .message-text {
            margin-top: 6px;
        }

        .stExpander {
            background-color: #1e507c !important;
            border-radius: 8px;
        }

        .chat-input-container {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background-color: #154069;
            padding: 1rem 2rem;
            box-shadow: 0 -2px 8px rgba(0,0,0,0.2);
        }

        .chat-form input,
        .chat-form button,
        .message-block,
        .message-text,
        .label {
            font-family: 'Noto Sans', sans-serif !important;
            font-size: 15px !important;
        }

        .chat-form input {
            background-color: #fff !important;
            color: #111 !important;
            border-radius: 6px;
            padding: 10px 12px;
            width: 100%;
        }

        .chat-form button {
            border-radius: 6px;
            background-color: #0b2e4d;
            color: white;
            font-weight: 600;
            padding: 9px 14px;
            margin-top: 10px;
            width: 100%;
        }
    </style>
""", unsafe_allow_html=True)



# Header
st.markdown("""
    <div class="app-title">
        <img src="https://images.prismic.io/icelandic/dca19f53-0f5e-4a8c-857e-c4a14211aa40_icelandic_corporate_logo_01.png?auto=compress,format" width="280">
        <h1 style="color:white;">ORYN Ai</h1>
    </div>
    <div class="app-subtitle">Know what the state of your stock is.</div>
""", unsafe_allow_html=True)

# Init session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "is_thinking" not in st.session_state:
    st.session_state.is_thinking = False

# 📬 Email Subscribe
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
                st.warning("Subscription webhook not configured.")

# 💬 Chat messages
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
                <div class="label">Oryn</div>
        """, unsafe_allow_html=True)
        st.markdown(msg, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ✏️ Chat Input
with st.container():
    st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("", placeholder="e.g stock of salmon over 180 days old....", label_visibility="collapsed")
        submitted = st.form_submit_button("Send")
    st.markdown("</div>", unsafe_allow_html=True)

# ⏎ On Submit
if submitted and user_input.strip():
    st.session_state.messages.append(("user", user_input.strip()))
    st.session_state.is_thinking = True
    st.rerun()

# 🤖 Trigger AI
if st.session_state.is_thinking:
    with st.spinner("Oryn is thinking..."):
        handle_ai_response()

# ⬇️ Auto Scroll
st.markdown("""
    <script>
        const container = window.parent.document.querySelector('.block-container');
        if (container) {
            container.scrollTo({ top: container.scrollHeight, behavior: 'smooth' });
        }
    </script>
""", unsafe_allow_html=True)
