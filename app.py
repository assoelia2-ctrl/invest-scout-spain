import streamlit as st
import google.generativeai as genai
from PIL import Image
from fpdf import FPDF

# --- SETUP ---
st.set_page_config(page_title="Málaga Invest: NOTFALL-SYSTEM")

if "GEMINI_API_KEY" not in st.secrets:
    st.error("🔑 API Key fehlt!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# NOTFALL-MODELL: Wir nutzen das stabilste verfügbare Modell
# 'gemini-pro-vision' ist der sicherste Anker gegen 404 Fehler
model = genai.GenerativeModel('gemini-pro-vision')

st.title("🛡️ Invest-Scout: Notfall-Anbindung")
st.warning("Wir nutzen jetzt das Hochstabilitäts-Modell, um den 404-Fehler zu umgehen.")

files = st.file_uploader("Bilder hochladen:", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

if files:
    if st.button("🚀 ANALYSE STARTEN"):
        with st.spinner("🤖 Kontaktiere Google Hochsicherheits-Server..."):
            try:
                # Bildvorbereitung
                imgs = [Image.open(f) for f in files]
                prompt = "Analysiere diese Immobilien-Screenshots auf AFO-Status, Preis pro m2 und Investment-Risiko in Malaga."
                
                # Der stabilste Aufruf-Weg
                response = model.generate_content([prompt] + imgs)
                
                if response.text:
                    st.session_state['notfall_result'] = response.text
                    st.markdown(response.text)
            except Exception as e:
                # Falls auch das nicht geht, liegt es am API-Key selbst
                st.error(f"⚠️ Letzter Schnittstellen-Fehler: {e}")
                st.info("Sollte dies scheitern, erstelle bitte einen neuen API-Key unter aistudio.google.com")

if 'notfall_result' in st.session_state:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    clean = st.session_state['notfall_result'].encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, txt=clean)
    st.download_button("📄 PDF Speichern", data=bytes(pdf.output()), file_name="Analyse.pdf")
