import streamlit as st
import requests
import pandas as pd

# 1. KONFIGURATION
st.set_page_config(page_title="Málaga Invest Pro & Chat", layout="centered")
groq_key = st.secrets.get("GROQ_API_KEY")

# 2. KOMPAKTES INTERFACE (Preisleiste entfernt)
st.title("🤖 Málaga Invest-Zentrale")

# Eingabe der Links und Objektdaten
anzeigen_link = st.text_input("🔗 Link zur Immobilien-Anzeige:", placeholder="Idealista, Fotocasa...")
g_link = st.text_input("🖼️ Google-Foto Link des Objekts:")

c_typ, c_preis = st.columns([2, 1])
with c_typ:
    objekt = st.text_input("Haus-Typ/Region:", value="Finca Málaga")
with c_preis:
    preis = st.number_input("Preis (€):", value=250000, step=5000)

# Kostenberechnung (7% ITP Andalusien)
itp = preis * 0.07
st.success(f"💰 **Kosten-Struktur:** ITP (7%): {itp:,.0f} € | Gesamt: {preis + itp:,.0f} €")

# 3. INTERAKTIVES CHAT-FELD (Für Aufgaben & Feedback)
st.subheader("💬 Chat mit deinem Experten")
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat-Verlauf anzeigen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Neues Chat-Eingabefeld
if prompt := st.chat_input("Was soll ich prüfen? (z.B. 'Prüfe Airbnb-Lizenz' oder 'Was passt nicht?')"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if groq_key:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {groq_key}"}
            full_prompt = f"Kontext: {objekt} für {preis}€. Anzeige: {anzeigen_link}. Aufgabe: {prompt}"
            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "system", "content": "Du bist ein Immobilien-Experte für Málaga."},
                             {"role": "user", "content": full_prompt}]
            }
            try:
                response = requests.post(url, json=payload, headers=headers, timeout=15).json()
                msg = response['choices'][0]['message']['content']
                st.markdown(msg)
                st.session_state.messages.append({"role": "assistant", "content": msg})
            except:
                st.error("KI-Chat aktuell nicht erreichbar.")

# 4. DIE VOLLE ERGEBNIS-ANALYSE (Statische Sektion)
st.divider()
if st.button("🚀 VOLLSTÄNDIGE ANALYSE STARTEN", use_container_width=True):
    st.subheader("📍 Standort-Check & Trends")
    st.map(pd.DataFrame({'lat': [36.721, 36.659, 37.019], 'lon': [-4.421, -4.756, -4.559]}))
    
    st.subheader("📈 Wertzuwachs (Prognose)")
    st.bar_chart(pd.DataFrame({"Region": ["Umland", "Stadt", "Küste"], "Trend %": [22, 15, 12]}).set_index("Region"))

    st.subheader("🌐 Markt-Recherche")
    st.link_button("📸 Foto-Marktcheck auf Google", 
                   f"https://www.google.com/search?q={objekt.replace(' ', '+')}+Málaga+kaufen+site:idealista.com")

st.divider()
st.caption("✅ System: Chat aktiv | 7% ITP | Foto-Check | KI | Karte | Trends")
