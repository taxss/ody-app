import streamlit as st
import requests
import json

import streamlit as st
import requests
import json

def handle_ai_response():
    ai_url = st.secrets.get("ai_url")

    if not ai_url:
        st.error("❌ AI URL is missing.")
        return

    # Grab the last user message
    user_query = next((msg[1] for msg in reversed(st.session_state.messages) if msg[0] == "user"), None)

    if not user_query or not user_query.strip():
        st.warning("⚠️ No user query found to send to ODY.")
        return

    # 🔍 DEBUG: Show what's about to be sent
    st.write("📤 Sending to ODY:", user_query)

    try:
        response = requests.post(
            ai_url,
            json={
                "query": user_query,
                "session_id": st.session_state.session_id
            },
            timeout=10
        )

        # Log status code
        st.write("🛠️ ODY responded with status:", response.status_code)

        if response.ok:
            try:
                result = response.json()
                content = result.get("output", "").replace("\\n", "\n").strip()

                # 🔍 DEBUG: Log parsed content
                st.write("📥 ODY replied:", content)

                if content:
                    st.session_state.messages.append(("bot", content))
                else:
                    st.session_state.messages.append(("bot", "🤖 ODY didn't return any message."))

            except json.JSONDecodeError:
                st.session_state.messages.append(("bot", "❌ Couldn't parse ODY's response as JSON."))
        else:
            st.session_state.messages.append(("bot", f"❌ ODY server error: {response.status_code}"))
            st.text(response.text)

    except Exception as e:
        st.session_state.messages.append(("bot", f"💥 Error contacting ODY: {str(e)}"))

    # Finish: Rerun so new message appears
    st.session_state.is_thinking = False
    st.rerun()
