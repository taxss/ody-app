import streamlit as st
import requests
import uuid
import json

# Page config
st.set_page_config(page_title="ODY ai", layout="centered")

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
        <h1 style="margin-bottom: 0; color:{text_color};">ODY Ai</h1>
        <p style="color: gray;">Your gateway to IHC insights</p>
    </div>
""", unsafe_allow_html=True)

# Session state init
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if 'is_thinking' not in st.session_state:
    st.session_state.is_thinking = False

# Chat message display
for role, msg in st.session_state.messages:
    if role == 'user':
        st.markdown(f"<div style='text-align: right; background-color:{user_bg}; padding:12px 16px; border-radius:16px; margin:6px 0; font-size:15px; color:{text_color};'>🧑‍💻 <strong>You:</strong><br>{msg}</div>", unsafe_allow_html=True)
    elif role == 'bot':
        st.markdown(f"<div style='text-align: left; background-color:{bot_bg}; padding:12px 16px; border-radius:16px; margin:6px 0; font-size:15px; line-height:1.6; color:{text_color};'>🤖 <strong>ODY:</strong><br>{msg}</div>", unsafe_allow_html=True)
    elif role == 'card':
        st.markdown(msg, unsafe_allow_html=True)
    elif role == 'table':
        st.table(msg)
    elif role == 'connection_cards':
        st.markdown("<div style='overflow-x: auto; white-space: nowrap;'>", unsafe_allow_html=True)
        for company in msg:
            name = company.get("name", "Unknown")
            place = company.get("place", "Unknown")
            industry = company.get("industry", "Unknown")
            activities = company.get("activities", "Unknown")
            st.markdown(f"""
                <div style='display: inline-block; vertical-align: top; width: 280px; margin: 0 10px 10px 0; border: 1px solid #ccc; border-radius: 12px; background-color: {card_bg}; color: {text_color}; padding: 16px;'>
                    <h5 style='margin-top: 0; color: {link_color};'>{name}</h5>
                    <p><strong>Location:</strong> {place}</p>
                    <p><strong>Industry:</strong> {industry}</p>
                    <p><strong>Activities:</strong> {activities}</p>
                </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# Input form
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("", placeholder="Ask ODY about IHC...", label_visibility="collapsed")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    st.session_state.messages.append(('user', user_input))
    st.session_state.is_thinking = True
    st.rerun()

if st.session_state.is_thinking:
    with st.spinner("ODY is thinking..."):
        ##Ody 1.0
        ##AI_ENDPOINT_URL = "https://timoleon.app.n8n.cloud/webhook/fc4d4829-f74d-42d9-9dd7-103fd2ecdb1c"
        ##Ody 2.0
        AI_ENDPOINT_URL = "https://timoleon.app.n8n.cloud/webhook/99295e6e-0eec-4189-8501-78a425c5ebe0"
        try:
            response = requests.post(AI_ENDPOINT_URL, json={
                "query": st.session_state.messages[-1][1],
                "session_id": st.session_state.session_id
            })

            if response.ok:
                result = response.json()
                content = result.get("output", "No response provided.").replace("\\n", "\n")

                parsed = None
                intro_text = ""
                try:
                    intro_text = content.split("```json")[0].strip()
                    parsed = json.loads(content.split("```json")[1].split("```")[0])
                except:
                    pass

                def safe_get(data, key):
                    return data.get(key) if data.get(key) else "Unknown"

                if parsed and isinstance(parsed, dict):
                    if intro_text:
                        st.session_state.messages.append(("bot", intro_text))

                    output_type = parsed.get("type")

                    if output_type == "text":
                        st.session_state.messages.append(("bot", parsed.get("content", "")))

                    elif output_type == "company_card":
                        html = f"""
                        <div style='border:1px solid #666; padding:18px 20px; border-radius:12px; background-color:{card_bg}; color:{text_color}; font-family:sans-serif; line-height:1.6; font-size:15px;'>
                            <h4 style='margin-top: 0; color:{link_color}; font-size:18px;'>{safe_get(parsed, 'company_name')}</h4>
                            <p><strong>Location:</strong> {safe_get(parsed, 'place')}</p>
                            <p><strong>Industry:</strong> {safe_get(parsed, 'industry')}</p>
                            <p><strong>Activities:</strong> {safe_get(parsed, 'activities')}</p>
                            <p><strong>Website:</strong> <a href="{safe_get(parsed, 'website')}" target="_blank" style="color:{link_color};">{safe_get(parsed, 'website')}</a></p>
                            <p><strong>Parent:</strong> {safe_get(parsed.get('parent_company', {}), 'name')}</p>
                        </div>
                        """
                        st.session_state.messages.append(('card', html))

                    elif output_type == "company_grid":
                        cols = st.columns(min(len(parsed['companies']), 3))
                        for i, company in enumerate(parsed['companies']):
                            with cols[i % len(cols)]:
                                st.markdown(f"""
                                    <div style='border:1px solid #ddd; padding:14px; border-radius:12px; font-size:14px; background-color:{card_bg}; color:{text_color};'>
                                        <h5 style='margin-top:0; color:{link_color};'>{safe_get(company, 'name')}</h5>
                                        <p><strong>Country:</strong> {safe_get(company, 'country')}</p>
                                        <p><strong>Industry:</strong> {safe_get(company, 'industry')}</p>
                                        <p>{safe_get(company, 'activities')}</p>
                                        <p><a href='{safe_get(company, 'website')}' target='_blank' style='color:{link_color};'>Website</a></p>
                                    </div>
                                """, unsafe_allow_html=True)

                    elif output_type == "connection_graph":
                        connection_cards = sorted(parsed.get("nodes", []), key=lambda c: c.get("name", ""))
                        st.session_state.messages.append(('connection_cards', connection_cards))

                    elif output_type == "table":
                        headers = parsed.get("columns", [])
                        rows = parsed.get("rows", [])
                        table_data = [dict(zip(headers, row)) for row in rows]
                        st.session_state.messages.append(('table', table_data))

                    else:
                        st.session_state.messages.append(("bot", content))
                else:
                    # No structured data detected, show content once
                    st.session_state.messages.append(("bot", content.strip()))

                st.session_state.is_thinking = False
                st.rerun()
            else:
                st.session_state.is_thinking = False
                st.error(f"Error {response.status_code}: {response.text}")
        except Exception as e:
            st.session_state.is_thinking = False
            st.error(f"Error: {str(e)}")
