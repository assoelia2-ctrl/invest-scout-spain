import streamlit as st
import google.generativeai as genai
from PIL import Image
from fpdf import FPDF
import io

# --- SETUP ---
st.set_page_config(page_title="Málaga Invest: Final Fix", layout="wide")

if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ GEMINI_API_KEY fehlt in den Secrets!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# --- MODELL-FIX (Gegen Fehler 404) ---
# Wir nutzen die explizite Pfadangabe, die die API verlangt
model = genai.GenerativeModel('models/gemini-1.5-flash')

# --- PDF GENERATOR ---
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    # Entfernt Sonderzeichen für PDF-Stabilität
    clean_text = text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, txt=clean_text)
    return pdf.output()

# --- UI ---
st.title("🛡️ Invest-Scout: Immobilien-Check")

uploaded_files = st.file_uploader("Screenshots hochladen:", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    if st.button("🚀 TIEFENPRÜFUNG STARTEN"):
        with st.spinner("Analyse läuft..."):
            try:
                image_parts = [Image.open(f) for f in uploaded_files]
                prompt = "Analysiere auf AFO, Rústico, Preis, m2 und Zustand. Gib ein klares Fazit."
                
                # Inhaltsgenerierung
                response = model.generate_content([prompt] + image_parts)
                
                if response.text:
                    st.session_state['last_analysis'] = response.text
                    st.markdown(response.text)
                else:
                    st.error("Keine Antwort erhalten.")
            except Exception as e:
                st.error(f"Fehler: {e}")

if 'last_analysis' in st.session_state:
    try:
        pdf_bytes = create_pdf(st.session_state['last_analysis'])
        st.download_button(
            label="📄 PDF speichern",
            data=bytes(pdf_bytes),
            file_name="Analyse_Malaga.pdf",
            mime="application/pdf"
        )
    except Exception as e:
        st.warning(f"PDF-Vorbereitung: {e}")
