import streamlit as st
import pandas as pd
import requests

# 1. INITIALISIERUNG & UI-LAYOUT
st.set_page_config(page_title="Málaga Invest-Zentrale", layout="wide")

# Speicher für Chat und Objektdaten (Verhindert Datenverlust beim Neuladen)
if "messages" not in st.session_state:
    st.session_state.messages = []
if "link_data" not in st.session_state:
    st.session_state.link_data = ""

groq_key = st.secrets.get("GROQ_API_KEY")

# 2. PROFI-LINK-READER (Tarn-Modus gegen 403-Fehler)
def fetch_safe_content(url):
    try:
        reader_url = f"https://r.jina.ai/{url}"
        # Tarnt die Anfrage als mobilen Safari-Browser auf einem iPhone
        headers = {
            "X-Return-Format": "markdown",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
        }
        response = requests.get(reader_url, headers=headers, timeout=15)
        if response.status_code == 200 and len(response.text) > 150:
            return response.text[:6000]
        return None
    except:
        return None

# 3. BENUTZEROBERFLÄCHE (iPhone-optimiert)
st.title("🤖 Málaga Invest-Zentrale")

anzeigen_link = st.text_input("🔗 Link zur Anzeige (Idealista/Fotocasa):", placeholder="Link hier einfügen...")

col_map, col_calc = st.columns([1, 1])
with col_map:
    # Karte zentriert auf Málaga
    map_data = pd.DataFrame({'lat': [36.7212], 'lon': [-4.4214]})
    st.map(map_data, zoom=9)

with col_calc:
    preis = st.number_input("Kaufpreis (€):", value=250000, step=5000)
    itp = preis * 0.07
    st.success(f"💰 ITP (7%): {itp:,.0f} € | Gesamt: {preis + itp:,.0f} €")

st.divider()

# 4. ANALYSE-LOGIK (Der Daten-Extraktor)
if st.button("🚀 JETZT DATEN AUS LINK ANALYSIEREN", use_container_width=True):
    if not anzeigen_link:
        st.warning("Bitte füge zuerst einen Link ein!")
    elif not groq_key:
        st.error("GROQ_API_KEY fehlt in den Secrets!")
    else:
        with st.spinner("Lese Anzeige aus und erstelle Analyse..."):
            raw_content = fetch_safe_content(anzeigen_link)
            
            if raw_content:
                st.session_state.link_data = raw_content
                prompt = f"Analysiere diese Immobilienanzeige präzise. Fasse m2, Zimmer, Lage und rechtliche Risiken (AFO, Rústico, DAFO) zusammen:\n\n{raw_content}"
                
                try:
                    headers = {"Authorization": f"Bearer {groq_key}"}
                    payload = {
                        "model": "llama-3.3-70b-versatile",
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.1
                    }
                    res = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers).json()
                    answer = res['choices'][0]['message']['content']
                    
                    # Ergebnis in den Chat-Verlauf legen
                    st.session_state.messages.append({"role": "assistant", "content": f"📋 **Analyse abgeschlossen:**\n\n{answer}"})
                    st.rerun() # Seite neu laden um Chat anzuzeigen
                except Exception as e:
                    st.error(f"KI-Fehler: {e}")
            else:
                st.error("❌ Zugriff blockiert (403). Das Portal lässt den automatischen Scan gerade nicht zu.")
                st.info("💡 **Tipp:** Kopiere einfach den Beschreibungstext der Anzeige und füge ihn unten im Chat ein. Ich analysiere ihn sofort!")

# 5. DER CHAT-EXPERTE (Mit Langzeit-Gedächtnis)
st.subheader("💬 Experten-Dialog")

# Verlauf anzeigen
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Eingabe für Fragen oder Text-Kopien
if chat_prompt := st.chat_input("Frage stellen oder Text hier reinkopieren..."):
    st.session_state.messages.append({"role": "user", "content": chat_prompt})
    with st.chat_message("user"):
        st.markdown(chat_prompt)

    with st.chat_message("assistant"):
        # Nutzt die Link-Daten als Kontext, falls sie existieren
        context = f"Hier sind die Daten zum Objekt: {st.session_state.link_data}" if st.session_state.link_data else "Keine Link-Daten vorhanden."
        
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": f"Du bist Immobilien-Experte für Málaga. {context}"},
                {"role": "user", "content": chat_prompt}
            ]
        }
        res = requests.post("https://api.groq.com/openai/v1/chat/completions", 
                             json=payload, headers={"Authorization": f"Bearer {groq_key}"}).json()
        full_res = res['choices'][0]['message']['content']
        st.markdown(full_res)
        st.session_state.messages.append({"role": "assistant", "content": full_res})
