# streamlit_auditbud_app.py
# Audit Bud - Streamlit prototype
# Requirements: streamlit, requests

import streamlit as st
import requests
import json
from datetime import datetime

st.set_page_config(page_title="Audit Bud", layout="wide")

# ------------------------- Helpers -------------------------
if 'messages' not in st.session_state:
    st.session_state.messages = []  # list of dicts: {role: 'user'|'ai', 'text': ...}

if 'metadata' not in st.session_state:
    # sample metadata structure provided by user
    st.session_state.metadata = {
        "Document ID": "IQ-LIMS-001",
        "Version": "1.0",
        "Status": "Draft",
        "Effective Date": "2025-09-06",
        "Author": "Validation Department",
        "Approvers": ["System Owner (placeholder)", "Quality (placeholder)", "IT (placeholder)"]
    }


# Utility to post to n8n (if webhook provided)
def post_to_webhook(url, payload=None, files=None, timeout=30):
    if not url:
        return {"error": "no webhook url provided"}
    try:
        if files:
            r = requests.post(url, data=payload or {}, files=files, timeout=timeout)
        else:
            r = requests.post(url, json=payload or {}, timeout=timeout)
        r.raise_for_status()
        try:
            return r.json()
        except Exception:
            return {"text": r.text}
    except Exception as e:
        return {"error": str(e)}


# ------------------------- Top header -------------------------
col1, col2, col3 = st.columns([1,6,1])
with col1:
    st.image("https://via.placeholder.com/40x40.png?text=AB", width=40)
with col2:
    st.markdown("# Audit Bud <span style='font-size:14px;color:#6b7280'>Your Automated Audit Readiness Assistant</span>", unsafe_allow_html=True)
with col3:
    dark = st.checkbox("Dark mode", key="darkmode")

