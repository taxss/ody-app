import streamlit as st

def apply_theme():
    mode = st.radio("Theme", ["Dark", "Light"], horizontal=True)
    dark = mode == "Dark"

    # Theme colors
    st.session_state["theme"] = {
        "bg": "#121212" if dark else "#FFFFFF",
        "text": "#F5F5F5" if dark else "#111111",
        "card_bg": "#1E1E1E" if dark else "#f0f0f0",
        "link": "#4EA8DE" if dark else "#1a0dab",
        "user-bg": "#2E2E2E" if dark else "#E6E6E6",
        "bot-bg": "#333333" if dark else "#F1F0F0"
    }

    st.markdown(f"""
        <style>
            :root {{
                --bg: {st.session_state["theme"]["bg"]};
                --text: {st.session_state["theme"]["text"]};
                --user-bg: {st.session_state["theme"]["user-bg"]};
                --bot-bg: {st.session_state["theme"]["bot-bg"]};
                --link: {st.session_state["theme"]["link"]};
            }}
            body {{
                background-color: var(--bg);
                color: var(--text);
            }}
        </style>
    """, unsafe_allow_html=True)
