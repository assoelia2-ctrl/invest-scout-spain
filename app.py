import streamlit as st
import google.generativeai as genai
from PIL import Image
from fpdf import FPDF
import io

# --- 1. SETUP & CONFIG ---
st.set_page_config(page_title="Málaga Invest: PDF Edition", layout="wide", page_icon="🛡️")

if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ GEMINI_API_KEY fehlt in den Secrets!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. PDF GENERATOR FUNKTION ---
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt="Immobilien-Analyse: Málaga Invest", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    # Text sauber formatieren (Umlaute/Sonderzeichen Handling)
    pdf.multi_cell(0, 10, txt=text.encode('latin-1', 'replace').decode('latin-1'))
    
    return pdf.output(dest='S').encode('latin-1')

# --- 3. UI ---
st.title("🛡️ Invest-Scout: Risiko-Check & PDF-Export")

with st.sidebar:
    st.header("📊 Kosten-Rechner")
    kaufpreis = st.number_input("Kaufpreis (€)", value=250000, step=5000)
    itp_steuer = kaufpreis * 0.07
    st.write(f"7% ITP Steuer: **{itp_steuer:,.0f} €**")
    st.success(f"Gesamt: **{kaufpreis + itp_steuer:,.0f} €**")

uploaded_files = st.file_uploader("Screenshots hochladen:", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    if st.button("🚀 TIEFENPRÜFUNG STARTEN", use_container_width=True):
        with st.spinner("Gemini erstellt Analyse..."):
            try:
                image_parts = [Image.open(f) for f in uploaded_files]
                prompt = """Analysiere diese Bilder auf: 
                1. RECHT: AFO, DAFO, Rústico, Ocupado. 
                2. ZUSTAND: Bausubstanz, Pool, Dach. 
                3. DATEN: Preis, m2, Ort.
                Erstelle ein klares Fazit."""
                
                response = model.generate_content([prompt] + image_parts)
                analysis_text = response.text
                
                st.session_state['last_analysis'] = analysis_text
                st.markdown(analysis_text)

            except Exception as e:
                st.error(f"Fehler: {e}")

# PDF Download-Button anzeigen, wenn eine Analyse vorliegt
if 'last_analysis' in st.session_state:
    st.divider()
    pdf_data = create_pdf(st.session_state['last_analysis'])
    st.download_button(
        label="📄 Analyse als PDF speichern",
        data=pdf_data,
        file_name="Immobilien_Analyse_Malaga.pdf",
        mime="application/pdf"
    )
