import streamlit as st

def apply_theme():
    mode = st.radio("Theme", ["Light", "Dark"], horizontal=True)
    dark = mode == "Dark"

    st.session_state["theme"] = {
        "bg": "#FFFFFF" if not dark else "#121212",
        "text": "#111111" if not dark else "#F5F5F5",
        "user-bg": "#F0F0F0" if not dark else "#2A2A2A",
        "bot-bg": "#F6F6F6" if not dark else "#1E1E1E"
    }

    theme = st.session_state["theme"]

    st.markdown(f"""
        <style>
            :root {{
                --bg: {theme['bg']};
                --text: {theme['text']};
                --user-bg: {theme['user-bg']};
                --bot-bg: {theme['bot-bg']};
            }}
        </style>
    """, unsafe_allow_html=True)
