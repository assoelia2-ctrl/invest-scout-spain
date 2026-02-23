import streamlit as st
import google.generativeai as genai
from PIL import Image
from fpdf import FPDF
import io

# --- 1. SETUP ---
st.set_page_config(page_title="Málaga Invest: EXPERT", layout="wide")

if "GEMINI_API_KEY" not in st.secrets:
    st.error("🔑 API Key fehlt in Secrets!")
    st.stop()

# Konfiguration erzwingen
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# MODELL-FIX: Wir nutzen die absolut sicherste ID für Version 0.7.2
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. PDF FUNKTION ---
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Immobilien-Analyse: Malaga Invest", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    clean_text = text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, txt=clean_text)
    return pdf.output()

# --- 3. UI ---
st.title("🛡️ Invest-Scout: Profi-Check Malaga")

uploaded_files = st.file_uploader("Screenshots hochladen:", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    if st.button("🚀 TIEFENPRÜFUNG STARTEN", use_container_width=True):
        with st.spinner("🤖 Analysiere AFO, Boden & Preis..."):
            try:
                imgs = [Image.open(f) for f in uploaded_files]
                
                # Der vollständige Experten-Auftrag
                prompt = """
                Du bist Immobilien-Experte für Malaga. Analysiere die Bilder auf:
                1. RECHT: AFO-Status, Suelo Rústico/Urbano Risiken.
                2. OBJEKT: Zustand, Pool-Legalität, m2-Plausibilität.
                3. FINANZEN: Preis-Check vs. Marktpreis Malaga.
                4. FAZIT: Klare Kaufempfehlung oder Warnung.
                """
                
                response = model.generate_content([prompt] + imgs)
                
                if response.text:
                    st.session_state['report'] = response.text
                    st.markdown("### 📋 Analyse-Ergebnis")
                    st.markdown(response.text)
            except Exception as e:
                st.error(f"Schnittstellen-Fehler: {e}")
                st.info("Falls 404 bleibt: App in Streamlit LÖSCHEN und neu verbinden.")

# PDF Download
if 'report' in st.session_state:
    try:
        pdf_out = create_pdf(st.session_state['report'])
        st.download_button("📄 PDF speichern", data=bytes(pdf_out), file_name="Analyse_Malaga.pdf", mime="application/pdf")
    except:
        st.info("PDF wird vorbereitet...")
