import streamlit as st
import requests

# Page config
st.set_page_config(page_title="ODY Chatbot", layout="centered")

# Insert custom CSS directly here
custom_css = """
<style>
body, .stApp {
    background-color: #ffffff;
    color: #333333;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

h1, h2, h3 {
    color: #1f2937;
}

.stButton button {
    background-color: #1f2937;
    color: white;
    border-radius: 8px;
    padding: 8px 16px;
}

.stButton button:hover {
    background-color: #374151;
    color: white;
}

.stTextInput input {
    border-radius: 8px;
}

[data-testid="stExpander"] {
    border-radius: 8px;
    background-color: #f9fafb;
}

[data-testid="stSidebar"] {
    background-color: #ffffff;
}
</style>
"""
# Include the CSS in your app
st.markdown(custom_css, unsafe_allow_html=True)
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
        AI_ENDPOINT_URL = "Yfc4d4829-f74d-42d9-9dd7-103fd2ecdb1c"
        
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

