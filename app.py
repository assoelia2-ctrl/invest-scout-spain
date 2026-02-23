import streamlit as st
import requests
import base64

# --- KONFIGURATION ---
st.set_page_config(page_title="Málaga Invest: Final Edition", layout="wide", page_icon="🛡️")

# Sicherstellen, dass der API Key vorhanden ist
if "GROQ_API_KEY" not in st.secrets:
    st.error("Bitte hinterlege den GROQ_API_KEY in den Streamlit-Secrets!")
    st.stop()

groq_key = st.secrets["GROQ_API_KEY"]

if "messages" not in st.session_state:
    st.session_state.messages = []

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# --- BENUTZEROBERFLÄCHE ---
st.title("🛡️ Málaga Invest: 100% Risiko-Check")
st.info("Lade alle Screenshots einer Anzeige hoch. Ich prüfe Preise, m², Zustand und rechtliche Risiken (AFO/Rústico).")

# Sidebar für schnelle Berechnungen
with st.sidebar:
    st.header("Finanz-Rechner")
    kaufpreis = st.number_input("Kaufpreis (€)", value=250000, step=5000)
    itp = kaufpreis * 0.07
    st.write(f"ITP Steuer (7%): **{itp:,.0f} €**")
    st.success(f"Gesamt-Invest: **{kaufpreis + itp:,.0f} €**")

# Datei-Upload (Multi-Modus)
uploaded_files = st.file_uploader("Alle Screenshots hier reinziehen:", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    cols = st.columns(min(len(uploaded_files), 4))
    for i, file in enumerate(uploaded_files):
        with cols[i % 4]:
            st.image(file, use_container_width=True)

    if st.button("🚀 KOMPLETT-ANALYSE STARTEN", use_container_width=True):
        with st.spinner("KI führt Tiefenprüfung durch..."):
            
            # Der ultimative Prüf-Prompt
            content_list = [{
                "type": "text", 
                "text": """DU BIST EIN IMMOBILIEN-EXPERTE FÜR MÁLAGA. 
                Führe für alle Bilder zusammen diese Prüfung durch:
                1. DATEN: Preis, m2, Zimmer, Standort extrahieren.
                2. RECHT: Suche nach AFO, Rústico, DAFO, Proindiviso, Ocupado. (KRITISCH!)
                3. ZUSTAND: Analyse der Bausubstanz, Pool, Garten & Renovierungsstau.
                4. RECHERCHE: Erstelle Suchbegriffe, um das Objekt in anderen Portalen zu finden.
                Gib eine klare Empfehlung: KAUFEN, PRÜFEN oder FINGER WEG."""
            }]
            
            for file in uploaded_files:
                base64_img = encode_image(file)
                content_list.append({
                    "type": "image_url", 
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}
                })
            
            payload = {
                "model": "llama-3.2-11b-vision-preview",
                "messages": [{"role": "user", "content": content_list}],
                "temperature": 0.1 # Niedrige Temperatur für faktenbasierte Analyse
            }
            
            try:
                res = requests.post("https://api.groq.com/openai/v1/chat/completions", 
                                     json=payload, 
                                     headers={"Authorization": f"Bearer {groq_key}"}).json()
                
                analysis = res['choices'][0]['message']['content']
                st.session_state.messages.append({"role": "assistant", "content": analysis})
                st.rerun()
            except Exception as e:
                st.error(f"Fehler bei der Analyse: {e}")

# --- EXPERTEN-CHAT ---
st.divider()
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if chat_input := st.chat_input("Nachfrage zu diesem Objekt..."):
    st.session_state.messages.append({"role": "user", "content": chat_input})
    # (Hier würde die normale Chat-Antwort-Logik folgen)
    st.rerun()
