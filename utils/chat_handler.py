import streamlit as st
import requests
import json

def handle_ai_response():
    ai_url = st.secrets.get("ai_url")
    
    if not ai_url:
        st.error("❌ AI URL is missing from Streamlit secrets.")
        return

    user_query = st.session_state.messages[-1][1]

    try:
        # Send query to AI endpoint
        response = requests.post(ai_url, json={
            "query": user_query,
            "session_id": st.session_state.session_id
        })

        # Log response status
        st.write("🛠️ DEBUG: Response status code:", response.status_code)

        # Check if the request was successful
        if response.ok:
            st.write("🛠️ DEBUG: Raw response text:", response.text)

            try:
                result = response.json()
                content = result.get("output", "").replace("\\n", "\n").strip()

                if content:
                    # Optional: Try to extract and display any JSON card later
                    st.session_state.messages.append(("bot", content))
                    st.write("✅ DEBUG: Parsed bot response:", content)
                else:
                    st.warning("⚠️ ODY responded but didn't send usable content.")
                    st.session_state.messages.append(("bot", "🤖 ODY didn’t send anything back. Try asking again?"))

            except json.JSONDecodeError as e:
                st.error("❌ Failed to parse ODY's response as JSON.")
                st.text(response.text)

        else:
            # Error from AI server
            st.error(f"❌ ODY server error: {response.status_code}")
            st.text(response.text)

    except Exception as e:
        # Network/timeout/general failure
        st.error(f"💥 Exception while contacting ODY: {str(e)}")
