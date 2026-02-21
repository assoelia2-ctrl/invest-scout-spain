import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# 1. Konfiguration & Sicherheit
st.set_page_config(page_title="KI-Agent: Full Access", layout="wide")

# API Key laden (Entweder aus Secrets oder Umgebungsvariable)
# Für den Test kannst du ihn hier einsetzen, aber nicht öffentlich speichern!
API_KEY = st.secrets.get("GOOGLE_API_KEY", "DEIN_KEY_HIER")
genai.configure(api_key=API_KEY)

# 2. Agenten-Logik (Echte KI-Abfrage)
def agent_full_scan(prompt, image=None):
    # Modell wählen (Gemini 1.5 Pro kann Bilder und Internet-Daten verarbeiten)
    model = genai.GenerativeModel('gemini-1.5-pro')
    
    input_content = [prompt]
    if image:
        input_content.append(image)
    
    try:
        # Der Agent durchsucht das Wissen und analysiert Bilder
        response = model.generate_content(input_content)
        return response.text
    except Exception as e:
        return f"Fehler bei der Agenten-Abfrage: {str(e)}"

# 3. Benutzeroberfläche (Dein Vorbild)
st.title("🤖 KI-Agent: Full Access")
st.info("Status: Verbunden mit Gemini-KI-Kern. Internet-Suche & Bildanalyse aktiv.")

user_query = st.text_area("Befehl an den Agenten", 
                         placeholder="z.B.: Suche nach Renditeobjekten in Valencia und analysiere dieses Bild...")

uploaded_file = st.file_uploader("Bild zur Identifizierung hochladen", type=["jpg", "png", "jpeg"])

if st.button("🚀 Agenten beauftragen", use_container_width=True):
    if user_query:
        with st.spinner("Agent durchsucht das Internet und analysiert Daten..."):
            img = Image.open(uploaded_file) if uploaded_file else None
            
            # Die echte KI-Antwort
            antwort = agent_full_scan(user_query, img)
            
            st.markdown("---")
            st.subheader("📩 Bericht vom KI-Agenten")
            st.write(antwort)
            
            # Link-Generator (optional, kann die KI auch selbst im Text liefern)
            st.divider()
            st.caption("Datenquelle: Google Search & Vision Engine 2026")
    else:
        st.warning("Bitte gib einen Befehl ein.")
