import streamlit as st
import google.generativeai as genai
from PIL import Image
from fpdf import FPDF
import io

# --- 1. KONFIGURATION ---
st.set_page_config(page_title="Andalusien Invest Scout", layout="wide")

# API-Key aus den Secrets laden
api_key = st.secrets.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("API-Key fehlt in den Secrets!")

# --- 2. HILFSFUNKTIONEN ---

def get_best_model():
    """Findet das beste verfügbare KI-Modell auf dem Server"""
    try:
        available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        if "models/gemini-1.5-flash" in available:
            return "models/gemini-1.5-flash"
        return available[0] if available else None
    except:
        return None

def create_pdf(text, image):
    """Erstellt ein sauberes PDF-Gutachten"""
    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Immobilien-Analyse: Andalusien", ln=True, align='C')
    pdf.ln(10)
    
    # Bild einfügen
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    pdf.image(img_byte_arr, x=10, y=30, w=90)
    pdf.ln(80)
    
    # Analyse-Text (Sonderzeichen-Safe)
    pdf.set_font("Arial", size=11)
    clean_text = text.replace("**", "").replace("*", "-").replace("€", "Euro")
    # Umwandlung für PDF-Kompatibilität
    pdf.multi_cell(0, 8, clean_text.encode('latin-1', 'ignore').decode('latin-1'))
    
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- 3. APP OBERFLÄCHE ---

st.title("☀️ Andalusien Real Estate Master")
st.write("Lade einen Screenshot hoch, um ein KI-gestütztes Gutachten zu erstellen.")

# Modell-Check in der Sidebar
selected_model = get_best_model()
with st.sidebar:
    if selected_model:
        st.success(f"KI bereit: {selected_model.split('/')[-1]}")
    else:
        st.error("KI-Modell nicht erreichbar.")

uploaded_file = st.file_uploader("Screenshot (Idealista, Fotocasa etc.)", type=['png', 'jpg', 'jpeg'])

if uploaded_file and selected_model:
    img = Image.open(uploaded_file)
    st.image(img, width=500, caption="Vorschau des Objekts")
    
    if st.button("🔍 KI-Gutachten jetzt erstellen"):
        with st.spinner("Analysiere Bausubstanz und Lage..."):
            try:
                model = genai.GenerativeModel(selected_model)
                prompt = """
                Du bist ein zertifizierter Baugutachter in Andalusien. 
                Analysiere diesen Screenshot detailliert:
                1. BAUSUBSTANZ: Risse, Salpeter (Humedad), Zustand der Fassade.
                2. ZUFAHRT: Ist es ein Carril (Schotterweg) oder asphaltiert?
                3. SOLAR: Potenzial für Photovoltaik und Schattenwurf.
                Antworte strukturiert in: 🚩 RISIKEN, ✨ CHANCEN und 💶 KOSTENSCHÄTZUNG.
                """
                response = model.generate_content([prompt, img])
                
                # In Session speichern, damit es beim PDF-Klick nicht verschwindet
                st.session_state['analysis_text'] = response.text
                st.session_state['current_img'] = img
            except Exception as e:
                st.error(f"Fehler bei der Analyse: {e}")

# Ergebnis-Anzeige & PDF Download
if 'analysis_text' in st.session_state:
    st.divider()
    st.markdown("### Dein Gutachten")
    st.write(st.session_state['analysis_text'])
    
    # PDF Button
    try:
        pdf_data = create_pdf(st.session_state['analysis_text'], st.session_state['current_img'])
        st.download_button(
            label="📥 Als PDF herunterladen",
            data=pdf_data,
            file_name="Andalusien_Gutachten.pdf",
            mime="application/pdf"
        )
    except Exception as e:
        st.warning(f"PDF-Vorschau bereit, Button wird generiert... ({e})")
