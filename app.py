import streamlit as st
import requests
import base64

# --- 1. GRUNDKONFIGURATION ---
st.set_page_config(page_title="Málaga Invest Expert", layout="wide", page_icon="🛡️")

# API Key Check
if "GROQ_API_KEY" not in st.secrets:
    st.error("Fehler: GROQ_API_KEY fehlt in den Streamlit-Secrets!")
    st.stop()

groq_key = st.secrets["GROQ_API_KEY"]

if "messages" not in st.session_state:
    st.session_state.messages = []

# Funktion zur Bildumwandlung
def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# --- 2. BENUTZEROBERFLÄCHE ---
st.title("🛡️ Málaga Invest: Multi-Scan & Risiko-Check")
st.markdown("""
### So gehst du vor:
1. Mache Screenshots von der Anzeige (Preis, Text, Fotos).
2. Wähle **alle** Screenshots gleichzeitig aus.
3. Klicke auf den Analyse-Button.
""")

# Sidebar für die Steuer-Berechnung
with st.sidebar:
    st.header("📊 Kalkulation")
    preis_input = st.number_input("Kaufpreis laut Anzeige (€)", value=250000, step=1000)
    itp = preis_input * 0.07
    st.write(f"7% ITP Steuer: {itp:,.0f} €")
    st.subheader(f"Gesamt: {preis_input + itp:,.0f} €")

# --- 3. MULTI-UPLOAD BEREICH ---
# HIER IST DIE WICHTIGE ZEILE FÜR MEHRERE DATEIEN:
uploaded_files = st.file_uploader(
    "Screenshots hier hochladen (Mehrfachauswahl möglich):", 
    type=["jpg", "png", "jpeg"], 
    accept_multiple_files=True
)

if uploaded_files:
    st.info(f"📁 {len(uploaded_files)} Datei(en) ausgewählt.")
    
    # Bilder nebeneinander anzeigen
    cols = st.columns(min(len(uploaded_files), 3))
    for i, file in enumerate(uploaded_files):
        with cols[i % 3]:
            st.image(file, use_container_width=True)

    if st.button("🚀 ALLE BILDER JETZT ANALYSIEREN", use_container_width=True):
        with st.spinner("KI liest Texte und Bilder aus..."):
            
            # Vorbereitung der Multimodalen Nachricht
            content_list = [{
                "type": "text", 
                "text": """Du bist ein Experte für Immobilieninvestitionen in Málaga. 
                Analysiere alle hochgeladenen Screenshots zusammenfassend:
                1. EXTRAKTION: Preis, m2-Anzahl, Anzahl der Zimmer, genauer Ort.
                2. RISIKO-CHECK: Suche nach Hinweisen auf AFO, Rústico, DAFO, Proindiviso oder Ocupado.
                3. OPTIK: Zustand der Immobilie, des Pools und der Umgebung bewerten.
                4. FAZIT: Ist dies ein sicheres Investment oder gibt es 'Red Flags'?"""
            }]
            
            # Alle Bilder zur Liste hinzufügen
            for file in uploaded_files:
                base64_img = encode_image(file)
                content_list.append({
                    "type": "image_url", 
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}
                })
            
            payload = {
                "model": "llama-3.2-11b-vision-preview",
                "messages": [{"role": "user", "content": content_list}],
                "temperature": 0.1
            }
            
            try:
                response = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {groq_key}"},
                    json=payload
                )
                res_json = response.json()
                
                if 'choices' in res_json:
                    analysis = res_json['choices'][0]['message']['content']
                    st.session_state.messages.append({"role": "assistant", "content": analysis})
                    st.rerun()
                else:
                    st.error("Fehler von der KI-Schnittstelle erhalten. Bitte erneut versuchen.")
            except Exception as e:
                st.error(f"Technischer Fehler: {e}")

# --- 4. CHAT-HISTORIE ---
st.divider()
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if chat_input := st.chat_input("Frage zu diesem Objekt stellen..."):
    st.session_state.messages.append({"role": "user", "content": chat_input})
    st.rerun()
