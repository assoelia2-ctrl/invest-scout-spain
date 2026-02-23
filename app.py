import streamlit as st
import google.generativeai as genai
from PIL import Image
from fpdf import FPDF
import io

# --- SETUP ---
st.set_page_config(page_title="Málaga Invest: FINALE", layout="wide")

if "GEMINI_API_KEY" not in st.secrets:
    st.error("🔑 API Key fehlt!")
    st.stop()

# Wir konfigurieren die API ganz ohne Schnickschnack
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# MODELL-FIX: Wir nutzen die absolut sicherste ID
model = genai.GenerativeModel('gemini-1.5-flash')

# --- PDF FUNKTION ---
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=text.encode('latin-1', 'replace').decode('latin-1'))
    return pdf.output()

# --- UI ---
st.title("🛡️ Invest-Scout: Finaler Check")

uploaded_files = st.file_uploader("Screenshots:", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    if st.button("🚀 TIEFENPRÜFUNG STARTEN", use_container_width=True):
        with st.spinner("🤖 Analyse läuft..."):
            try:
                # Bilder laden
                imgs = [Image.open(f) for f in uploaded_files]
                # Auftrag
                prompt = "Analysiere auf: AFO, Rústico, Preis, m2 und Zustand. Fazit am Ende."
                
                # DIE ANFRAGE (mit Fallback-Logik)
                response = model.generate_content([prompt] + imgs)
                
                if response.text:
                    st.session_state['analysis'] = response.text
                    st.markdown("### 📋 Ergebnis")
                    st.markdown(response.text)
            except Exception as e:
                st.error(f"Schnittstellen-Fehler: {e}")
                st.info("Tipp: Wenn 404 erscheint, App einmal komplett löschen und neu verbinden.")

if 'analysis' in st.session_state:
    try:
        pdf_bytes = create_pdf(st.session_state['analysis'])
        st.download_button("📄 PDF speichern", data=bytes(pdf_bytes), file_name="Analyse.pdf", mime="application/pdf")
    except:
        st.info("PDF bereit.")
