import streamlit as st
import requests
import pandas as pd

# 1. KONFIGURATION & KEY-CHECK
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
        return f"❌ Fehler {response.status_code}: Bitte kurz warten."
    except:
        return "📡 Verbindung zum Agenten unterbrochen."

def get_real_market_links(query, budget):
    """Erzeugt echte, funktionierende Links zu den Portalen."""
    # Basis-Links für die Provinz Málaga
    idealista = f"https://www.idealista.com/de/venta-viviendas/malaga-provincia/?precio-maximo={budget}"
    fotocasa = f"https://www.fotocasa.es/es/comprar/viviendas/malaga-provincia/todas-las-zonas/l?maxPrice={budget}"
    return idealista, fotocasa

# 2. BENUTZEROBERFLÄCHE (UI)
st.title("🤖 Málaga Investment-Zentrale")
st.success("Status: Groq-Agent aktiv & Live-Links bereit")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🔍 Suche & Strategie")
    user_input = st.text_input("Was suchst du? (z.B. Finca in Antequera)", value="Finca mit Garten in Málaga Umland")
    max_price = st.number_input("Max. Budget (€)", value=250000, step=5000)
    
    if st.button("🚀 Agenten-Analyse starten", use_container_width=True):
        with st.spinner("Agent wertet Marktdaten aus..."):
            # Der Agent liefert die strategische Beratung
            prompt = f"""
            Analysiere als Immobilien-Experte: {user_input} mit Budget {max_price}€. 
            Nenne 3 lukrative Gebiete in der Provinz Málaga für dieses Budget.
            Gib eine Einschätzung zur Wertsteigerung (Capital Growth) ab.
            Antworte kurz und präzise. Erfinde KEINE Immobilien-Links.
            """
            antwort = call_groq_agent(prompt)
            st.markdown("### 🤖 Strategische Analyse:")
            st.write(antwort)
            
            # Hier generieren wir die ECHTEN Links zu den Portalen
            id_link, fc_link = get_real_market_links(user_input, max_price)
            
            st.divider()
            st.subheader("🏠 Echte Live-Angebote öffnen:")
            st.info("Klicke auf die Buttons, um die aktuellen Inserate auf den Portalen zu sehen.")
            c1, c2 = st.columns(2)
            c1.link_button("👉 Idealista (Live-Ergebnisse)", id_link, use_container_width=True)
            c2.link_button("👉 Fot
