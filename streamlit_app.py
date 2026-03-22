import streamlit as st
import google.generativeai as genai
from docx import Document
import io

# Page Configuration
st.set_page_config(page_title="Manuscript-Check | Pro Logic Detective", page_icon="🕵️‍♂️", layout="wide")

# Custom CSS for a professional "Landing Page" feel
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
    .report-text {
        font-family: 'Inter', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# Connection to Gemini API
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

# --- LANDING PAGE CONTENT ---
st.title("🕵️‍♂️ Manuscript-Check")
st.subheader("Catch Plot Holes Before Your Readers Do.")
st.markdown("""
**Stop worrying about continuity errors.** Manuscript-Check analyzes your chapters for physical impossibilities, 
timeline slips, and character inconsistencies in seconds.
""")
st.markdown("---")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.header("1. Input Your Chapter")
    
    # File Upload
    uploaded_file = st.file_uploader("Upload Word Document (.docx)", type=["docx"])
    
    if uploaded_file is not None:
        file_text = read_docx(uploaded_file)
        user_input = st.text_area("Review/Edit your text:", value=file_text, height=400)
    else:
        user_input = st.text_area("Paste your scene here:", height=400, placeholder="Once upon a time...")
    
    analyze_button = st.button("🔍 Run Deep Logic Analysis")

with col2:
    st.header("2. Analysis Report")
    if analyze_button and user_input:
        with st.spinner('The Detective is scrutinizing your manuscript...'):
            try:
                # The NEW English System Prompt
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
                
                st.markdown(f'<div class="report-text">{response.text}</div>', unsafe_allow_html=True)
                
                # Download Button
                st.download_button(
                    label="📥 Download Analysis Report (.txt)",
                    data=response.text,
                    file_name="manuscript_logic_report.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"Analysis failed: {e}")
    else:
        st.info("Awaiting input... Upload or paste your text on the left to start the analysis.")

# Footer
st.markdown("---")
st.caption("Built by Authors, for Authors. | Confidential & Private Analysis")