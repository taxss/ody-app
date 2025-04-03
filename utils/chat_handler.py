import streamlit as st
import requests
import json

def handle_ai_response():
    ai_url = st.secrets.get("ai_url")
    
    if not ai_url:
        st.error("❌ AI URL is missing from Streamlit secrets.")
        return

    user_query = next((msg[1] for msg in reversed(st.session_state.messages) if msg[0] == "user"), None)
    if not user_query:
        st.warning("⚠️ No user query found.")
        return

    try:
        response = requests.post(ai_url, json={
            "query": user_query,
            "session_id": st.session_state.session_id
        })

        if response.ok:
            try:
                result = response.json()
                content = result.get("output", "").replace("\\n", "\n").strip()

                if content:
                    st.session_state.messages.append(("bot", content))
                else:
                    st.session_state.messages.append(("bot", "🤖 ODY didn’t send anything back. Try again?"))

            except json.JSONDecodeError:
                st.session_state.messages.append(("bot", "❌ Couldn't read ODY's response (invalid JSON)."))

        else:
            # Append error message to chat cleanly
            st.session_state.messages.append(("bot", "❌ ODY had a problem processing that. Please try again later."))
            st.error(f"ODY server error: {response.status_code}")
            st.text(response.text)

    except Exception as e:
        st.session_state.messages.append(("bot", f"💥 Error talking to ODY: {str(e)}"))
