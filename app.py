import streamlit as st
import google.generativeai as genai
from PIL import Image
from fpdf import FPDF
import io

# --- 1. INITIALISIERUNG ---
st.set_page_config(page_title="Málaga Invest: Fixed", layout="wide")

if "GEMINI_API_KEY" not in st.secrets:
    st.error("🔑 Key fehlt in Secrets!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# --- DER ULTIMATIVE 404-FIX ---
# Wir nutzen hier den nackten Namen, den die neueste Library erzwingt
model = genai.GenerativeModel('gemini-1.5-flash')

def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    clean_text = text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, txt=clean_text)
    return pdf.output()

# --- 2. UI ---
st.title("🛡️ Invest-Scout: Finaler Fix")

uploaded_files = st.file_uploader("Screenshots:", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    if st.button("🚀 TIEFENPRÜFUNG STARTEN"):
        with st.spinner("KI wird gerufen..."):
            try:
                # Bild-Konvertierung für die neue API-Version
                img_list = [Image.open(f) for f in uploaded_files]
                
                # Direkter Aufruf ohne v1beta-Umweg
                response = model.generate_content(
                    ["Analysiere auf AFO, Rústico, Preis und Zustand."] + img_list
                )
                
                if response.text:
                    st.session_state['result'] = response.text
                    st.markdown(response.text)
            except Exception as e:
                # Dieser Block fängt den 404 ab und erklärt, was zu tun ist
                st.error(f"Schnittstellen-Fehler: {e}")
                st.info("Falls hier wieder 404 steht: Klicke in Streamlit rechts unten auf 'Manage App' -> 'Reboot App'.")

if 'result' in st.session_state:
    try:
        pdf_data = create_pdf(st.session_state['result'])
        st.download_button("📄 PDF Speichern", data=bytes(pdf_data), file_name="Analyse.pdf")
    except:
        pass
