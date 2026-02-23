import streamlit as st
import pandas as pd
import requests
from openai import OpenAI

# 1. SETUP
st.set_page_config(page_title="Málaga Invest-Zentrale", layout="centered")

# Keys aus den Secrets laden
groq_key = st.secrets.get("GROQ_API_KEY")

# 2. FUNKTION ZUM AUSLESEN DES LINKS (Die Brücke zum Inhalt)
def fetch_web_content(url):
    try:
        # Jina Reader wandelt die Webseite (Idealista etc.) in Text um
        reader_url = f"https://r.jina.ai/{url}"
        response = requests.get(reader_url, timeout=10)
        if response.status_code == 200:
            return response.text[:5000] 
        return None
    except:
        return None

# 3. HEADER & EINGABE
st.title("🤖 Málaga Invest-Zentrale")

anzeigen_link = st.text_input("🔗 Link zur Anzeige (Idealista/Fotocasa):", placeholder="Hier Link einfügen...")

# 4. DER FEHLENDE ANALYSE-BUTTON (Zentral platziert)
if st.button("🚀 JETZT DATEN AUS LINK AUSLESEN & ANALYSIEREN", use_container_width=True):
    if anzeigen_link:
        with st.status("Extrahiere Daten aus der Webseite..."):
            web_text = fetch_web_content(anzeigen_link)
            
            if web_text:
                st.success("✅ Webseiten-Inhalt erfolgreich geladen!")
                
                if groq_key:
                    prompt = f"Analysiere diesen Immobilientext. Fasse m2, Zimmer, Lage und rechtliche Risiken (AFO/Rústico) kurz zusammen:\n\n{web_text}"
                    
                    url = "https://api.groq.com/openai/v1/chat/completions"
                    headers = {"Authorization": f"Bearer {groq_key}"}
                    payload = {
                        "model": "llama-3.3-70b-versatile",
                        "messages": [{"role": "user", "content": prompt}]
                    }
                    res = requests.post(url, json=payload, headers=headers).json()
                    
                    st.subheader("📋 Analyse-Ergebnis")
                    st.info(res['choices'][0]['message']['content'])
                else:
                    st.error("Groq-Key fehlt in den Secrets!")
            else:
                st.error("Konnte den Link nicht auslesen. Ist die URL korrekt?")
    else:
        st.warning("Bitte füge zuerst einen Link ein!")

st.divider()

# 5. FINANZ-RECHNER & KARTE (Wiederhergestellt)
col1, col2 = st.columns([1, 1])

with col1:
    preis = st.number_input("Kaufpreis (€):", value=250000, step=5000)
    itp = preis * 0.07
    st.metric("Steuern (7% ITP)", f"{itp:,.0f} €")
    st.metric("Gesamt-Invest", f"{preis + itp:,.0f} €")

with col2:
    st.write("📍 **Ungefähre Lage:**")
    # Beispiel-Karte für Málaga (wird angezeigt, sobald die App läuft)
    map_data = pd.DataFrame({'lat': [36.7212], 'lon': [-4.4214]})
    st.map(map_data, zoom=10)

# 6. CHAT-BEREICH
st.divider()
st.subheader("💬 Rückfragen zum Objekt")
chat_input = st.chat_input("Frage zum Risiko stellen...")

st.caption("✅ System: Link-Analyse aktiv | Karte & Rechner wiederhergestellt | Groq-Core")
