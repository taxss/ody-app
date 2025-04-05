import streamlit as st
import requests
import json

def handle_ai_response():
    ai_url = st.secrets.get("ai_url")

    if not ai_url:
        st.error("❌ AI URL is missing.")
        return

    # Get last user query
    user_query = next((msg[1] for msg in reversed(st.session_state.messages) if msg[0] == "user"), None)

    if not user_query or not user_query.strip():
        st.warning("⚠️ No user query found.")
        return

    try:
        # Send request to AI backend
        response = requests.post(
            ai_url,
            json={
                "query": user_query,
                "session_id": st.session_state.session_id
            },
            timeout=90
        )

        # ✅ Remove "Ody is typing..." placeholder if it's still there
        if st.session_state.messages and st.session_state.messages[-1][1].startswith("⌛"):
            st.session_state.messages.pop()

        if response.ok:
            try:
                result = response.json()
                content = result.get("output", "").replace("\\n", "\n").strip()

                if content:
                    st.session_state.messages.append(("bot", content))
                else:
                    st.session_state.messages.append(("bot", "🤖 ODY didn’t return any content."))
            except json.JSONDecodeError:
                st.session_state.messages.append(("bot", "❌ ODY returned malformed response."))
        else:
            st.session_state.messages.append(("bot", f"❌ ODY server error: {response.status_code}"))
            st.text(response.text)

    except Exception as e:
        st.session_state.messages.append(("bot", f"💥 ODY crashed: {str(e)}"))

    # ✅ Reset state + rerun
    st.session_state.is_thinking = False
    st.rerun()
