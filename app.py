import streamlit as st
import google.generativeai as genai
from PIL import Image
from fpdf import FPDF
import io

# --- 1. INITIALISIERUNG ---
st.set_page_config(page_title="Málaga Invest: Final", layout="wide")

if "GEMINI_API_KEY" not in st.secrets:
    st.error("🔑 API Key fehlt in den Secrets!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# --- MODELL-FIX GEGEN 404 ---
# Wir nutzen die ID, die laut Google-Dokumentation IMMER funktionieren muss
MODEL_ID = 'gemini-1.5-flash'
model = genai.GenerativeModel(MODEL_ID)

# --- PDF FUNKTION ---
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    # Entfernt Zeichen, die das PDF zum Absturz bringen könnten
    clean_text = text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, txt=clean_text)
    return pdf.output()

# --- 3. BENUTZEROBERFLÄCHE ---
st.title("🛡️ Invest-Scout: Finaler Check")

uploaded_files = st.file_uploader("Screenshots hochladen:", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    if st.button("🚀 TIEFENPRÜFUNG STARTEN", use_container_width=True):
        with st.spinner("🤖 Analysiere..."):
            try:
                # Bilder vorbereiten
                img_list = [Image.open(f) for f in uploaded_files]
                
                # Der Auftrag
                prompt = "Analysiere auf: AFO, Rústico, Preis, m2 und Zustand. Gib ein klares Fazit."
                
                # Anfrage absenden
                response = model.generate_content([prompt] + img_list)
                
                if response.text:
                    st.session_state['last_analysis'] = response.text
                    st.markdown("### 📋 Ergebnis")
                    st.markdown(response.text)
                else:
                    st.error("Antwort leer. Bitte erneut versuchen.")
            except Exception as e:
                # Zeigt uns den exakten Pfad-Fehler, falls er noch besteht
                st.error(f"Schnittstellen-Fehler: {e}")

# PDF Download
if 'last_analysis' in st.session_state:
    try:
        pdf_bytes = create_pdf(st.session_state['last_analysis'])
        st.download_button(
            label="📄 Analyse als PDF speichern",
            data=bytes(pdf_bytes),
            file_name="Invest_Analyse.pdf",
            mime="application/pdf"
        )
    except Exception as e:
        st.info("Bereite PDF vor...")
