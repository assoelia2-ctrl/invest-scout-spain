import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. API-Setup
api_key = st.secrets.get("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("API-Key fehlt in den Secrets!")

# 2. Analyse-Logik mit expliziter Modell-Wahl
def analyze_image(img):
    # Wir nutzen hier die aktuellste stabile Bezeichnung
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = """
    Du bist Baugutachter in Andalusien. Analysiere diesen Screenshot auf: 
    1. Substanz (Risse, Feuchtigkeit), 
    2. Zufahrt (Asphalt/Schotter), 
    3. Solar-Potential. 
    Gliedere in RISIKEN, CHANCEN und KOSTEN.
    """
    
    response = model.generate_content([prompt, img])
    return response.text

# 3. App-Interface
st.set_page_config(page_title="Andalusien Invest Scout")
st.title("☀️ Andalusien Real Estate Master")

uploaded_file = st.file_uploader("Screenshot hochladen", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    st.divider()
    img = Image.open(uploaded_file)
    st.image(img, width=400)
    
    if st.button("🔍 Analyse starten"):
        with st.spinner("KI Gutachter prüft das Objekt..."):
            try:
                # Wir stellen sicher, dass das Bild im richtigen Format vorliegt
                result = analyze_image(img)
                st.markdown(result)
            except Exception as e:
                st.error(f"Fehler: {e}")
                st.info("Tipp: Wenn 'Model not found' erscheint, bitte die App einmal neu starten (Reboot).")

# Versionsinfo für uns zur Kontrolle
with st.sidebar:
    import google.generativeai as g
    st.write(f"KI-Bibliothek Version: {g.__version__}")
