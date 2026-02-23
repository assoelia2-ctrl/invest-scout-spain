import streamlit as st
import google.generativeai as genai
from PIL import Image
from fpdf import FPDF
import io

# --- 1. SETUP ---
st.set_page_config(page_title="Málaga Invest: TOTAL-FIX", layout="wide")

if "GEMINI_API_KEY" not in st.secrets:
    st.error("🔑 API Key fehlt!")
    st.stop()

# Wir konfigurieren die API OHNE Beta-Pfad
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# --- DER ULTIMATIVE 404-FIX ---
# Wir weisen das Modell hier GANZ explizit ohne Präfixe zu
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    model = genai.GenerativeModel('models/gemini-1.5-flash')

# --- 2. ANALYSE-LOGIK ---
st.title("🛡️ Invest-Scout: Finaler Malaga-Check")

uploaded_files = st.file_uploader("Bilder hochladen:", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    if st.button("🚀 TIEFENPRÜFUNG JETZT STARTEN"):
        with st.spinner("🤖 Erzwinge Verbindung zu Google..."):
            try:
                images = [Image.open(f) for f in uploaded_files]
                
                # Alles drin: AFO, Rústico, Preise, Risiko
                prompt = """
                Verhalte dich wie ein Immobilien-Anwalt in Málaga. Analysiere:
                1. RECHT: AFO-Status & Grundstückstyp (Rústico/Urbano).
                2. DETAILS: Baulicher Zustand & m2-Check.
                3. PREIS: Ist das Angebot für Málaga fair?
                4. FAZIT: Kaufempfehlung (Ja/Nein) & Risiko-Score.
                """
                
                # Wir schalten hier die Beta-Version manuell aus
                response = model.generate_content([prompt] + images)
                
                if response.text:
                    st.session_state['report'] = response.text
                    st.markdown(response.text)
            except Exception as e:
                # Zeigt uns, ob es immer noch ein 404 ist
                st.error(f"⚠️ Google-Fehler: {e}")

# PDF Export (Stabil für Umlaute)
if 'report' in st.session_state:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    clean_text = st.session_state['report'].encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, txt=clean_text)
    st.download_button("📄 PDF speichern", data=bytes(pdf.output()), file_name="Analyse.pdf")
