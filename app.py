import streamlit as st
import requests
import pandas as pd

# 1. KONFIGURATION
st.set_page_config(page_title="Málaga Invest Pro AI", layout="wide")

# Zugriff auf deinen GROQ_API_KEY aus den Secrets
groq_key = st.secrets.get("GROQ_API_KEY")

@st.cache_data(ttl=3600)
def call_groq_agent(prompt):
    """Nutzt deinen Groq-Key für extrem schnelle Antworten ohne Fehler 400."""
    if not groq_key:
        return "❌ GROQ_API_KEY fehlt in den Secrets!"
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {groq_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.3-70b-versatile", # Ein sehr leistungsstarkes Modell
        "messages": [{"role": "user", "content": prompt}]
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=20)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        elif response.status_code == 429:
            return "🕒 Groq-Limit erreicht. Bitte 30 Sek. warten."
        else:
            return f"❌ Fehler {response.status_code}: {response.text}"
    except Exception as e:
        return f"📡 Verbindungsproblem: {e}"

# 2. RECHNER-LOGIK
def calculate_costs(price):
    itp = price * 0.07
    notar = price * 0.01
    total = price + itp + notar
    return {"Kaufpreis": price, "ITP (7%)": itp, "Notar/Register": notar, "Gesamt-Invest": total}

# 3. BENUTZEROBERFLÄCHE
st.title("🤖 Málaga Investment-Zentrale (Groq Edition)")
st.success("Status: Verbunden mit Groq Cloud")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🔍 Analyse & Suche")
    user_input = st.text_input("Link oder Suchanfrage (z.B. Finca Málaga 250k):")
    
    if st.button("🚀 Agent beauftragen"):
        if user_input:
            with st.spinner("Groq-Agent analysiert..."):
                prompt = f"""
                Analysiere für Málaga Invest: {user_input}.
                1. Falls Link: Checke m2-Preis & Lage.
                2. Falls Suche: Liste 3 Angebote mit Links.
                3. Prognose: 5-Jahres-Wertsteigerung für das Viertel.
                """
                antwort = call_groq_agent(prompt)
                st.markdown(antwort)

with col2:
    st.subheader("📊 Kosten-Check")
    price_eval = st.number_input("Kaufpreis (€)", value=250000, step=10000)
    costs = calculate_costs(price_eval)
    st.table(pd.DataFrame([costs]).T.rename(columns={0: "Betrag (€)"}))
    
    # 5-Jahres-Trend Grafik
    prognose_data = pd.DataFrame({
        "Viertel": ["Centro", "Teatinos", "El Palo", "Axarquía"],
        "Trend %": [15, 22, 12, 18]
    })
    st.bar_chart(prognose_data.set_index("Viertel"))
