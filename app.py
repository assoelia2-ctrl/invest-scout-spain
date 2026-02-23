import streamlit as st
import pandas as pd
import requests

# 1. GRUND-EINSTELLUNGEN
st.set_page_config(page_title="Málaga Invest-Zentrale", layout="wide")

# Speicher für Chat und Objektdaten initialisieren
if "messages" not in st.session_state:
    st.session_state.messages = []
if "objekt_details" not in st.session_state:
    st.session_state.objekt_details = ""

groq_key = st.secrets.get("GROQ_API_KEY")

# 2. FUNKTION: WEBSEITE IN TEXT VERWANDELN
def link_auslesen(url):
    try:
        # Nutzung von Jina Reader als Brücke (umgeht Blockaden)
        reader_url = f"https://r.jina.ai/{url}"
        response = requests.get(reader_url, timeout=10)
        if response.status_code == 200:
            return response.text[:5000] # Die wichtigsten 5000 Zeichen
        return None
    except:
        return None

# 3. BENUTZEROBERFLÄCHE (UI)
st.title("🤖 Málaga Invest-Zentrale")

anzeigen_link = st.text_input("🔗 Immobilien-Link einfügen:", placeholder="https://www.idealista.com/...")

# Rechner und Karte nebeneinander
col_links, col_rechts = st.columns([1, 1])

with col_links:
    preis = st.number_input("Kaufpreis (€):", value=250000, step=5000)
    itp = preis * 0.07
    st.metric("Steuern (7% ITP)", f"{itp:,.0f} €")
    st.metric("Gesamt-Invest", f"{preis + itp:,.0f} €")

with col_rechts:
    # Karte zentriert auf Málaga
    map_data = pd.DataFrame({'lat': [36.7212], 'lon': [-4.4214]})
    st.map(map_data, zoom=9)

st.divider()

# 4. DER ENTSCHEIDENDE ANALYSE-BUTTON
if st.button("🚀 JETZT DATEN AUS LINK EXTRAHIEREN & ANALYSIEREN", use_container_width=True):
    if not anzeigen_link:
        st.warning("Bitte füge zuerst einen Link ein.")
    else:
        with st.spinner("KI liest die Anzeige und wertet Details aus..."):
            inhalt = link_auslesen(anzeigen_link)
            
            if inhalt:
                st.session_state.objekt_details = inhalt # Speichern für den Chat
                
                # KI-Analyse erstellen
                prompt = f"Du bist Immobilien-Experte. Analysiere diesen Text. Fasse m2, Zimmer, Lage und rechtliche Risiken (AFO, Rústico) zusammen:\n\n{inhalt}"
                
                headers = {"Authorization": f"Bearer {groq_key}"}
                payload = {
                    "model": "llama-3.3-70b-versatile",
                    "messages": [{"role": "user", "content": prompt}]
                }
                
                res = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers).json()
                ki_antwort = res['choices'][0]['message']['content']
                
                # Ergebnis im Chat speichern
                st.session_state.messages.append({"role": "assistant", "content": f"✅ **Analyse abgeschlossen:**\n\n{ki_antwort}"})
                st.rerun() # Sofortige Anzeige im Chat-Fenster erzwingen
            else:
                st.error("Konnte die Daten nicht vom Link abrufen. Bitte prüfe die URL.")

# 5. DER CHAT (Zeigt die Analyse und erlaubt Fragen)
st.subheader("💬 Experten-Dialog")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_frage := st.chat_input("Frage zu Details oder Risiken stellen..."):
    st.session_state.messages.append({"role": "user", "content": user_frage})
    with st.chat_message("user"):
        st.markdown(user_frage)

    with st.chat_message("assistant"):
        context = st.session_state.objekt_details
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": f"Du bist Immobilien-Experte. Kontext zum Objekt: {context}"},
                {"role": "user", "content": user_frage}
            ]
        }
        res = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers={"Authorization": f"Bearer {groq_key}"}).json()
        antwort = res['choices'][0]['message']['content']
        st.markdown(antwort)
        st.session_state.messages.append({"role": "assistant", "content": antwort})
