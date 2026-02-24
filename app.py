import streamlit as st
import google.generativeai as genai
from PIL import Image
from fpdf import FPDF
import io

# 1. API Setup
api_key = st.secrets.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

st.set_page_config(page_title="Andalusien Invest Scout", layout="wide")
st.title("☀️ Andalusien Real Estate Master")

# 2. System-Check (Sidebar)
with st.sidebar:
    st.header("System-Check")
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        selected_model = "models/gemini-1.5-flash" if "models/gemini-1.5-flash" in available_models else available_models[0]
        st.success(f"Modell aktiv: {selected_model}")
    except Exception as e:
        st.error(f"Verbindungsproblem: {e}")
        selected_model = None

# 3. PDF Generator Funktion
def create_pdf(text, image):
    pdf = FPDF()
    pdf.add_page()
    
    # Titel
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Objekt-Gutachten: Andalusien Invest", ln=True, align='C')
    pdf.ln(10)
    
    # Bild einfügen (Temporär speichern für PDF)
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    pdf.image(img_byte_arr, x=10, y=30, w=100)
    pdf.ln(70) # Platzhalter für das Bild
    
    # Analyse-Text
    pdf.set_font("Arial", size=11)
    # Entferne Markdown-Sterne für sauberen PDF-Text
    clean_text = text.replace("**", "").replace("*", "-")
    pdf.multi_cell(0, 8, clean_text)
    
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# 4. Haupt-Logik
uploaded_file = st.file_uploader("Screenshot hochladen", type=['png', 'jpg', 'jpeg'])

if uploaded_file and selected_model:
    img = Image.open(uploaded_file)
    st.image(img, width=500, caption="Hochgeladenes Objekt")
    
    if st.button("🔍 Analyse starten"):
        with st.spinner("KI-Gutachter erstellt Analyse..."):
            try:
                model = genai.GenerativeModel(selected_model)
                prompt = "Du bist Baugutachter in Andalusien. Analysiere Substanz, Zufahrt und Solar-Potential. Gliedere in RISIKEN, CHANCEN, KOSTEN."
                response = model.generate_content([prompt, img])
                
                # Ergebnis speichern
                st.session_state['last_analysis'] = response.text
                st.session_state['last_img'] = img
                
            except Exception as e:
                st.error(f"Fehler: {e}")

    # Wenn Analyse vorhanden, zeige Ergebnis und PDF-Button
    if 'last_analysis' in st.session_state:
        st.markdown("### Analyse-Ergebnis")
        st.write(st.session_state['last_analysis'])
        
        # PDF Button
        pdf_data = create_pdf(st.session_state['last_analysis'], st.session_state['last_img'])
        st.download_button(
            label="📥 Gutachten als PDF herunterladen",
            data=pdf_data,
            file_name="Andalusien_Gutachten.pdf",
            mime="application/pdf"
        )
