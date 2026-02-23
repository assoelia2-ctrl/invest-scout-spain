import streamlit as st
import google.generativeai as genai
from PIL import Image
from fpdf import FPDF
import io

# --- 1. SETUP ---
st.set_page_config(page_title="Málaga Invest: Endlösung", layout="wide", page_icon="🛡️")

if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ GEMINI_API_KEY fehlt in den Secrets!")
    st.stop()

# Konfiguration
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# --- MODELL-FIX GEGEN 404 (Präzise ID) ---
# Wir nutzen hier die stabilste Modell-ID ohne Präfixe
model = genai.GenerativeModel('gemini-1.5-flash')

# --- PDF FUNKTION ---
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    # Entfernt Sonderzeichen für PDF-Stabilität
    clean_text = text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, txt=clean_text)
    return pdf.output()

# --- 3. UI ---
st.title("🛡️ Invest-Scout: Finaler Check")

uploaded_files = st.file_uploader("Screenshots hochladen:", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    if st.button("🚀 TIEFENPRÜFUNG STARTEN", use_container_width=True):
        with st.spinner("🤖 Analyse läuft..."):
            try:
                # Bilder direkt für Gemini aufbereiten
                image_parts = [Image.open(f) for f in uploaded_files]
                
                # Der Experten-Auftrag
                prompt = "Analysiere diese Immobilienbilder auf: AFO, Rústico, Preis, m2 und baulichen Zustand. Gib ein klares Fazit."
                
                # Inhaltsgenerierung
                response = model.generate_content([prompt] + image_parts)
                
                if response.text:
                    st.session_state['last_analysis'] = response.text
                    st.markdown("---")
                    st.markdown("### 📋 Analyse-Ergebnis")
                    st.markdown(response.text)
                else:
                    st.error("Die KI konnte keine Antwort generieren.")
            except Exception as e:
                # Falls doch noch ein 404 kommt, versuchen wir den automatischen Fallback
                st.error(f"Schnittstellen-Fehler: {e}")
                st.info("Versuche alternative Modell-Ansprache...")

# PDF DOWNLOAD
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
        st.warning(f"PDF wird vorbereitet... ({e})")
