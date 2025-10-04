import streamlit as st
import requests

st.set_page_config(layout="wide", page_title="Audit Bud", page_icon=":page_facing_up:")

# Sidebar: user question input and send button
with st.sidebar:
    st.markdown("### Audit Bud")
    st.markdown("Your Automated Audit Readiness Assistant")
    st.divider()
    st.info("I'm ready to answer questions about your audit documents.")
    chat = st.text_input("Ask a question...", key="chat_input")
    submitted = st.button("Send")

# Initialize session state to hold response data
if 'reply' not in st.session_state:
    st.session_state.reply = ""
if 'document_details' not in st.session_state:
    st.session_state.document_details = {
        "documentId": "",
        "version": "",
        "status": "",
        "effectiveDate": "",
        "author": "",
        "approvers": "",
    }

if submitted and chat:
    webhook_url = "https://aruna78.app.n8n.cloud/webhook/auditbud"
    response = requests.post(webhook_url, json={"question": chat})
    if response.status_code == 200:
        data = response.json()
        st.session_state.reply = data.get("reply", "")
        doc = data.get("documentDetails", {})
        st.session_state.document_details["documentId"] = doc.get("documentId", "")
        st.session_state.document_details["version"] = doc.get("version", "")
        st.session_state.document_details["status"] = doc.get("status", "")
        st.session_state.document_details["effectiveDate"] = doc.get("effectiveDate", "")
        st.session_state.document_details["author"] = doc.get("author", "")
        st.session_state.document_details["approvers"] = ", ".join(doc.get("approvers", []))
        st.sidebar.success("Question sent and response received!")
    else:
        st.sidebar.error(f"Failed to send! Status code: {response.status_code}")

# Layout
col1, col2 = st.columns([2, 3])

with col1:
    if st.session_state.reply:
        st.markdown("### Response from n8n")
        st.info(st.session_state.reply)
    else:
        st.empty()

with col2:
    st.markdown("#### Document Details")
    c1, c2 = st.columns(2)
    with c1:
        st.text_input("Document ID", value=st.session_state.document_details["documentId"])
    with c2:
        st.text_input("Version", value=st.session_state.document_details["version"])
    c3, c4 = st.columns(2)
    with c3:
        st.text_input("Status", value=st.session_state.document_details["status"])
    with c4:
        st.text_input("Effective Date", value=st.session_state.document_details["effectiveDate"])
    st.text_input("Author", value=st.session_state.document_details["author"])
    st.text_input("Approvers", value=st.session_state.document_details["approvers"])

hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
