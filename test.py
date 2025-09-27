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

# --- CUSTOM CSS FOR BRANDING ---
st.markdown("""
<style>
/* Page background */
.stApp {
    background-color: #FFFFFF;
    color: #001965;
}

/* Header */
.header-title {
    color: #FFFFFF;
    background-color: #001965;
    padding: 15px;
    border-radius: 8px;
}

/* Chat bubbles */
.user-msg {
    background-color: #E6F0FF; /* Science Blue tint */
    color: #001965;
    padding: 10px 15px;
    border-radius: 12px;
    margin: 5px 0px;
    text-align: left;
}

.ai-msg {
    background-color: #001965; /* Midnight Blue */
    color: #FFFFFF;
    padding: 10px 15px;
    border-radius: 12px;
    margin: 5px 0px;
    text-align: left;
}

textarea {
    border-radius: 8px;
    border: 1px solid #005AD2;
    padding: 10px;
}

div.stButton > button {
    background-color: #005AD2;
    color: #FFFFFF;
    height: 40px;
    width: 200px;
    border-radius: 8px;
    border: none;
    font-size: 16px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# --- HEADER WITH LOGO AND TITLE ---
col1, col2 = st.columns([1, 6])

with col1:
    st.image("image.png", width=80)

with col2:
    st.markdown("""
    <div class="header-title">
        <h1 style="margin:0;">📑 Audit Buddy </h1>
        <p style="margin:0; font-size: 16px;">Ask questions and get AI-powered answers from your audit knowledge base.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- USER INPUT ---
query = st.text_area("💬 Enter your question here:", height=120)

# --- SUBMIT BUTTON ---
if st.button("🔍 Get Answer"):
    if query.strip() == "":
        st.warning("⚠️ Please enter a question.")
    else:
        with st.spinner("🤖 Thinking..."):
            try:
                # Call your webhook
                response = requests.post(
                    "https://aruna78.app.n8n.cloud/webhook-test/audit-buddy",
                    json={"query": query},
                    timeout=30
                )

                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("answer", "No answer received.")
                    
                    # Append messages to session state
                    st.session_state.messages.insert(0, {"role": "AI", "text": answer})
                    st.session_state.messages.insert(0, {"role": "user", "text": query})
                else:
                    st.error(f"❌ Error: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"⚠️ Connection error: {e}")

# --- DISPLAY CHAT ---
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-msg">💬 {msg["text"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai-msg">🤖 {msg["text"]}</div>', unsafe_allow_html=True)
