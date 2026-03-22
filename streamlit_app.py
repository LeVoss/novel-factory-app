import streamlit as st
import google.generativeai as genai
from docx import Document
import io

# 1. Page Configuration
st.set_page_config(
    page_title="Manuscript-Check | Pro Logic Detective", 
    page_icon="🕵️‍♂️", 
    layout="wide"
)

# Custom Styling
st.markdown("""
    <style>
    .main {
        background-color: #ffffff;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3.5em;
        background-color: #2e7d32;
        color: white;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1b5e20;
        border: none;
    }
    .privacy-box {
        background-color: #f1f8e9;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #2e7d32;
        margin-bottom: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. API Connection
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        model = genai.GenerativeModel(available_models[0])
    except Exception as e:
        st.error(f"Connection Error: {e}")
        st.stop()
else:
    st.error("API Key missing! Please check your secrets.toml.")
    st.stop()

def read_docx(file):
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

# --- HEADER & LANDING PAGE ---
st.title("🕵️‍♂️ Manuscript-Check")
st.subheader("Your Silent Partner in Storytelling Excellence.")

# Value Propositions
cols_features = st.columns(3)
with cols_features[0]:
    st.markdown("### 📝 Smart Detection")
    st.caption("Spot continuity errors, teleporting characters, and impossible physics instantly.")
with cols_features[1]:
    st.markdown("### ⏱️ Timeline Guard")
    st.caption("Keep your story’s internal clock ticking perfectly across every chapter.")
with cols_features[2]:
    st.markdown("### 💡 Creative Solutions")
    st.caption("Get professional editorial suggestions to bridge narrative gaps seamlessly.")

# Privacy Promise
st.markdown("""
    <div class="privacy-box">
        <strong>🔒 Your Privacy Matters:</strong><br>
        We do not store your manuscript. Your text is processed securely and deleted immediately after analysis. 
        Your creative IP remains 100% yours.
    </div>
    """, unsafe_allow_html=True)

st.markdown("### How it Works")
st.write("1. **Upload** your .docx or paste your text. 2. **Analyze** the internal logic. 3. **Refine** your draft.")
st.markdown("---")

# --- MAIN INTERFACE ---
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.header("1. Input Your Chapter")
    
    uploaded_file = st.file_uploader("Upload Word Document (.docx)", type=["docx"])
    
    if uploaded_file is not None:
        file_text = read_docx(uploaded_file)
        user_input = st.text_area("Review/Edit your text:", value=file_text, height=450)
    else:
        user_input = st.text_area("Paste your scene here:", height=450, placeholder="Once upon a time...")
    
    analyze_button = st.button("🔍 Run Deep Logic Analysis")

with col2:
    st.header("2. Analysis Report")
    if analyze_button and user_input:
        with st.spinner('The Detective is scrutinizing your manuscript...'):
            try:
                system_instruction = """
                You are a world-class developmental editor and logic expert for fiction. 
                Analyze the provided text strictly for contradictions and plot holes. 
                Structure your response using these EXACT categories:
                
                1. 🌍 PHYSICALITY & ENVIRONMENT (e.g., lighting, distances, gravity)
                2. ⏱️ TIMELINE & CONTINUITY (e.g., impossible sequences, time skips)
                3. 👤 CHARACTER LOGIC (e.g., internal contradictions, forbidden knowledge)
                4. 💡 PRO-TIP FOR FIXING (How to resolve the issues creatively)
                
                If a category is clear, state 'No issues detected.' Use a professional, encouraging tone.
                """
                
                response = model.generate_content(f"{system_instruction}\n\nManuscript Content: {user_input}")
                
                st.markdown(response.text)
                
                st.download_button(
                    label="📥 Download Analysis Report (.txt)",
                    data=response.text,
                    file_name="manuscript_logic_report.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"Analysis failed: {e}")
    else:
        st.info("Awaiting input... Upload or paste your text on the left to start.")

# Footer
st.markdown("---")
st.caption("© 2026 Manuscript-Check | Built by Authors, for Authors.")