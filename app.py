import streamlit as st
from utils.chat_handler import handle_ai_response
import uuid
import requests

# Page setup
st.set_page_config(page_title="ODYN Ai", layout="centered", initial_sidebar_state="collapsed")

# 🖋 Google Font: Noto Sans
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;600&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# 🧼 Icelandic Visual Styling
st.markdown("""
    <style>
        html, body, .stApp {
            background-color: #154069 !important;
            color: #F4F7FA !important;
            font-family: 'Noto Sans', sans-serif !important;
        }
        .block-container {
            padding: 2rem 2rem;
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
            font-size: 1em;
            margin-bottom: 2em;
        }
        .message-block {
            border-radius: 12px;
            padding: 12px 16px;
            margin: 12px 0;
            line-height: 1.6;
            font-size: 16px;
        }
        .you {
            background-color: #DCE6F2;
            color: #0D1C2E;
            text-align: right;
        }
        .ody {
            background-color: #EAF0F8;
            color: #0D1C2E;
            text-align: left;
        }
        .label {
            font-size: 0.8em;
            font-weight: 600;
            margin-bottom: 4px;
            display: block;
            opacity: 0.6;
        }
        .stTextInput > div > input {
            background-color: #FFFFFF !important;
            color: #111 !important;
            border-radius: 8px;
        }
        .stButton button {
            border-radius: 6px;
            background-color: #154069;
            color: white;
        }
        .stForm {
            margin-top: 2em;
        }
        .stExpander {
            background-color: #1e507c !important;
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# App header
st.markdown("""
    <div class="app-title">
        <img src="https://images.prismic.io/icelandic/dca19f53-0f5e-4a8c-857e-c4a14211aa40_icelandic_corporate_logo_01.png?auto=compress,format" width="280">
        <h1 style="color:white;">ODYN Ai</h1>
    </div>
    <div class="app-subtitle">Know what the state of your stock is.</div>
""", unsafe_allow_html=True)

# Session state setup
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "is_thinking" not in st.session_state:
    st.session_state.is_thinking = False

# 📬 Email subscription
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

# 👤 + 🤖 Display all messages
for role, msg in st.session_state.messages:
    if role == "user":
        st.markdown(f"""
            <div class="message-block you">
                <span class="label">You</span>
                {msg}
            </div>
        """, unsafe_allow_html=True)

    elif role == "bot":
        # Wrap ODYN message AND markdown inside styled bubble
        st.markdown(f"""
            <div class="message-block odyn">
                <span class="label">Odyn</span>
                <div style="margin-top: 8px;">
        """, unsafe_allow_html=True)

        # Markdown-render inside the bubble (indented)
        st.markdown(msg)

        # Close the div
        st.markdown("</div></div>", unsafe_allow_html=True)


# ✏️ Chat input
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input(
        "Ask ODYN something...",
        placeholder="e.g. ESG score of Marel",
        label_visibility="collapsed"
    )
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    st.session_state.messages.append(("user", user_input))
    # ✍️ Add typing indicator
    st.session_state.messages.append(("bot", "⌛ Ody is typing..."))
    st.session_state.is_thinking = True
    st.rerun()

# 🤖 Trigger AI response
if st.session_state.is_thinking:
    with st.spinner("Ody is thinking..."):
        try:
            handle_ai_response()
        except Exception as e:
            st.session_state.messages.append(("bot", f"💥 Error talking to ODY: {str(e)}"))
        finally:
            st.session_state.is_thinking = False

# ⬇️ Auto-scroll to latest message
st.markdown("""
    <script>
        const container = window.parent.document.querySelector('.block-container');
        if (container) {
            container.scrollTo({ top: container.scrollHeight, behavior: 'smooth' });
        }
    </script>
""", unsafe_allow_html=True)
