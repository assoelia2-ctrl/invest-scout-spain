import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. API-Setup mit Fehlerprüfung
api_key = st.secrets.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    # Wir definieren das Modell hier noch nicht fest, um flexibel zu sein
else:
    st.error("API-Key fehlt in den Secrets!")

# 2. Robuste Analyse-Logik
def analyze_image(img):
    # Liste möglicher Modelle, falls eines nicht gefunden wird
    model_names = ['gemini-1.5-flash', 'gemini-pro-vision']
    
    prompt = "Du bist Baugutachter in Andalusien. Analysiere diesen Screenshot auf: 1. Substanz (Risse, Feuchtigkeit), 2. Zufahrt (Asphalt/Schotter), 3. Solar-Potential. Gliedere in RISIKEN, CHANCEN und KOSTEN."
    
    for name in model_names:
        try:
            model = genai.GenerativeModel(name)
            response = model.generate_content([prompt, img])
            return response.text
        except Exception:
            continue # Versuche das nächste Modell in der Liste
    
    return "Fehler: Keines der KI-Modelle konnte erreicht werden. Bitte prüfe die Version von google-generativeai."

# 3. App-Interface
st.set_page_config(page_title="Andalusien Invest Scout")
st.title("☀️ Andalusien Real Estate Master")

uploaded_files = st.file_uploader("Screenshots hochladen", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])

if uploaded_files:
    for i, file in enumerate(uploaded_files):
        st.divider()
        img = Image.open(file)
        st.image(img, width=300)
        
        if st.button(f"🔍 Analyse starten (Bild {i+1})", key=f"btn_{i}"):
            with st.spinner("KI Gutachter prüft das Objekt..."):
                try:
                    result = analyze_image(img)
                    st.markdown(result)
                except Exception as e:
                    st.error(f"Technischer Fehler: {e}")
