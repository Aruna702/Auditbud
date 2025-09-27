import streamlit as st
import requests

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Audit Buddy",
    page_icon="📑",
    layout="wide"
)

# --- SESSION STATE TO STORE CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- CUSTOM CSS ---
st.markdown("""
<style>
.stApp {
    display: flex;
    flex-direction: column;
    height: 100vh;
}
.chat-container {
    flex: 1;
    overflow-y: auto;
    padding: 1rem;
}
.input-container {
    position: sticky;
    bottom: 0;
    background-color: white;
    padding: 1rem;
    border-top: 1px solid #ddd;
}
.user-msg {
    background-color: #E6F0FF;
    color: #001965;
    padding: 10px 15px;
    border-radius: 12px;
    margin: 5px 0;
    text-align: left;
    width: fit-content;
    max-width: 80%;
}
.ai-msg {
    background-color: #001965;
    color: #FFFFFF;
    padding: 10px 15px;
    border-radius: 12px;
    margin: 5px 0;
    text-align: left;
    width: fit-content;
    max-width: 80%;
}
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
<div style="background-color:#001965;color:white;padding:15px;border-radius:8px;margin-bottom:10px;">
  <h2 style="margin:0;">📑 Audit Buddy</h2>
  <p style="margin:0;font-size:16px;">Ask questions and get AI-powered answers from your audit knowledge base.</p>
</div>
""", unsafe_allow_html=True)

# --- INPUT AREA ---
st.markdown('<div class="input-container">', unsafe_allow_html=True)
query = st.text_area("💬 Type your message...", height=80, label_visibility="collapsed")

if st.button("🔍 Send"):
    if query.strip():
        # Append user message immediately
        st.session_state.messages.append({"role": "user", "text": query})

        with st.spinner("🤖 Thinking..."):
            try:
                response = requests.post(
                    "https://aruna78.app.n8n.cloud/webhook/audit-buddy",  # ✅ use production webhook
                    json={"query": query},
                    timeout=30
                )

                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("answer", "No answer received.")
                    st.session_state.messages.append({"role": "AI", "text": answer})
                else:
                    st.error(f"❌ Error: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"⚠️ Connection error: {e}")
    else:
        st.warning("⚠️ Please enter a question.")
st.markdown('</div>', unsafe_allow_html=True)

# --- CHAT AREA (moved here so it updates after new messages) ---
chat_container = st.container()
with chat_container:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for msg in st.session_state.messages:  # ✅ keep natural order (top to bottom)
        if msg["role"] == "user":
            st.markdown(f'<div class="user-msg">💬 {msg["text"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="ai-msg">🤖 {msg["text"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
