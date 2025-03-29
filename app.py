import streamlit as st
import requests

st.set_page_config(page_title="Company Info", layout="centered")
st.title("📌 Company Information")

N8N_WEBHOOK_URL = "YOUR_N8N_WEBHOOK_URL"

def fetch_company_data():
    try:
        response = requests.get(N8N_WEBHOOK_URL)
        response.raise_for_status()
        return response.json()
    except:
        return None

if st.button("🔄 Load Company Data"):
    with st.spinner("Fetching from n8n..."):
        data = fetch_company_data()

        if data:
            st.success("✅ Data successfully loaded!")

            st.header(data.get('company_name', 'N/A'))
            st.markdown(f"""
                - **📍 Location:** {data.get('place', 'N/A')}
                - **⚙️ Activities:** {data.get('principal_activities', 'N/A')}
                - **🏷️ Industry:** {data.get('industry', 'N/A')}
                - **🔗 Website:** [{data.get('website_url', 'N/A')}]({data.get('website_url', '#')})
            """)

            with st.expander("Show Company IDs"):
                st.write("**Company ID:**", data.get('company_id', 'N/A'))
                st.write("**Parent Company ID:**", data.get('parent_company_id', 'N/A'))

        else:
            st.error("❌ Error fetching data. Check webhook URL.")
