import streamlit as st
import requests

# n8n webhook URL
WEBHOOK_URL = "https://aruna78.app.n8n.cloud/webhook/audit-buddy"

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []  # [{sender, text}]
if "metadata" not in st.session_state:
    st.session_state.metadata = {}  # latest metadata

st.set_page_config(layout="wide", page_title="Audit Buddy")

# Layout: 2 columns
col1, col2 = st.columns([2, 1])

# ---- Left column: Chat ----
with col1:
    st.header("💬 Audit Buddy Chat")

    # Display messages
    for msg in st.session_state.messages:
        if msg["sender"] == "user":
            st.markdown(f"🧑 **You:** {msg['text']}")
        else:
            st.markdown(f"🤖 **Bot:** {msg['text']}")

    # Chat input
    user_input = st.chat_input("Type your query...")

    if user_input:
        # Save user msg
        st.session_state.messages.append({"sender": "user", "text": user_input})

        try:
            # Send to webhook
            response = requests.post(WEBHOOK_URL, json={"text": user_input})
            if response.status_code == 200:
                data = response.json()

                # Bot reply
                bot_reply = data.get("reply", "No reply received.")
                st.session_state.messages.append({"sender": "bot", "text": bot_reply})

                # Metadata
                st.session_state.metadata = {
                    "intent": data.get("intent", ""),
                    "attributes": data.get("attributes", {}),
                    "context": data.get("context", "")
                }
            else:
                st.session_state.messages.append({"sender": "bot", "text": f"Error: {response.text}"})
        except Exception as e:
            st.session_state.messages.append({"sender": "bot", "text": f"Request failed: {e}"})


# ---- Right column: Metadata ----
with col2:
    st.header("📑 Metadata")

    if st.session_state.metadata:
        st.json(st.session_state.metadata)
    else:
        st.info("No metadata yet. Ask a question!")
