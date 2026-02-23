import streamlit as st
import requests
import base64
from PIL import Image
import io

# --- 1. SETUP ---
st.set_page_config(page_title="Málaga Invest Expert", layout="wide", page_icon="🛡️")

if "GROQ_API_KEY" not in st.secrets:
    st.error("🔑 GROQ_API_KEY fehlt in den Streamlit-Secrets!")
    st.stop()

groq_key = st.secrets["GROQ_API_KEY"]

# --- 2. BILD-OPTIMIERUNG (Verhindert Abstürze) ---
def process_image(image_file):
    img = Image.open(image_file)
    if img.mode in ("RGBA", "P"): img = img.convert("RGB")
    img.thumbnail((1024, 1024)) 
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG", quality=80)
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# --- 3. UI ---
st.title("🛡️ Invest-Scout: Finaler Risiko-Check")
st.info("Lade Screenshots (Idealista, Fotos etc.) hoch. Ich prüfe Recht, Boden & Zustand.")

uploaded_files = st.file_uploader(
    "Bilder auswählen:", 
    type=["jpg", "png", "jpeg"], 
    accept_multiple_files=True
)

if uploaded_files:
    st.success(f"✅ {len(uploaded_files)} Bilder bereit.")
    
    if st.button("🚀 TIEFENPRÜFUNG STARTEN", use_container_width=True):
        with st.spinner("Experten-Analyse läuft..."):
            try:
                # Master-Prompt mit all deinen Anforderungen
                content_list = [{
                    "type": "text", 
                    "text": """DU BIST EIN IMMOBILIEN-EXPERTE FÜR ANDALUSIEN.
                    Analysiere diese Bilder GEMEINSAM auf:
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
                
                # --- DAS NEUE STABILE MODELL ---
                payload = {
                    "model": "llama-3.2-90b-vision-preview",
                    "messages": [{"role": "user", "content": content_list}],
                    "temperature": 0.1
                }
                
                res = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {groq_key}"},
                    json=payload
                )
                
                if res.status_code == 200:
                    st.markdown("### 📋 Analyse-Ergebnis")
                    st.markdown(res.json()['choices'][0]['message']['content'])
                else:
                    # Falls Groq das Modell wieder nicht findet, versuchen wir automatisch das Backup
                    st.warning("Hauptmodell überlastet. Nutze Backup-Analyse...")
                    payload["model"] = "llama-3.2-11b-vision-preview" 
                    res = requests.post("https://api.groq.com/openai/v1/chat/completions", 
                                         headers={"Authorization": f"Bearer {groq_key}"}, json=payload)
                    if res.status_code == 200:
                        st.markdown(res.json()['choices'][0]['message']['content'])
                    else:
                        st.error(f"Kritischer Fehler: {res.status_code}")
                        st.write(res.text)
            except Exception as e:
                st.error(f"Technischer Fehler: {e}")

st.divider()
st.caption("Version 5.0 - Stabilitäts-Update")
