import streamlit as st
import json
import requests

def safe_get(data, key):
    return data.get(key) or "Unknown"

def handle_ai_response():
    try:
        url = st.secrets["webhooks"]["ai_url"]
        query = st.session_state.messages[-1][1]
        session_id = st.session_state.session_id

        response = requests.post(url, json={"query": query, "session_id": session_id})
        content = response.json().get("output", "").replace("\\n", "\n")
        parsed = None
        intro_text = content

        try:
            start = content.find('{')
            end = content.rfind('}') + 1
            if start != -1 and end != -1:
                json_part = content[start:end]
                parsed = json.loads(json_part)
                intro_text = content[:start].strip()
        except json.JSONDecodeError:
            pass

        if parsed:
            if intro_text:
                st.session_state.messages.append(("bot", intro_text))

            output_type = parsed.get("type")

            if output_type == "text":
                st.session_state.messages.append(("bot", parsed.get("content", "")))

            elif output_type == "company_card":
                html = f"""
                    <div style='background-color:var(--user-bg); padding:18px; border-radius:12px;'>
                        <h4 style='color:var(--link);'>{safe_get(parsed, "company_name")}</h4>
                        <p><strong>Location:</strong> {safe_get(parsed, "place")}</p>
                        <p><strong>Industry:</strong> {safe_get(parsed, "industry")}</p>
                        <p><strong>Activities:</strong> {safe_get(parsed, "activities")}</p>
                        <p><strong>Website:</strong> <a href="{safe_get(parsed, "website")}" style="color:var(--link);">{safe_get(parsed, "website")}</a></p>
                    </div>
                """
                st.session_state.messages.append(("card", html))

            elif output_type == "table":
                headers = parsed.get("columns", [])
                rows = parsed.get("rows", [])
                table_data = [dict(zip(headers, row)) for row in rows]
                st.table(table_data)

        else:
            st.session_state.messages.append(("bot", intro_text))

    except Exception as e:
        st.error(f"💥 Error: {str(e)}")
    finally:
        st.session_state.is_thinking = False
        st.rerun()