# Apply simple dark mode styles
if dark:
    st.markdown(
        """
        <style>
        .stApp { background-color: #0b1220; color: #e6eef8 }
        .st-bk { background-color: #071029 }
        </style>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# ------------------------- Webhook inputs -------------------------
with st.expander("n8n webhook settings (optional)"):
    chat_webhook = st.text_input("Chat webhook URL (n8n)", value=st.session_state.get('chat_webhook',''))
    metadata_webhook = st.text_input("Metadata webhook URL (n8n)", value=st.session_state.get('metadata_webhook',''))
    st.session_state.chat_webhook = chat_webhook
    st.session_state.metadata_webhook = metadata_webhook

# ------------------------- Main layout -------------------------
left_col, right_col = st.columns([2,1], gap="large")

# LEFT: Chat interface
with left_col:
    st.subheader("Chat with Audit Bud")

    # Suggested prompt chips
    suggested = [
        "Summarize this document",
        "List audit findings",
        "Extract metadata",
        "Next review date",
    ]
    cols = st.columns(len(suggested))
    for i, s in enumerate(suggested):
        if cols[i].button(s):
            # add to input
            st.session_state.input_text = s

    # chat message area
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            if msg['role'] == 'user':
                st.markdown(f"<div style='background:#e6f0ff;padding:10px;border-radius:12px;margin:6px 0'>{msg['text']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='background:#f4f7fb;padding:10px;border-radius:12px;margin:6px 0'><strong>Audit Bud</strong>: {msg['text']}</div>", unsafe_allow_html=True)

    # message input
    if 'input_text' not in st.session_state:
        st.session_state.input_text = ''

    cols = st.columns([8,1])
    with cols[0]:
        user_input = st.text_input("", value=st.session_state.input_text, key='chat_input', placeholder='Ask Audit Bud a question...')
    with cols[1]:
        if st.button("Send"):
            if user_input.strip():
                st.session_state.messages.append({'role':'user','text':user_input})
                st.session_state.input_text = ''
                # send to chat webhook if provided
                payload = {
                    'message': user_input,
                    'timestamp': datetime.utcnow().isoformat()
                }
                result = post_to_webhook(st.session_state.get('chat_webhook',''), payload=payload)
                # result handling
                if 'error' in result:
                    ai_text = f"(webhook error) {result['error']}"
                else:
                    # try to extract text field; fallback to whole json
                    ai_text = result.get('text') or result.get('reply') or json.dumps(result)
                st.session_state.messages.append({'role':'ai','text':ai_text})
                st.experimental_rerun()

# RIGHT: Metadata dashboard + upload + screenshot component
with right_col:
    st.subheader("Document Metadata")
    st.write("Upload PDF or Word (.pdf, .docx)")
    uploaded_file = st.file_uploader("Upload document", type=['pdf','docx'])
    if uploaded_file is not None:
        # show filename
        st.write(f"Uploaded: {uploaded_file.name}")
        # send to metadata webhook (as file) if provided
        if st.session_state.get('metadata_webhook'):
            files = {'file': (uploaded_file.name, uploaded_file.getvalue())}
            resp = post_to_webhook(st.session_state['metadata_webhook'], payload={'filename': uploaded_file.name}, files=files)
            if 'error' in resp:
                st.error(f"Metadata webhook error: {resp['error']}")
            else:
                # if webhook returns metadata json, replace
                try:
                    if isinstance(resp, dict):
                        # merge keys
                        st.session_state.metadata.update(resp)
                except Exception:
                    pass

    # Display metadata cards
    for k, v in st.session_state.metadata.items():
        if isinstance(v, list):
            v = ", ".join(v)
        st.markdown(f"**{k}**  
        {v}")

    # Screenshot component: we will render the metadata panel inside an HTML component
    st.markdown("---")
    st.markdown("**Screenshot Metadata Panel**")

    # Prepare metadata JSON to pass into component
    metadata_json = json.dumps(st.session_state.metadata)
    screenshot_component = f"""
    <div id='metadata-card' style='font-family:Inter, system-ui, sans-serif; width:100%; padding:12px; background:linear-gradient(180deg, #ffffff, #f8fbff); border-radius:12px; box-shadow:0 6px 18px rgba(3, 37, 96, 0.08);'>
    <h3 style='margin-top:0; color:#003a8c;'>Metadata Preview</h3>
    <pre id='metadata-json' style='white-space:pre-wrap; font-family:Inter, Arial, sans-serif; font-size:13px; color:#0b2447;'>
    {metadata_json}
    </pre>
    <div style='display:flex; gap:8px; margin-top:12px;'>
      <button id='captureBtn' style='padding:8px 12px; border-radius:8px; border:none; background:#005AD2; color:white; cursor:pointer;'>Take Screenshot</button>
    </div>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <script>
    const btn = document.getElementById('captureBtn');
    btn.addEventListener('click', ()=>{
        const el = document.getElementById('metadata-card');
        html2canvas(el, {
            useCORS: true,
            allowTaint: true,
            logging: false,
            scale: 2,
            windowWidth: document.documentElement.scrollWidth,
            windowHeight: document.documentElement.scrollHeight
        }).then(canvas=>{
            const link = document.createElement('a');
            link.download = 'auditbud-metadata-' + Date.now() + '.png';
            link.href = canvas.toDataURL('image/png');
            link.click();
        }).catch(err=>{
            console.error(err);
            alert('Screenshot failed: ' + err);
        });
    });
    </script>
    """

    st.components.v1.html(screenshot_component, height=300)

    st.markdown("---")
    st.caption("Note: The screenshot captures the metadata preview area. For a full-page capture, additional permissions/CORS-friendly resources may be required for embedded images.")

# ------------------------- Footer / notes -------------------------
st.markdown("---")
st.markdown("**Developer notes:** Connect your n8n webhook URLs in the settings expander. The chat sends `{message}` JSON to the chat webhook and expects a JSON response with a `text` or `reply` field. The metadata webhook receives a file upload (form-data) and can return a JSON object to update the metadata display.")

st.markdown("**Run locally:** `streamlit run streamlit_auditbud_app.py`\nRequirements: `pip install streamlit requests`")
