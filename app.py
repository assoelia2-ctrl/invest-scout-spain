    import streamlit as st
import requests
import pandas as pd

# 1. SETUP
st.set_page_config(page_title="Andalusien Invest Pro", layout="centered")
groq_key = st.secrets.get("GROQ_API_KEY")

# 2. DEIN SCORING-SYSTEM (Integriert)
def analyze_risk(description):
    risk_keywords = {"suelo rústico": 5, "no urbanizable": 5, "sin licencia": 6, "ocupada": 10}
    score = 0
    found_flags = []
    for k, v in risk_keywords.items():
        if k in description.lower():
            score += v
            found_flags.append(k)
    return score, found_flags

# 3. INTERFACE (Kompakt & Stabil)
st.title("🤖 Málaga Invest-Zentrale")

# Eingaben
anzeigen_link = st.text_input("🔗 Link zur Anzeige (Idealista/Fotocasa):")
c_typ, c_preis = st.columns([2, 1])
with c_typ:
    objekt = st.text_input("Haus-Typ/Region:", value="Finca Málaga")
with c_preis:
    preis = st.number_input("Preis (€):", value=250000)

# Kosten & Risiko-Vorschau
itp = preis * 0.07
st.success(f"💰 ITP (7%): {itp:,.0f}€ | Gesamt: {preis + itp:,.0f}€")

# 4. CHAT-FELD FÜR AUFGABEN
st.subheader("💬 Chat mit deinem Experten")
if "messages" not in st.session_state: st.session_state.messages = []
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if prompt := st.chat_input("z.B. 'Prüfe das Risiko' oder 'Suche Alternativen'"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Hier nutzt die KI dein Scoring-Wissen für die Antwort
    with st.chat_message("assistant"):
        st.write(f"Analysiere Risiko für {objekt}... (Nutze Scoring-Modell)")
        # KI Call hier einfügen...

# 5. DIE ANALYSE (Buttons für Scans)
st.divider()
if st.button("🚀 VOLLSTÄNDIGER MARKT-SCAN"):
    st.info("Starte Playwright-Scraper & Google Distance Matrix...")
    # Deine Funktionen hier aufrufen
    st.map(pd.DataFrame({'lat': [36.72], 'lon': [-4.42]}))
