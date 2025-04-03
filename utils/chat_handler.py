import streamlit as st
import requests
import json

def handle_ai_response():
    ai_url = st.secrets.get("ai_url")

    if not ai_url:
        st.error("❌ AI URL is missing from Streamlit secrets.")
        return

    # Safely grab the latest user message
    user_query = next((msg[1] for msg in reversed(st.session_state.messages) if msg[0] == "user"), None)

    if not user_query or not user_query.strip():
        st.warning("⚠️ No user query found to send.")
        return

    try:
        # 🚀 Send the request to ODY with extended timeout
        response = requests.post(
            ai_url,
            json={
                "query": user_query,
                "session_id": st.session_state.session_id
            },
            timeout=30  # ⏱️ increased timeout from default 10s to 30s
        )

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
            # Append readable error message for the user
            st.session_state.messages.append(("bot", f"❌ ODY server error: {response.status_code}"))
            st.text(response.text)

    except Exception as e:
        # Append exception error
        st.session_state.messages.append(("bot", f"💥 Error contacting ODY: {str(e)}"))

    # ✅ Trigger UI refresh so bot message shows up right away
    st.session_state.is_thinking = False
    st.rerun()
