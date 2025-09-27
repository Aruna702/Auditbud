import streamlit as st
import requests

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Audit Buddy for Novo Nordisk Hackathon",
    page_icon="📑",
    layout="wide"
)

# --- CUSTOM CSS FOR BRANDING ---
st.markdown(
    f"""
    <style>
    /* Page background */
    .stApp {{
        background-color: #FFFFFF;
        color: #001965;
    }}
    
    /* Header */
    .header-title {{
        color: #FFFFFF;
        background-color: #001965;
        padding: 15px;
        border-radius: 8px;
    }}
    
    /* Buttons */
    div.stButton > button {{
        background-color: #005AD2;
        color: #FFFFFF;
        height: 40px;
        width: 200px;
        border-radius: 8px;
        border: none;
        font-size: 16px;
        font-weight: bold;
    }}
    
    /* Text area */
    textarea {{
        border-radius: 8px;
        border: 1px solid #005AD2;
        padding: 10px;
    }}
    
    /* Info box */
    .stAlert > div[data-baseweb="alert"] {{
        background-color: #E6F0FF; /* Light tint of Science Blue */
        color: #001965;
        border-radius: 8px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# --- HEADER WITH LOGO AND TITLE ---
col1, col2 = st.columns([1, 6])

with col1:
    st.image("image.png", width=80)

with col2:
    st.markdown(
        """
        <div class="header-title">
            <h1 style="margin:0;">📑 Audit Buddy</h1>
            <p style="margin:0; font-size: 16px;">Ask questions and get AI-powered answers from your audit knowledge base.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

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
                response = requests.post(
                    "https://aruna78.app.n8n.cloud/webhook-test/audit-buddy",
                    json={"query": query},
                    timeout=30
                )

                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("answer", "No answer received.")
                    
                    st.markdown("### ✅ Answer:")
                    st.info(answer)
                else:
                    st.error(f"❌ Error: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"⚠️ Connection error: {e}")
