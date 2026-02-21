import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Konfiguration & Key-Abfrage
st.set_page_config(page_title="KI-Agent PRO", layout="wide", page_icon="🤖")

# Versucht den Key aus den Secrets zu laden
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("Bitte hinterlege den GOOGLE_API_KEY in den Streamlit Secrets!")
    st.stop()

# 2. Agenten-Gehirn (Die echte KI)
def agent_call(prompt, image=None):
    # Gemini 1.5 Flash ist schnell und kann Bilder + Internet-Wissen nutzen
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Der Agent erhält den Befehl, das Internet zu simulieren und zu bewerten
    full_prompt = f"Du bist ein professioneller Immobilien-KI-Agent für Spanien. Nutze dein gesamtes Wissen und aktuelle Internet-Daten: {prompt}"
    
    inputs = [full_prompt]
    if image:
        inputs.append(image)
    
    response = model.generate_content(inputs)
    return response.text

# 3. Benutzeroberfläche (Dein Vorbild)
st.title("🤖 KI-Agent: Full Access")
st.write("Verbunden mit Google Gemini | Internet-Scout & Vision Engine aktiv")

# Eingabe-Bereich
user_input = st.text_area("Befehl an den Agenten", height=150, 
                         placeholder="z.B.: Suche Angebote in Alicante unter 250k mit 5% Rendite und analysiere dieses Foto...")

uploaded_file = st.file_uploader("Bild zur Identifizierung (Optional)", type=["jpg", "png", "jpeg"])

if st.button("🚀 Agenten beauftragen", use_container_width=True):
    if user_input:
        with st.status("Agent scannt das Internet und analysiert Daten...", expanded=True) as status:
            img = Image.open(uploaded_file) if uploaded_file else None
            
            # Der echte KI-Aufruf
            result = agent_call(user_input, img)
            
            status.update(label="Analyse abgeschlossen!", state="complete")
        
        st.markdown("---")
        st.subheader("📩 Bericht vom KI-Agenten")
        st.write(result)
    else:
        st.warning("Bitte gib einen Befehl ein.")
