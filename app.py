import streamlit as st
import google.generativeai as genai
from PIL import Image
from fpdf import FPDF
import io

# --- 1. SETUP & KONFIGURATION ---
st.set_page_config(page_title="Málaga Invest: EXPERT", layout="wide", page_icon="🛡️")

# Styles für ein professionelles Aussehen
st.markdown("""<style>.stButton>button {width: 100%; border-radius: 5px; height: 3em; background-color: #ff4b4b; color: white; font-weight: bold;}</style>""", unsafe_allow_html=True)

if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ API Key fehlt in den Secrets! Bitte GEMINI_API_KEY hinzufügen.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. EXPERTEN-FUNKTIONEN ---
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Immobilien-Analyse: Málaga Invest", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    # Bereinigung für PDF-Kompatibilität (Umlaute)
    clean_text = text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, txt=clean_text)
    return pdf.output()

# --- 3. BENUTZEROBERFLÄCHE (UI) ---
st.title("🛡️ Invest-Scout: Profi-Check")
st.info("Lade Screenshots von Immobilienangeboten hoch (Ideal: AFO-Status, Grundbuchauszug, Fotos).")

uploaded_files = st.file_uploader("Screenshots auswählen:", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    st.success(f"✅ {len(uploaded_files)} Bilder bereit für Analyse.")
    
    if st.button("🚀 TIEFENPRÜFUNG STARTEN"):
        with st.spinner("🤖 KI analysiert Dokumente und Bilder..."):
            try:
                # Bildverarbeitung
                image_parts = [Image.open(f) for f in uploaded_files]
                
                # Der Master-Prompt (Alles drin, was du brauchst)
                prompt = """
                Du bist ein Experte für Immobilieninvestments in Andalusien. 
                Analysiere die hochgeladenen Bilder extrem genau auf:
                1. AFO / Urbanistico Status (Legalität)
                2. Grundstückstyp (Rústico oder Urbano)
                3. Preis-Leistungsverhältnis basierend auf m2 und Zustand
                4. Baulicher Zustand und Renovierungsbedarf
                5. FAZIT: Investment-Risiko (Skala 1-10) und klare Kaufempfehlung.
                Antworte strukturiert in Deutsch.
                """
                
                response = model.generate_content([prompt] + image_parts)
                
                if response.text:
                    st.session_state['full_report'] = response.text
                    st.markdown("---")
                    st.markdown("### 📋 Analyse-Ergebnis")
                    st.markdown(response.text)
                else:
                    st.warning("Die KI konnte keine Daten extrahieren. Bitte bessere Screenshots nutzen.")
            except Exception as e:
                st.error(f"Schnittstellen-Fehler: {e}")
                st.info("Hinweis: Falls 404 erscheint, App in Streamlit löschen und neu verbinden.")

# --- 4. EXPORT-BEREICH ---
if 'full_report' in st.session_state:
    st.markdown("---")
    try:
        pdf_bytes = create_pdf(st.session_state['full_report'])
        st.download_button(
            label="📄 Als PDF-Bericht speichern",
            data=bytes(pdf_bytes),
            file_name="Invest_Analyse_Malaga.pdf",
            mime="application/pdf"
        )
    except Exception as e:
        st.info("Erstelle Download-Link...")

