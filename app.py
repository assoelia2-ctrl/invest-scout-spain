import streamlit as st
import google.generativeai as genai
from PIL import Image
from fpdf import FPDF
import io

# --- 1. SETUP ---
st.set_page_config(page_title="Málaga Invest: Final", layout="wide")

if "GEMINI_API_KEY" not in st.secrets:
    st.error("🔑 KEY fehlt in Secrets!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# --- MODELL-FIX GEGEN 404 ---
# Wir erzwingen die stabilste Version ohne Pfad-Präfix
model = genai.GenerativeModel('gemini-1.5-flash')

# --- PDF GENERATOR ---
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    clean_text = text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, txt=clean_text)
    return pdf.output()

# --- 3. UI ---
st.title("🛡️ Invest-Scout: Finaler Check")

uploaded_files = st.file_uploader("Screenshots:", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    if st.button("🚀 TIEFENPRÜFUNG STARTEN", use_container_width=True):
        with st.spinner("Analyse läuft..."):
            try:
                image_parts = [Image.open(f) for f in uploaded_files]
                # Der präzise Auftrag
                prompt = "Analysiere auf: AFO, Rústico, Preis, m2 und Zustand. Gib ein klares Fazit."
                
                # Wir nutzen hier die sicherste Methode der Inhaltsübergabe
                response = model.generate_content([prompt] + image_parts)
                
                if response.text:
                    st.session_state['last_analysis'] = response.text
                    st.markdown("### 📋 Ergebnis")
                    st.markdown(response.text)
            except Exception as e:
                # Falls 404 erneut auftritt, zeigt die App jetzt die genaue Ursache
                st.error(f"Technischer Fehler: {e}")

if 'last_analysis' in st.session_state:
    try:
        pdf_bytes = create_pdf(st.session_state['last_analysis'])
        st.download_button("📄 PDF speichern", data=bytes(pdf_bytes), file_name="Analyse.pdf", mime="application/pdf")
    except Exception as e:
        st.info("Bereite PDF vor...")
