import streamlit as st
import google.generativeai as genai
from PIL import Image
from fpdf import FPDF
import io

# --- 1. SETUP ---
st.set_page_config(page_title="Málaga Invest: PRO", layout="wide")

if "GEMINI_API_KEY" not in st.secrets:
    st.error("🔑 API Key fehlt! Bitte in den Streamlit Secrets hinterlegen.")
    st.stop()

# API Konfiguration
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# --- DER ULTIMATIVE 404-FIX ---
# Wir nutzen hier eine stabilere Methode, um das Modell zu laden
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# --- PDF FUNKTION ---
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    # Bereinigung für PDF-Stabilität
    clean_text = text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, txt=clean_text)
    return pdf.output()

# --- 3. UI ---
st.title("🛡️ Invest-Scout: Finaler Malaga-Check")

uploaded_files = st.file_uploader("Screenshots auswählen:", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    if st.button("🚀 TIEFENPRÜFUNG STARTEN"):
        with st.spinner("🤖 Analysiere AFO, Rústico und Marktpreise..."):
            try:
                # Bilder vorbereiten
                image_parts = [Image.open(f) for f in uploaded_files]
                
                # Der vollständige Analyse-Auftrag
                prompt = """
                Analysiere als Immobilien-Experte für Málaga:
                1. RECHT: Gibt es Hinweise auf AFO oder Suelo Rústico?
                2. OBJEKT: Zustand, m2-Plausibilität und Pool-Legalität.
                3. PREIS: Ist der Preis für die Region Málaga realistisch?
                4. FAZIT: Klare Kaufempfehlung oder Warnung.
                """
                
                # Anfrage absenden
                response = model.generate_content([prompt] + image_parts)
                
                if response.text:
                    st.session_state['last_analysis'] = response.text
                    st.markdown("### 📋 Ergebnis")
                    st.markdown(response.text)
            except Exception as e:
                # Zeigt den Fehler an, falls Google immer noch blockt
                st.error(f"Schnittstellen-Fehler: {e}")

# PDF Export
if 'last_analysis' in st.session_state:
    try:
        pdf_bytes = create_pdf(st.session_state['last_analysis'])
        st.download_button(
            label="📄 Analyse als PDF speichern",
            data=bytes(pdf_bytes),
            file_name="Invest_Analyse_Malaga.pdf",
            mime="application/pdf"
        )
    except Exception as e:
        st.info("PDF wird erstellt...")

