import streamlit as st
import requests
import base64
from PIL import Image
import io

# --- 1. SETUP ---
st.set_page_config(page_title="Málaga Invest Expert", layout="wide", page_icon="🛡️")

# Sicherstellen, dass der Key da ist
if "GROQ_API_KEY" not in st.secrets:
    st.error("❌ Kritischer Fehler: GROQ_API_KEY fehlt in den Secrets!")
    st.stop()

groq_key = st.secrets["GROQ_API_KEY"]

# --- 2. BILD-OPTIMIERUNG (Verhindert Daten-Stau) ---
def process_image(image_file):
    img = Image.open(image_file)
    if img.mode in ("RGBA", "P"): img = img.convert("RGB")
    # Verkleinerung für stabile Übertragung
    img.thumbnail((1024, 1024)) 
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG", quality=80)
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# --- 3. BENUTZEROBERFLÄCHE ---
st.title("🛡️ Invest-Scout: Finale Version")
st.info("Lade deine Screenshots hoch. Ich prüfe Recht, Boden & Zustand mit dem neuesten Experten-Modell.")

uploaded_files = st.file_uploader(
    "Screenshots wählen:", 
    type=["jpg", "png", "jpeg"], 
    accept_multiple_files=True
)

if uploaded_files:
    st.success(f"✅ {len(uploaded_files)} Bilder bereit zur Analyse.")
    
    if st.button("🚀 TIEFENPRÜFUNG STARTEN", use_container_width=True):
        with st.spinner("KI-Experte führt Risiko-Check durch..."):
            try:
                # Dein spezialisierter Prompt für Málaga
                content_list = [{
                    "type": "text", 
                    "text": """DU BIST EIN IMMOBILIEN-EXPERTE FÜR ANDALUSIEN.
                    Analysiere alle Bilder GEMEINSAM auf:
                    1. RECHTLICHE RISIKEN: Suche nach AFO, DAFO, Suelo Rústico, Ocupado, Proindiviso.
                    2. STANDORT & BODEN: Bewerte Bodenbeschaffenheit und Lage (Urbano/Rústico).
                    3. ZUSTAND: Analyse von Bausubstanz, Pool, Dach & Renovierungsstau.
                    4. DATEN: Extrahiere Preis, m2 und Ort."""
                }]
                
                for file in uploaded_files:
                    encoded = process_image(file)
                    content_list.append({
                        "type": "image_url", 
                        "image_url": {"url": f"data:image/jpeg;base64,{encoded}"}
                    })
                
                # --- DAS AKTUELLE PRODUKTIONS-MODELL ---
                payload = {
                    "model": "llama-3.2-90b-vision-preview",
                    "messages": [{"role": "user", "content": content_list}],
                    "temperature": 0.1
                }
                
                res = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"},
                    json=payload,
                    timeout=60
                )
                
                if res.status_code == 200:
                    st.markdown("---")
                    st.markdown("### 📋 Analyse-Ergebnis")
                    st.markdown(res.json()['choices'][0]['message']['content'])
                else:
                    st.error(f"⚠️ Schnittstellen-Meldung: {res.status_code}")
                    # Zeige hilfreiche Tipps statt nur Fehlercodes
                    if res.status_code == 400:
                        st.warning("Modell-Wechsel bei Groq erkannt. Bitte starte die App einmal neu (Reboot).")
                    st.expander("Details anzeigen").write(res.text)

            except Exception as e:
                st.error(f"🆘 Technischer Fehler: {e}")

st.divider()
st.caption("Version 6.0 - Produktions-Modell Llama 3.2 90B")
