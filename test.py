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
.block-container {
    max-width: 800px;
    margin: auto;
    height: 90vh; /* full app height */
    display: flex;
    flex-direction: column;
}

/* Scrollable chat area */
.chat-container {
    flex: 1;  /* take remaining space */
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

/* Fixed input row */
.input-row {
    background: white;
    padding: 10px;
    border-top: 1px solid #ddd;
}
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
<div class="header" style="background:#001965;color:white;padding:15px;border-radius:8px;margin-bottom:10px;">
  <h2>📑 Audit Buddy</h2>
  <p>Ask questions and get AI-powered answers from your audit knowledge base.</p>
</div>
""", unsafe_allow_html=True)

# --- CHAT HISTORY (scrollable) ---
chat_placeholder = st.container()
with chat_placeholder:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="user-msg">💬 {msg["text"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="ai-msg">🤖 {msg["text"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
# --- AUTO SCROLL TO BOTTOM ---
st.markdown("""
<script>
    var chatBox = window.parent.document.querySelector('.chat-container');
    if (chatBox) {
        chatBox.scrollTop = chatBox.scrollHeight;
    }
</script>
""", unsafe_allow_html=True)

# --- FIXED INPUT BAR ---
st.markdown('<div class="input-row">', unsafe_allow_html=True)
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
        st.session_state.messages.append({"role": "user", "text": query})

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
st.markdown('</div>', unsafe_allow_html=True)
