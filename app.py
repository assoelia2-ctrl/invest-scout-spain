import streamlit as st
import requests
import pandas as pd

# 1. SETUP
st.set_page_config(page_title="Málaga Invest Pro", layout="centered")
groq_key = st.secrets.get("GROQ_API_KEY")

# 2. HAUPTSEITE & KOSTEN (7% ITP)
st.title("🤖 Málaga Invest-Zentrale")
objekt = st.text_input("Haus-Typ/Ort:", value="Finca Málaga")
preis = st.number_input("Kaufpreis (€):", value=250000, step=5000)

itp = preis * 0.07 
st.metric("Grunderwerbsteuer (7% ITP)", f"{itp:,.0f} €")
st.metric("Gesamtinvestment", f"{preis + itp:,.0f} €")

# 3. DIREKT-LINKS
c1, c2 = st.columns(2)
with c1:
    st.link_button("🏠 Idealista Suche", f"https://www.idealista.com/de/venta-viviendas/malaga-provincia/?precio-maximo={preis}")
with c2:
    st.link_button("🏠 Fotocasa Suche", f"https://www.fotocasa.es/es/comprar/viviendas/malaga-provincia/l?maxPrice={preis}")

# 4. DIE FEHLENDEN ERGEBNISSE (KI, KARTE, TRENDS)
if st.button("🚀 EXPERTEN-CHECK STARTEN", use_container_width=True):
    st.divider()
    
    # TEIL 1: KI-ANALYSE (Fakten-Bericht)
    st.subheader("📋 Strategische Bewertung")
    if groq_key:
        with st.spinner("Hole Marktdaten..."):
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {groq_key}"}
            payload = {"model": "llama-3.3-70b-versatile", "messages": [
                {"role": "system", "content": "Analysiere Immobilien in Málaga basierend auf Fakten."},
                {"role": "user", "content": f"Check: {objekt} für {preis} Euro."}]}
            try:
                r = requests.post(url, json=payload, headers=headers, timeout=10)
                st.write(r.json()['choices'][0]['message']['content'])
            except:
                st.error("KI-Dienst antwortet nicht. Bitte Button erneut drücken.")
    
    # TEIL 2: STANDORT-KARTE
    st.subheader("📍 Standort-Check")
    # Markiert wichtige Punkte in der Provinz Málaga
    map_data = pd.DataFrame({'lat': [36.721, 36.659, 36.890], 'lon': [-4.421, -4.780, -4.520]})
    st.map(map_data)
    
    # TEIL 3: MARKT-TRENDS (GRAFIK)
    st.subheader("📈 Wertentwicklung (Prognose)")
    chart_df = pd.DataFrame({
        "Region": ["Umland", "Küstennahe", "Stadt"],
        "Trend %": [18, 12, 14]
    }).set_index("Region")
    st.bar_chart(chart_df)

st.divider()
st.caption("Alle Systeme aktiv: ITP 7% | KI-Check | Karte | Trends")
