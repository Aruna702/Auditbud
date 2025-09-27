import streamlit as st
import requests

# --- PAGE CONFIG ---
st.set_page_config(page_title="Audit Buddy", page_icon="📑", layout="centered")

# --- APP TITLE ---
st.title("📑 Audit Buddy")
st.caption("Ask questions and get AI-powered answers from your audit knowledge base.")

# --- USER INPUT ---
query = st.text_area("Enter your question here:", height=100)

# --- SUBMIT BUTTON ---
if st.button("🔍 Get Answer"):
    if query.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            try:
                # Send query to n8n webhook
                response = requests.post(
                    "https://aruna78.app.n8n.cloud/webhook-test/audit-buddy",
                    json={"query": query},
                    timeout=30
                )

                if response.status_code == 200:
                    data = response.json()
                    st.markdown("###  Answer:")
                    st.write(data.get("answer", "No answer received."))
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Connection error: {e}")
