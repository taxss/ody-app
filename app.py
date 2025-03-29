import streamlit as st
import requests

# App config
st.set_page_config(page_title="ODY Chatbot", layout="centered")

# Header
st.title("🤖 ODY Chatbot")
st.subheader("Ask me anything about IHC companies")

# User input
user_query = st.text_input("Enter your query:", placeholder="e.g., Who is the CEO of Esyasoft?")

# Button to trigger AI response
if st.button("🔍 Search") and user_query:
    with st.spinner("ODY is thinking..."):
        # Replace this with your actual AI-n8n endpoint
        AI_ENDPOINT_URL = "YOUR_N8N_WEBHOOK_URL"
        
        # Call AI to get structured response
        response = requests.post(AI_ENDPOINT_URL, json={"query": user_query})

        if response.ok:
            data = response.json()
            
            # Display structured output
            st.success("Here's what I found:")

            st.markdown(f"**Company Name:** {data.get('company_name', 'N/A')}")
            st.markdown(f"**Location:** {data.get('place', 'N/A')}")
            st.markdown(f"**Principal Activities:** {data.get('principal_activities', 'N/A')}")
            st.markdown(f"**Industry:** {data.get('industry', 'N/A')}")

            if data.get('website_url'):
                st.markdown(f"**Website:** [Link]({data['website_url']})")
            else:
                st.markdown("**Website:** N/A")

            # Optional IDs
            with st.expander("🔑 Company IDs"):
                st.write(f"**Company ID:** {data.get('company_id', 'N/A')}")
                parent = data.get('parent_company_id', 'N/A') or 'N/A'
                st.write(f"**Parent Company ID:** {parent}")

        else:
            st.error("Failed to fetch details from AI service.")
