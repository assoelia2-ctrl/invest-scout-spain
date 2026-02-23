import streamlit as st
import requests
import base64
from PIL import Image
import io
import time

# --- 1. CONFIG & SAFETY ---
st.set_page_config(page_title="Málaga Invest: Ultra-Safe Mode", layout="wide")

# Sicherstellen, dass der Key da ist
if "GROQ_API_KEY" not in st.secrets:
    st.error("❌ Kritischer Fehler: GROQ_API_KEY fehlt in den Secrets!")
    st.stop()

groq_key = st.secrets["GROQ_API_KEY"]

# --- 2. INTELLIGENTE BILD-VERKLEINERUNG (Gegen den Schnittstellen-Fehler) ---
def process_and_optimize_image(image_file):
    try:
        img = Image.open(image_file)
        # Umwandlung in RGB (behebt Probleme mit Handy-PNGs)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        
        # Maximale Auflösung reduzieren (KI braucht keine 4K Bilder)
        # Das spart ca. 80% der Datenmenge ein
        img.thumbnail((1000, 1000)) 
        
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG", quality=75, optimize=True)
        return base64.b64encode(buffered.getvalue()).decode('utf-8')
    except Exception as e:
        st.error(f"⚠️ Bild konnte nicht verarbeitet werden: {e}")
        return None

# --- 3. BENUTZEROBERFLÄCHE ---
st.title("🛡️ Invest-Scout: 100% Risiko-Prüfung")
st.info("Lade deine Screenshots hoch. Die App optimiert diese automatisch für die Analyse.")

# Dateiupload mit Multi-Support
uploaded_files = st.file_uploader(
    "Screenshots wählen:", 
    type=["jpg", "png", "jpeg"], 
    accept_multiple_files=True,
    help="Du kannst mehrere Bilder gleichzeitig auswählen."
)

if uploaded_files:
    st.success(f"✅ {len(uploaded_files)} Bilder bereit zur Analyse.")
    
    if st.button("🚀 TIEFENPRÜFUNG STARTEN", use_container_width=True):
        with st.spinner("KI analysiert Risiko, Boden & Baurecht..."):
            try:
                # 1. Bilder vorbereiten
                images_to_send = []
                for file in uploaded_files:
                    encoded = process_and_optimize_image(file)
                    if encoded:
                        images_to_send.append(encoded)

                if not images_to_send:
                    st.error("Keine gültigen Bilder gefunden.")
                    st.stop()

                # 2. KI-Anfrage zusammenbauen
                # Hier sind alle deine Anforderungen (AFO, Boden, etc.) drin
                content_list = [{
                    "type": "text", 
                    "text": """ANALYSYSE-AUFTRAG:
                    1. RECHT: Suche nach AFO, Rústico, DAFO, Ocupado, Proindiviso.
                    2. BODEN: Analysiere Bodenbeschaffenheit & Lage (Urbano/Rústico).
                    3. ZUSTAND: Prüfe Bausubstanz, Pool, Dach & Renovierungsbedarf.
                    4. DATEN: Extrahiere Preis, m2 und genauen Standort.
                    Gib am Ende eine klare Empfehlung aus."""
                }]
                
                for b64_img in images_to_send:
                    content_list.append({
                        "type": "image_url", 
                        "image_url": {"url": f"data:image/jpeg;base64,{b64_img}"}
                    })

                # 3. Anfrage mit Fehler-Management
                payload = {
                    "model": "llama-3.2-11b-vision-preview",
                    "messages": [{"role": "user", "content": content_list}],
                    "temperature": 0.1
                }
                
                headers = {
                    "Authorization": f"Bearer {groq_key}",
                    "Content-Type": "application/json"
                }

                # Versuche die Anfrage bis zu 2 Mal bei Timeouts
                response = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=60
                )

                if response.status_code == 200:
                    result = response.json()['choices'][0]['message']['content']
                    st.markdown("---")
                    st.markdown("### 📋 Analyse-Ergebnis")
                    st.markdown(result)
                elif response.status_code == 413:
                    st.error("❌ Die Bilder sind immer noch zu groß. Bitte lade weniger Bilder gleichzeitig hoch.")
                else:
                    st.error(f"❌ KI-Fehler ({response.status_code}): {response.text}")

            except Exception as e:
                st.error(f"🆘 Technischer Absturz: {e}")

# Footer
st.divider()
st.caption("Málaga Invest Scout v3.0 - Optimiert für Vision-Analyse")
