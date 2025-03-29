import streamlit as st
import requests
import uuid
import json

# Page config
st.set_page_config(page_title="ODY Chatbot", layout="centered")

# Dark/Light mode toggle
mode = st.sidebar.radio("Theme", ["Dark", "Light"])
dark_mode = mode == "Dark"

bg_color = "#121212" if dark_mode else "#FFFFFF"
text_color = "#F5F5F5" if dark_mode else "#111111"
card_bg = "#1E1E1E" if dark_mode else "#f0f0f0"
link_color = "#4EA8DE" if dark_mode else "#1a0dab"
user_bg = "#2E2E2E" if dark_mode else "#E6E6E6"
bot_bg = "#333333" if dark_mode else "#F1F0F0"

# Logo and title
st.markdown(f"""
    <div style="text-align: center; background-color: {bg_color}; padding: 1em; border-radius: 10px;">
        <img src="https://companiesmarketcap.com/img/company-logos/256/IHC.AE.png" width="60">
        <h1 style="margin-bottom: 0; color:{text_color};">ODY Chatbot</h1>
        <p style="color: gray;">Your gateway to IHC insights</p>
    </div>
""", unsafe_allow_html=True)

# Session state init
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Chat message display
for role, msg in st.session_state.messages:
    if role == 'user':
        st.markdown(f"<div style='text-align: right; background-color:{user_bg}; padding:12px 16px; border-radius:16px; margin:6px 0; font-size:15px; color:{text_color};'>{msg}</div>", unsafe_allow_html=True)
    elif role == 'bot':
        st.markdown(f"<div style='text-align: left; background-color:{bot_bg}; padding:12px 16px; border-radius:16px; margin:6px 0; font-size:15px; line-height:1.6; color:{text_color};'>{msg}</div>", unsafe_allow_html=True)
    elif role == 'card':
        st.markdown(msg, unsafe_allow_html=True)
    elif role == 'table':
        st.table(msg)
    elif role == 'graph':
        st.pyplot(msg)

# Input form
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("", placeholder="Ask ODY about IHC...", label_visibility="collapsed")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    st.session_state.messages.append(('user', user_input))

    with st.spinner("ODY is thinking..."):
        AI_ENDPOINT_URL = "https://timoleon.app.n8n.cloud/webhook/fc4d4829-f74d-42d9-9dd7-103fd2ecdb1c"
        try:
            response = requests.post(AI_ENDPOINT_URL, json={
                "query": user_input,
                "session_id": st.session_state.session_id
            })

            if response.ok:
                result = response.json()
                content = result.get("output", "No response provided.").replace("\\n", "\n")

                # Try to parse JSON inside the content
                parsed = None
                try:
                    parsed = json.loads(content.split("```json")[-1].split("```")[-2])
                except:
                    pass

                if parsed and isinstance(parsed, dict):
                    output_type = parsed.get("type")

                    if output_type == "text":
                        st.session_state.messages.append(("bot", parsed.get("content", "")))

                    elif output_type == "company_card":
                        html = f"""
                        <div style='border:1px solid #666; padding:18px 20px; border-radius:12px; background-color:{card_bg}; color:{text_color}; font-family:sans-serif; line-height:1.6; font-size:15px;'>
                            <h4 style='margin-top: 0; color:{link_color}; font-size:18px;'>{parsed['company_name']}</h4>
                            <p><strong>ID:</strong> {parsed['company_id']}</p>
                            <p><strong>Location:</strong> {parsed['place']}</p>
                            <p><strong>Industry:</strong> {parsed['industry']}</p>
                            <p><strong>Activities:</strong> {parsed['activities']}</p>
                            <p><strong>Website:</strong> <a href="{parsed['website']}" target="_blank" style="color:{link_color};">{parsed['website']}</a></p>
                            <p><strong>Parent:</strong> {parsed['parent_company']['name']} (ID: {parsed['parent_company']['id']})</p>
                        </div>
                        """
                        st.session_state.messages.append(('card', html))

                    elif output_type == "company_grid":
                        cols = st.columns(min(len(parsed['companies']), 3))
                        for i, company in enumerate(parsed['companies']):
                            with cols[i % len(cols)]:
                                st.markdown(f"""
                                    <div style='border:1px solid #ddd; padding:14px; border-radius:12px; font-size:14px; background-color:{card_bg}; color:{text_color};'>
                                        <h5 style='margin-top:0; color:{link_color};'>{company['name']}</h5>
                                        <p><strong>Country:</strong> {company['country']}</p>
                                        <p><strong>Industry:</strong> {company['industry']}</p>
                                        <p>{company['activities']}</p>
                                        <p><a href='{company['website']}' target='_blank' style='color:{link_color};'>Website</a></p>
                                    </div>
                                """, unsafe_allow_html=True)

                    elif output_type == "table":
                        headers = parsed.get("columns", [])
                        rows = parsed.get("rows", [])
                        table_data = [dict(zip(headers, row)) for row in rows]
                        st.session_state.messages.append(('table', table_data))

                    else:
                        st.session_state.messages.append(("bot", content))
                else:
                    st.session_state.messages.append(("bot", content))

                st.rerun()
            else:
                st.error(f"Error {response.status_code}: {response.text}")
        except Exception as e:
            st.error(f"Error: {str(e)}")
