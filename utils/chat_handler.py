import streamlit as st
import requests
import json

def handle_ai_response():
    ai_url = st.secrets.get("ai_url")
    if not ai_url:
        st.error("❌ AI URL is missing in secrets!")
        return

    user_query = st.session_state.messages[-1][1]

    try:
        response = requests.post(ai_url, json={
            "query": user_query,
            "session_id": st.session_state.session_id
        })

        if response.ok:
            result = response.json()
            content = result.get("output", "").replace("\\n", "\n")
            st.session_state.messages.append(("bot", content))
        else:
            st.error(f"❌ AI server error: {response.status_code}")
            st.text(response.text)

    except Exception as e:
        st.error(f"💥 Error contacting AI server: {str(e)}")
