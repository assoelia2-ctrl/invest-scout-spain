import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. KONFIGURATION & KEY-ABFRAGE ---
# Holt den Key automatisch aus dem Feld "Secrets", das du in den Settings ausgefüllt hast
api_key = st.secrets.get("GEMINI_API_KEY")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # Hier ist die wichtige Änderung: 1.5-flash statt pro-vision
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"Fehler bei der KI-Konfiguration: {e}")
else:
    st.warning("⚠️ Bitte hinterlege den GEMINI_API_KEY in den Streamlit Cloud Secrets.")

# --- 2. EXPERTEN-ANALYSE FUNKTION ---
def analyze_image(img):
    """Der Anforderungstext für die KI"""
    prompt = """
    Du bist ein erfahrener Immobilien-Gutachter in Andalusien. 
    Analysiere diesen Screenshot detailliert auf:
    1. BAUSUBSTANZ: Risse, Feuchtigkeit (Salpeter), Zustand Dach/Fenster.
    2. UMGEBUNG: Zufahrt (Asphalt oder Schotter/Carril), Bepflanzung (geschützte Bäume?).
    3. POTENZIAL: Schattenwurf durch Berge/Nachbarn, Eignung für Solar.
    
    Antworte in diesen Kategorien:
    🚩 RISIKEN: Was könnte teuer oder rechtlich schwierig werden?
    ✨ CHANCEN: Wo liegt der versteckte Wert?
    💶 KOSTEN-SCHÄTZUNG: Grobe Richtung für erste Maßnahmen.
    """
    # Bild an das Modell senden
    response = model.generate_content([prompt, img])
    return response.text

# --- 3. APP OBERFLÄCHE ---
st.set_page_config(page_title="Andalusien Invest Scout", layout="wide")
st.title("☀️ Andalusien Real Estate Master")
st.write("KI-Analyse für Screenshots von Idealista, Fotocasa & Co.")

# Upload Bereich
uploaded_files = st.file_uploader("Screenshots hier hochladen", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])

if uploaded_files:
    for i, file in enumerate(uploaded_files):
        st.divider()
        col1, col2 = st.columns([1, 1.5])
        
        img = Image.open(file)
        
        with col1:
            st.image(img, caption=f"Hochgeladenes Bild {i+1}", use_container_width=True)
            
        with col2:
            if st.button(f"🔍 KI-Gutachten für Bild {i+1} starten", key=f"btn_{i}"):
                if api_key:
                    with st.spinner("KI analys
