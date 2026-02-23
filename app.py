import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. KEY DIREKT AUS DEN CLOUD-SECRETS LADEN ---
api_key = st.secrets.get("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("API-Key fehlt in den Secrets! Bitte prüfe die Streamlit-Cloud-Einstellungen.")

# --- 2. ANALYSE FUNKTION ---
def analyze_image(img):
    prompt = """
    Du bist ein zertifizierter Baugutachter für Immobilien in Andalusien.
    Analysiere diesen Screenshot technisch:
    1. Substanz (Risse, Salpeter/Humedad).
    2. Zufahrt (Carril oder asphaltiert).
    3. Solar-Potential & Schatten.
    Gliedere in: 🚩 RISIKEN, ✨ CHANCEN, 💶 KOSTEN-SCHÄTZUNG.
    """
    response = model.generate_content([prompt, img])
    return response.text

# --- 3. APP INTERFACE ---
st.title("☀️ Andalusien Real Estate AI-Expert")

# Datei Upload
Dateien = st.file_uploader("Screenshots hochladen", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])

if Dateien:
    for i, d in enumerate(Dateien):
        st.markdown("---")
        img = Image.open(d)
        st.image(img, width=400)
        
        if st.button(f"🔍 KI-Gutachten starten (Objekt {i+1})", key=f"btn_{i}"):
            if api_key:
                with st.spinner("Analyse läuft..."):
                    ergebnis = analyze_image(img)
                    st.markdown(ergebnis)
            else:
                st.warning("Kein API-Key verfügbar.")
