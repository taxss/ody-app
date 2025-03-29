import streamlit as st
import requests

# Page config (Call this ONLY ONCE at the very top)
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
st.markdown(custom_css, unsafe_allow_html=True)

# Header
st.title("🤖 ODY Chatbot")
st.subheader("Ask me anything about IHC companies")

# User input
user_query = st.text_input("Enter your query:", placeholder="e.g., Who is the CEO of Esyasoft?")

# Button to trigger AI response
if st.button("🔍 Search") and user_query:
    with st.spinner("ODY is thinking..."):
        # Replace this with your actual AI-n8n endpoint (Ensure it's a valid URL)
        AI_ENDPOINT_URL = "https://timoleon.app.n8n.cloud/webhook-test/fc4d4829-f74d-42d9-9dd7-103fd2ecdb1c"
        
        try:
            response = requests.post(AI_ENDPOINT_URL, json={"query": user_query})

            if response.ok:
                result = response.json()
                
                # Display raw response
                st.success("Here's the response from ODY:")
                st.json(result)

            else:
                st.error(f"Failed to fetch details: Status code {response.status_code}")
                st.write(response.text)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
