import streamlit as st
import requests
import uuid
import json
import networkx as nx
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="ODY Chatbot", layout="centered")

# Logo and title
st.markdown("""
    <div style="text-align: center;">
        <img src="https://companiesmarketcap.com/img/company-logos/256/IHC.AE.png" width="60">
        <h1 style="margin-bottom: 0;">ODY Chatbot</h1>
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
        st.markdown(f"<div style='text-align: right; background-color:#DCF8C6; padding:10px; border-radius:10px; margin:5px 0;'>{msg}</div>", unsafe_allow_html=True)
    elif role == 'bot':
        st.markdown(f"<div style='text-align: left; background-color:#F1F0F0; padding:10px; border-radius:10px; margin:5px 0;'>{msg}</div>", unsafe_allow_html=True)
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
                        <div style='border:1px solid #ccc; padding:15px; border-radius:10px; background:#fff;'>
                            <h4>{parsed['company_name']}</h4>
                            <p><strong>ID:</strong> {parsed['company_id']}</p>
                            <p><strong>Location:</strong> {parsed['place']}</p>
                            <p><strong>Industry:</strong> {parsed['industry']}</p>
                            <p><strong>Activities:</strong> {parsed['activities']}</p>
                            <p><strong>Website:</strong> <a href="{parsed['website']}" target="_blank">{parsed['website']}</a></p>
                            <p><strong>Parent:</strong> {parsed['parent_company']['name']} (ID: {parsed['parent_company']['id']})</p>
                        </div>
                        """
                        st.session_state.messages.append(('card', html))

                    elif output_type == "company_grid":
                        cols = st.columns(min(len(parsed['companies']), 3))
                        for i, company in enumerate(parsed['companies']):
                            with cols[i % len(cols)]:
                                st.markdown(f"""
                                    <div style='border:1px solid #ddd; padding:10px; border-radius:10px;'>
                                        <h5>{company['name']}</h5>
                                        <p><strong>Country:</strong> {company['country']}</p>
                                        <p><strong>Industry:</strong> {company['industry']}</p>
                                        <p>{company['activities']}</p>
                                        <p><a href='{company['website']}' target='_blank'>Website</a></p>
                                    </div>
                                """, unsafe_allow_html=True)

                    elif output_type == "table":
                        headers = parsed.get("columns", [])
                        rows = parsed.get("rows", [])
                        table_data = [dict(zip(headers, row)) for row in rows]
                        st.session_state.messages.append(('table', table_data))

                    elif output_type == "connection_graph":
                        G = nx.DiGraph()
                        for node in parsed["nodes"]:
                            G.add_node(node)
                        for edge in parsed["edges"]:
                            G.add_edge(*edge)
                        fig, ax = plt.subplots()
                        pos = nx.spring_layout(G)
                        nx.draw(G, pos, with_labels=True, node_color="#AED6F1", node_size=2000, font_size=10, arrows=True, ax=ax)
                        st.session_state.messages.append(('graph', fig))

                    else:
                        st.session_state.messages.append(("bot", content))
                else:
                    st.session_state.messages.append(("bot", content))

                st.rerun()
            else:
                st.error(f"Error {response.status_code}: {response.text}")
        except Exception as e:
            st.error(f"Error: {str(e)}")
