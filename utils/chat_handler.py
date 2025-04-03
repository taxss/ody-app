import streamlit as st
import requests
import json

def handle_ai_response():
    ai_url = st.secrets.get("ai_url")

    if not ai_url:
        st.error("❌ AI URL is missing.")
        return

    # Get the last user message safely
    user_query = next((msg[1] for msg in reversed(st.session_state.messages) if msg[0] == "user"), None)
    if not user_query:
        st.warning("⚠️ No user query found.")
        return

    try:
        # Send user query to AI endpoint
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
                st.session_state.messages.append(("bot", "❌ ODY sent something I couldn’t understand."))
        else:
            st.session_state.messages.append(("bot", f"❌ ODY server error: {response.status_code}"))
            st.text(response.text)

    except Exception as e:
        st.session_state.messages.append(("bot", f"💥 ODY crashed: {str(e)}"))

    # ✅ Force rerun so bot message appears immediately
    st.session_state.is_thinking = False
    st.rerun()
