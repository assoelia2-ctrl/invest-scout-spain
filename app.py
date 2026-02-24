import streamlit as st
import google.generativeai as genai
from PIL import Image
from fpdf import FPDF
import io
import tempfile
import os

# --- 1. KONFIGURATION ---
st.set_page_config(page_title="Andalusien Invest Scout", layout="wide")

api_key = st.secrets.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# --- 2. HILFSFUNKTIONEN ---

def get_best_model():
    try:
        available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        if "models/gemini-1.5-flash" in available:
            return "models/gemini-1.5-flash"
        return available[0] if available else None
    except:
        return None

def create_pdf(text, image):
    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Immobilien-Analyse: Andalusien", ln=True, align='C')
    pdf.ln(10)
    
    # BILD-FIX: Temporäre Datei nutzen, damit FPDF nicht abstürzt
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        image.save(tmp.name, format="PNG")
        pdf.image(tmp.name, x=10, y=30, w=90)
        tmp_path = tmp.name

    pdf.ln(85)
    
    # Analyse-Text
    pdf.set_font("Arial", size=11)
    clean_text = text.replace("**", "").replace("*", "-").replace("€", "Euro")
    pdf.multi_cell(0, 8, clean_text.encode('latin-1', 'ignore').decode('latin-1'))
    
    pdf_output = pdf.output(dest='S').encode('latin-1', 'ignore')
    
    # Aufräumen
    if os.path.exists(tmp_path):
        os.remove(tmp_path)
        
    return pdf_output

# --- 3. APP OBERFLÄCHE ---

st.title("☀️ Andalusien Real Estate Master")

selected_model = get_best_model()
uploaded_file = st.file_uploader("Screenshot hochladen", type=['png', 'jpg', 'jpeg'])

if uploaded_file and selected_model:
    img = Image.open(uploaded_file)
    st.image(img, width=500)
    
    if st.button("🔍 KI-Gutachten jetzt erstellen"):
        with st.spinner("Analysiere..."):
            try:
                model = genai.GenerativeModel(selected_model)
                prompt = "Du bist Baugutachter in Andalusien. Analysiere Substanz, Zufahrt und Solar-Potential. Gliedere in RISIKEN, CHANCEN und KOSTEN."
                response = model.generate_content([prompt, img])
                st.session_state['analysis_text'] = response.text
                st.session_state['current_img'] = img
            except Exception as e:
                st.error(f"Fehler: {e}")

if 'analysis_text' in st.session_state:
    st.divider()
    st.markdown(st.session_state['analysis_text'])
    
    # PDF Button
    try:
        pdf_data = create_pdf(st.session_state['analysis_text'], st.session_state['current_img'])
        st.download_button(
            label="📥 Als PDF herunterladen",
            data=pdf_data,
            file_name="Andalusien_Gutachten.pdf",
            mime="application/pdf"
        )
    except Exception as e:
        st.error(f"PDF-Fehler: {e}")
