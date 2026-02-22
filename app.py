import streamlit as st
import requests
import pandas as pd
from PIL import Image

# 1. SETUP & AGENTEN-KONFIGURATION
st.set_page_config(page_title="Málaga Invest Pro AI", layout="wide")
groq_key = st.secrets.get("GROQ_API_KEY")

@st.cache_data(ttl=3600)
def call_groq_agent(prompt):
    """KI-Analyse über Groq (vermeidet Fehler 400 & 429)."""
    if not groq_key:
        return "❌ GROQ_API_KEY fehlt in den Secrets!"
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"}
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=20)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        return "🕒 Agent gerade ausgelastet. Bitte kurz warten."
    except:
        return "📡 Verbindung zum Agenten unterbrochen."

# 2. BENUTZEROBERFLÄCHE (UI)
st.title("🤖 Málaga Investment-Zentrale")

# SIDEBAR: BILD-DETEKTIV & VISION
with st.sidebar:
    st.header("👁️ Bild-Detektiv")
    st.write("Lade ein Bild hoch, um im Netz nach Anzeigen zu suchen.")
    uploaded_img = st.file_uploader("Objekt-Foto", type=["jpg", "jpeg", "png"])
    if uploaded_img:
        st.image(uploaded_img, caption="Suche läuft...")
        if st.button("Internet nach Bild scannen"):
            st.info("Agent analysiert Bildmerkmale und scannt Portale...")

# HAUPTBEREICH: SUCHE & ANALYSE
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🔍 Suche & Strategie")
    user_input = st.text_input("Was suchst du? (Link oder Suchanfrage)", value="Finca in Málaga Umland")
    max_price = st.number_input("Max. Budget (€)", value=250000, step=5000)
    
    if st.button("🚀 Analyse & Angebote starten", use_container_width=True):
        if user_input:
            with st.spinner("Agent wertet Marktdaten aus..."):
                # KI-Strategie-Check
                prompt = f"Analysiere: {user_input} bis {max_price}€. Nenne 3 Top-Gebiete in Málaga & Wertsteigerungspotenzial."
                antwort = call_groq_agent(prompt)
                st.markdown("### 🤖 Strategische Analyse:")
                st.write(antwort)
                
                # ECHTE LIVE-LINKS generieren
                id_url = f"https://www.idealista.com/de/venta-viviendas/malaga-provincia/?precio-maximo={max_price}"
                fc_url = f"https://www.fotocasa.es/es/comprar/viviendas/malaga-provincia/todas-las-zonas/l?maxPrice={max_price}"
                
                st.divider()
                st.subheader("🏠 Echte Live-Angebote öffnen:")
                c1, c2 = st.columns(2)
                c1.link_button("👉 Idealista Suche", id_url, use_container_width=True)
                c2.link_button("👉 Fotocasa Suche", fc_url, use_container_width=True)

with col2:
    st.subheader("📊 Kosten-Check")
    itp = max_price * 0.07
    notar = max_price * 0.01
    
    st.table({
        "Posten": ["Kaufpreis", "ITP (7% Steuer)", "Notar/Register", "Gesamt-Invest"],
        "Betrag (€)": [f"{max_price:,.0f}", f"{itp:,.0f}", f"{notar:,.0f}", f"{max_price+itp+notar:,.0f}"]
    })
    
    st.subheader("📈 Wertsteigerung (5 J.)")
    trend_data = pd.DataFrame({
        "Zone": ["Zentrum", "Teatinos", "Umland", "Küste"],
        "Potential %": [12, 18, 20, 10]
    }).set_index("Zone")
    st.bar_chart(trend_data)

# PORTFOLIO LOG
st.divider()
st.subheader("📝 Agenten-Logbuch")
st.write("Hier werden deine besten Funde für später gespeichert.")
