import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Audit Buddy", layout="centered")

# Keep messages in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Input form
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message here...", "")
    submitted = st.form_submit_button("Send")

if submitted and user_input.strip():
    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    # Dummy AI reply (replace with your API call)
    st.session_state.messages.append({"role": "ai", "content": f"You asked \"{user_input}\""})

# Render chat messages into HTML
messages_html = ""
for msg in st.session_state.messages:
    if msg["role"] == "user":
        messages_html += f'<div class="user-msg">{msg["content"]}</div>'
    else:
        messages_html += f'<div class="ai-msg">{msg["content"]}</div>'

# Chat container with CSS + Auto-scroll JS
html = f"""
<style>
.chat-container {{
    height: 70vh;
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
(function(){{
  const chatBox = document.getElementById('chat-box');
  if (!chatBox) return;
  const key = 'audit-buddy-autoscroll';

  // Read preference (default = true)
  function readAuto() {{
    const v = localStorage.getItem(key);
    if (v === null) return true;
    return v === 'true';
  }}

  // Save preference when user scrolls
  chatBox.addEventListener('scroll', function(){{
    const nearBottom = (chatBox.scrollTop + chatBox.clientHeight) >= (chatBox.scrollHeight - 20);
    localStorage.setItem(key, nearBottom ? 'true' : 'false');
  }});

  // Scroll if auto is on
  function scrollIfNeeded(){{
    if (readAuto()) {{
      chatBox.scrollTop = chatBox.scrollHeight;
    }}
  }}

  // Delay to ensure rendering
  setTimeout(scrollIfNeeded, 50);

}})();
</script>
"""

components.html(html, height=650, scrolling=False)
