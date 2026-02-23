import streamlit as st
import requests
import base64
from PIL import Image
import io

# --- 1. SETUP & DESIGN ---
st.set_page_config(page_title="Málaga Invest: Final Master", layout="wide", page_icon="🛡️")

# API Key Sicherheit
if "GROQ_API_KEY" not in st.secrets:
    st.error("🔑 GROQ_API_KEY fehlt in den Streamlit-Secrets!")
    st.stop()

groq_key = st.secrets["GROQ_API_KEY"]

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 2. BILD-OPTIMIERUNG (Gegen Fehler 413/Schnittstellenfehler) ---
def process_image(image_file):
    img = Image.open(image_file)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    # Maximale Größe für stabile API-Übertragung
    img.thumbnail((1024, 1024)) 
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG", quality=85)
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# --- 3. INTERFACE ---
st.title("🛡️ Málaga Invest: 100% Risiko- & Objekt-Check")
st.markdown("Lade Screenshots (Idealista/Fotocasa) oder Fotos vor Ort hoch. Die KI prüft alles auf einmal.")

# Sidebar für Finanzen
with st.sidebar:
    st.header("📊 Investment-Rechner")
    preis = st.number_input("Kaufpreis (€)", value=250000, step=5000)
    itp = preis * 0.07
    st.write(f"7% ITP Steuer: **{itp:,.0f} €**")
    st.success(f"Gesamt-Invest: **{preis + itp:,.0f} €**")
    st.divider()
    st.info("Tipp: Lade mehrere Screenshots hoch (Preis, Beschreibung, Bilder), um das beste Ergebnis zu erhalten.")

# MULTI-UPLOAD BEREICH
uploaded_files = st.file_uploader(
    "Screenshots/Fotos hier hochladen:", 
    type=["jpg", "png", "jpeg"], 
    accept_multiple_files=True
)

if uploaded_files:
    # Zeige Vorschau
    cols = st.columns(min(len(uploaded_files), 4))
    for i, file in enumerate(uploaded_files):
        with cols[i % 4]:
            st.image(file, use_container_width=True)

    if st.button("🚀 VOLL-ANALYSE STARTEN", use_container_width=True):
        with st.spinner("KI führt Tiefenprüfung durch..."):
            try:
                # Der Master-Prompt für alle Prüfverfahren
                prompt_text = """DU BIST EIN IMMOBILIEN-EXPERTE FÜR ANDALUSIEN.
                Analysiere alle Bilder GEMEINSAM auf folgende Punkte:
                1. RECHTLICHE RISIKEN: Suche nach AFO, DAFO, Suelo Rústico, Proindiviso, Ocupado. (SEHR WICHTIG!)
                2. OBJEKT-DATEN: Preis, m2, Zimmer, Lage aus dem Text extrahieren.
                3. STANDORT & BODEN: Bewerte die Lage (Hang, Tal, Urban) und Bodenbeschaffenheit laut Fotos.
                4. ZUSTAND: Analyse von Bausubstanz, Dach, Pool und Modernisierungsbedarf.
                5. FAZIT: Klare Empfehlung (Kauf, Vorsicht, Finger weg)."""

                content_list = [{"type": "text", "text": prompt_text}]
                
                for file in uploaded_files:
                    base64_img = process_image(file)
                    content_list.append({
                        "type": "image_url", 
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}
                    })
                
                payload = {
                    "model": "llama-3.2-11b-vision-preview",
                    "messages": [{"role": "user", "content": content_list}],
                    "temperature": 0.1
                }
                
                headers = {"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"}
                response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
                
                if response.status_code == 200:
                    analysis = response.json()['choices'][0]['message']['content']
                    st.session_state.messages.append({"role": "assistant", "content": analysis})
                    st.rerun()
                else:
                    st.error(f"Schnittstellen-Fehler ({response.status_code}): {response.text}")

            except Exception as e:
                st.error(f"Technischer Fehler: {e}")

# --- 4. EXPERTEN-DIALOG ---
st.divider()
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if chat_input := st.chat_input("Nachfrage zum Objekt stellen..."):
    st.session_state.messages.append({"role": "user", "content": chat_input})
    st.rerun()
