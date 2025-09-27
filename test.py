import streamlit as st
import requests
import streamlit.components.v1 as components
import html as html_module

# --- PAGE CONFIG ---
st.set_page_config(page_title="Audit Buddy", page_icon="📑", layout="wide")

# --- SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- HEADER ---
st.markdown("""
<div class="header" style="background:#001965;color:white;padding:15px;border-radius:8px;margin-bottom:10px;">
  <h2>📑 Audit Buddy</h2>
  <p>Ask questions and get AI-powered answers from your audit knowledge base.</p>
</div>
""", unsafe_allow_html=True)

# --- BUILD CHAT HTML FOR COMPONENT ---
messages_html = ""
for msg in st.session_state.messages:
    safe_text = html_module.escape(msg["text"])
    if msg["role"] == "user":
        messages_html += f'<div class="user-msg">💬 {safe_text}</div>'
    else:
        messages_html += f'<div class="ai-msg">🤖 {safe_text}</div>'

html = f"""
<style>
/* chat styling inside the component iframe */
.chat-container {{
    height: 70vh;               /* adjust if you want a different visible chat height */
    overflow-y: auto;
    padding: 1rem;
    border: 1px solid #ddd;
    border-radius: 8px;
    background-color: #f9f9f9;
    box-sizing: border-box;
}}
.user-msg, .ai-msg {{
    display: inline-block;
    padding: 10px 15px;
    border-radius: 12px;
    margin: 6px 0;
    max-width: 80%;
    word-wrap: break-word;
}}
.user-msg {{ background-color: #E6F0FF; color: #001965; float: right; clear: both; }}
.ai-msg {{ background-color: #f0f4ff; color: #001965; float: left; clear: both; }}
</style>

<div class="chat-container" id="chat-box">
{messages_html}
</div>

<script>
(function(){
  const chatBox = document.getElementById('chat-box');
  if (!chatBox) return;
  const key = 'audit-buddy-autoscroll';

  // Read auto-scroll preference from localStorage (default: enabled)
  function readAuto() {
    const v = localStorage.getItem(key);
    if (v === null) return true;
    return v === 'true';
  }

  // When user scrolls, save whether they are near bottom (true) or not (false)
  chatBox.addEventListener('scroll', function(){
    const nearBottom = (chatBox.scrollTop + chatBox.clientHeight) >= (chatBox.scrollHeight - 20);
    localStorage.setItem(key, nearBottom ? 'true' : 'false');
  });

  // Scroll to bottom only if auto is enabled
  function scrollIfNeeded(){
    const auto = readAuto();
    if (auto) {
      chatBox.scrollTop = chatBox.scrollHeight;
    }
  }

  // Small delay to make sure content is rendered, then scroll if needed
  setTimeout(scrollIfNeeded, 50);

})();
</script>
"""

# Render the chat as an embedded component (iframe). The height should match the chat-container height.
components.html(html, height=650, scrolling=False)

# --- INPUT FORM (Streamlit) ---
st.markdown('<div style="padding:10px;border-top:1px solid #ddd;background:white;">', unsafe_allow_html=True)
with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([9, 1])
    with col1:
        query = st.text_input("Type your message", key="chat_input", placeholder="Type your message here...", label_visibility="collapsed")
    with col2:
        submitted = st.form_submit_button("🔍")

    if submitted and query.strip():
        # Add user question
        st.session_state.messages.append({"role": "user", "text": query})

        # Call your webhook and append AI reply
        with st.spinner("🤖 Thinking..."):
            try:
                response = requests.post("https://aruna78.app.n8n.cloud/webhook/audit-buddy", json={"query": query}, timeout=30)
                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("answer", "No answer received.")
                    st.session_state.messages.append({"role": "AI", "text": answer})
                    st.experimental_rerun()
                else:
                    st.error(f"❌ Error: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"⚠️ Connection error: {e}")
st.markdown('</div>', unsafe_allow_html=True)
