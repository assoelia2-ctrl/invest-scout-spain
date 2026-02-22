import streamlit as st
import requests
import pandas as pd

# 1. SETUP
st.set_page_config(page_title="Málaga Invest", layout="centered")
groq_key = st.secrets.get("GROQ_API_KEY")

# 2. KOSTEN-LOGIK (SOFORT-CHECK)
st.title("🤖 Málaga Invest-Zentrale")
objekt = st.text_input("Haus-Typ/Ort:", value="Finca Málaga")
preis = st.number_input("Kaufpreis (€):", value=250000, step=5000)

# Fixkosten sofort anzeigen
itp = preis * 0.07 
st.metric("Grunderwerbsteuer (7% ITP)", f"{itp:,.0f} €")
st.metric("Gesamtinvestment", f"{preis + itp:,.0f} €")

# 3. INTERAKTIVE ELEMENTE
c1, c2 = st.columns(2)
with c1:
    st.link_button("🏠 Idealista Suche", f"https://www.idealista.com/de/venta-viviendas/malaga-provincia/?precio-maximo={preis}")
with c2:
    st.link_button("🏠 Fotocasa Suche", f"https://www.fotocasa.es/es/comprar/viviendas/malaga-provincia/l?maxPrice={preis}")

# 4. KI-ANALYSE & KARTE
if st.button("🚀 EXPERTEN-CHECK STARTEN", use_container_width=True):
    st.divider()
    
    # KI-Bericht
    if groq_key:
        with st.spinner("Hole Marktdaten..."):
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {groq_key}"}
            payload = {"model": "llama-3.3-70b-versatile", "messages": [
                {"role": "system", "content": "Gib kurze Immobilien-Fakten zu Málaga."},
                {"role": "user", "content": f"Check: {objekt} für {preis}€."}]}
            try:
                r = requests.post(url, json=payload, headers=headers, timeout=10)
                st.write(r.json()['choices'][0]['message']['content'])
            except:
                st.error("Verbindung zu schwach. Bitte erneut versuchen.")
    
    # Karte & Trends
    st.subheader("📍 Standort & Prognose")
    df = pd.DataFrame({'lat': [36.72, 36.65], 'lon': [-4.42, -4.78]})
    st.map(df)
    st.bar_chart(pd.DataFrame({"Viertel": ["Umland", "Stadt"], "Wachstum": [18, 14]}).set_index("Viertel"))
