import streamlit as st
import pandas as pd
import requests

# 1. KONFIGURATION & SPEICHER (Session State)
st.set_page_config(page_title="Málaga Invest-Zentrale", layout="wide")

# Verhindert, dass Daten beim Tippen oder Laden verschwinden
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_context" not in st.session_state:
    st.session_state.last_context = ""

groq_key = st.secrets.get("GROQ_API_KEY")

# 2. DER ROBUSTE LINK-READER (Gegen 403-Blockaden)
def get_web_text(url):
    try:
        # Nutzung von Jina Reader als Brücke
        reader_url = f"https://r.jina.ai/{url}"
        # Tarnung als echter Browser
        headers = {
            "X-Return-Format": "markdown",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(reader_url, headers=headers, timeout=12)
        
        # Prüfung ob der Inhalt wirklich Objektdaten enthält oder eine Fehlermeldung
        if response.status_code == 200 and "Forbidden" not in response.text and len(response.text) > 200:
            return response.text[:7000] # Die wichtigsten 7000 Zeichen
        return "BLOCK_403"
    except:
        return None

# 3. BENUTZEROBERFLÄCHE (UI)
st.title("🤖 Málaga Invest-Zentrale")

# Link-Eingabe (Purer Fokus auf Funktionalität)
link_input = st.text_input("🔗 Link zur Anzeige (Idealista/Fotocasa):", placeholder="Link hier einfügen...")

col_calc, col_map = st.columns([1, 1])
with col_calc:
    preis = st.number_input("Kaufpreis (€):", value=250000, step=5000)
    itp = preis * 0.07
    st.info(f"💰 Grunderwerbsteuer (7% ITP): {itp:,.0f} €")
    st.success(f"📈 Gesamt-Invest: {preis + itp:,.0f} €")

with col_map:
    # Karte bleibt stabil auf Málaga zentriert
    st.map(pd.DataFrame({'lat': [36.72], 'lon': [-4.42]}), zoom=9)

st.divider()

# 4. DIE ANALYSE-LOGIK (Löst das Link-Problem endgültig)
if st.button("🚀 ANALYSE STARTEN", use_container_width=True):
    if not link_input:
        st.warning("Bitte füge zuerst einen Link ein!")
    elif not groq_key:
        st.error("GROQ_API_KEY fehlt in den Streamlit-Secrets!")
    else:
        with st.spinner("Versuche Link-Daten auszulesen..."):
            web_content = get_web_text(link_input)
            
            if web_content == "BLOCK_403":
                st.error("❌ Zugriff verweigert (403). Idealista blockiert den automatischen Scan.")
                st.info("💡 **Kein Problem:** Kopiere einfach den Text der Anzeige (m2, Zimmer, Beschreibung) und füge ihn unten im Chat ein. Ich analysiere ihn sofort!")
            elif web_content:
                st.session_state.last_context = web_content
                
                # KI-Analyse via Groq (umgeht OpenAI Quota-Problem)
                prompt = f"Analysiere diese Immobilie kurz und knackig. m2, Zimmer, Lage, Preis. Prüfe auf AFO/Rústico Risiken:\n\n{web_content}"
                
                headers = {"Authorization": f"Bearer {groq_key}"}
                payload = {
                    "model": "llama-3.3-70b-versatile",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.1
                }
                
                try:
                    res = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers).json()
                    analysis = res['choices'][0]['message']['content']
                    st.session_state.messages.append({"role": "assistant", "content": f"✅ **Link-Analyse abgeschlossen:**\n\n{analysis}"})
                    st.rerun()
                except:
                    st.error("KI-Dienst aktuell nicht erreichbar.")
            else:
                st.error("Link konnte nicht verarbeitet werden.")

# 5. DER EXPERTEN-CHAT (Gedächtnis-Funktion)
st.subheader("💬 Experten-Dialog")

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if chat_query := st.chat_input("Frage stellen oder Text hier reinkopieren..."):
    st.session_state.messages.append({"role": "user", "content": chat_query})
    with st.chat_message("user"):
        st.markdown(chat_query)

    with st.chat_message("assistant"):
        # Falls oben ein Link gelesen wurde, nutzt die KI dieses Wissen hier automatisch
        system_context = f"Objekt-Informationen: {st.session_state.last_context}" if st.session_state.last_context else "Keine Link-Daten vorhanden."
        
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": f"Du bist Immobilien-Experte für Málaga. {system_context}"},
                {"role": "user", "content": chat_query}
            ]
        }
        res = requests.post("https://api.groq.com/openai/v1/chat/completions", 
                             json=payload, headers={"Authorization": f"Bearer {groq_key}"}).json()
        ans = res['choices'][0]['message']['content']
        st.markdown(ans)
        st.session_state.messages.append({"role": "assistant", "content": ans})
