import streamlit as st
import requests
import base64
from PIL import Image
import io

# --- 1. CONFIG ---
st.set_page_config(page_title="Málaga Invest Expert", layout="wide", page_icon="🛡️")

# API Key Prüfung
if "GROQ_API_KEY" not in st.secrets:
    st.error("🔑 Fehler: GROQ_API_KEY fehlt in den Streamlit-Secrets!")
    st.stop()

groq_key = st.secrets["GROQ_API_KEY"]

# --- 2. BILD-OPTIMIERUNG (Verhindert Fehler 413) ---
def process_image(image_file):
    img = Image.open(image_file)
    if img.mode in ("RGBA", "P"): img = img.convert("RGB")
    # Reduktion auf 1024px für maximale Stabilität
    img.thumbnail((1024, 1024)) 
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG", quality=80)
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# --- 3. UI ---
st.title("🛡️ Málaga Invest: Profi-Risiko-Check")
st.markdown("Lade Screenshots hoch. Analyse von **AFO, Rústico, Boden & Zustand**.")

uploaded_files = st.file_uploader(
    "Screenshots wählen (Mehrfachauswahl):", 
    type=["jpg", "png", "jpeg"], 
    accept_multiple_files=True
)

if uploaded_files:
    st.success(f"✅ {len(uploaded_files)} Bilder bereit.")
    
    if st.button("🚀 TIEFENPRÜFUNG STARTEN", use_container_width=True):
        with st.spinner("KI-Experte analysiert..."):
            try:
                # Dein Experten-Prompt
                content_list = [{
                    "type": "text", 
                    "text": """ANALYSYSE-AUFTRAG:
                    1. RECHT: Suche nach AFO, Rústico, DAFO, Ocupado, Proindiviso.
                    2. BODEN: Analysiere Bodenbeschaffenheit & Lage (Urbano/Rústico).
                    3. ZUSTAND: Prüfe Bausubstanz, Pool, Dach & Renovierungsbedarf.
                    4. DATEN: Extrahiere Preis, m2 und genauen Standort."""
                }]
                
                for file in uploaded_files:
                    encoded = process_image(file)
                    content_list.append({
                        "type": "image_url", 
                        "image_url": {"url": f"data:image/jpeg;base64,{encoded}"}
                    })

                # --- FAIL-SAFE MODELL-LISTE ---
                # Wir versuchen erst 90b, falls Groq wieder schraubt, nehmen wir 11b
                models_to_try = ["llama-3.2-90b-vision-preview", "llama-3.2-11b-vision-preview"]
                success = False

                for model_id in models_to_try:
                    if success: break
                    
                    payload = {
                        "model": model_id,
                        "messages": [{"role": "user", "content": content_list}],
                        "temperature": 0.1
                    }
                    
                    res = requests.post(
                        "https://api.groq.com/openai/v1/chat/completions",
                        headers={"Authorization": f"Bearer {groq_key}"},
                        json=payload,
                        timeout=45
                    )
                    
                    if res.status_code == 200:
                        st.markdown("### 📋 Analyse-Ergebnis")
                        st.markdown(res.json()['choices'][0]['message']['content'])
                        success = True
                    elif res.status_code == 400:
                        continue # Versuche das nächste Modell in der Liste
                    else:
                        st.error(f"Fehler {res.status_code}: {res.text}")
                        break

                if not success:
                    st.error("❌ Alle KI-Modelle sind aktuell bei Groq im Wartungsmodus. Bitte in 10 Min. erneut versuchen.")

            except Exception as e:
                st.error(f"🆘 Technischer Fehler: {e}")

st.divider()
st.caption("Version 8.0 - Ultra-Stable Edition")
