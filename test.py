import streamlit as st
import requests

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Audit Buddy",
    page_icon="📑",
    layout="wide"
)

# --- SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- CUSTOM CSS ---
st.markdown("""
<style>
/* Center the main content and limit width */
.block-container {
    max-width: 800px;  /* adjust width as needed */
    padding-left: 1rem;
    padding-right: 1rem;
    margin-left: auto;
    margin-right: auto;
    display: flex;
    flex-direction: column;
    height: 90vh; /* take most of screen height */
}

/* Chat wrapper fills available space */
.chat-wrapper {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow-y: auto;
    padding: 1rem;
    border: 1px solid #ddd;
    border-radius: 8px;
    background-color: #f9f9f9;
    margin-bottom: 10px;
}

/* Chat bubbles */
.user-msg, .ai-msg {
    display: inline-block;
    padding: 10px 15px;
    border-radius: 12px;
    margin: 6px 0;
    max-width: 80%;
    word-wrap: break-word;
}

.user-msg {
    background-color: #E6F0FF;
    color: #001965;
    float: right;
    clear: both;
}

.ai-msg {
    background-color: #f0f4ff;
    color: #001965;
    float: left;
    clear: both;
}

/* Input bar pinned at bottom */
.input-row {
    position: sticky;
    bottom: 0;
    background: white;
    padding: 10px;
    border-top: 1px solid #ddd;
    z-index: 10;
}

/* Header styling */
.header {
    background-color:#001965;
    color:white;
    padding:15px;
    border-radius:8px;
    margin-bottom:10px;
}
.header h2 { margin:0; }
.header p { margin:0; font-size:16px; }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
<div class="header">
  <h2>📑 Audit Buddy</h2>
  <p>Ask questions and get AI-powered answers from your audit knowledge base.</p>
</div>
""", unsafe_allow_html=True)

# --- CHAT + INPUT ---
st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-msg">💬 {msg["text"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai-msg">🤖 {msg["text"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- INPUT BAR ---
with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([9, 1])
    with col1:
        query = st.text_input(
            "Type your message",
            key="chat_input",
            placeholder="Type your message here...",
            label_visibility="collapsed"
        )
    with col2:
        submitted = st.form_submit_button("🔍")

    if submitted and query.strip():
        # Save user message
        st.session_state.messages.append({"role": "user", "text": query})

        # Get AI response
        with st.spinner("🤖 Thinking..."):
            try:
                response = requests.post(
                    "https://aruna78.app.n8n.cloud/webhook/audit-buddy",
                    json={"query": query},
                    timeout=30
                )
                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("answer", "No answer received.")
                    st.session_state.messages.append({"role": "AI", "text": answer})
                    st.rerun()
                else:
                    st.error(f"❌ Error: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"⚠️ Connection error: {e}")
