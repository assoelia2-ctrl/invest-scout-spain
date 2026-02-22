import streamlit as st
import requests
import pandas as pd

# 1. SETUP & KONFIGURATION
st.set_page_config(page_title="Málaga Invest Pro", layout="centered")
groq_key = st.secrets.get("GROQ_API_KEY")

# 2. SCHNELLE EINGABE-SCHICHT
st.title("🤖 Málaga Invest-Zentrale")
objekt = st.text_input("Haus-Typ oder Ort (z.B. Finca Málaga):", value="Finca Málaga")
preis = st.number_input("Kaufpreis (€):", value=250000, step=5000)
g_link = st.text_input("Google-Foto Link (Optional):")

# Sofortige Kostenberechnung (7% ITP Andalusien)
itp = preis * 0.07
gesamt = preis + itp
st.info(f"📊 **Fixkosten-Check:** Steuer (7% ITP): {itp:,.0f} € | Gesamt: {gesamt:,.0f} €")

# 3. DIREKT-RECHERCHE (EXTERNE LINKS)
st.subheader("🏠 Live-Angebote prüfen")
c1, c2 = st.columns(2)
with c1:
    st.link_button("👉 Idealista", f"https://www.idealista.com/de/venta-viviendas/malaga-provincia/?precio-maximo={preis}")
with c2:
    st.link_button("👉 Fotocasa", f"https://www.fotocasa.es/es/comprar/viviendas/malaga-provincia/l?maxPrice={preis}")

# 4. DIE "ALLES-DRIN" ERGEBNIS-SCHICHT
st.divider()
if st.button("🚀 VOLLE ANALYSE STARTEN", use_container_width=True):
    
    # A. KI-EXPERTE (REALE FAKTEN)
    st.subheader("📋 Strategische Bewertung")
    if groq_key:
        with st.spinner("KI analysiert Marktdaten..."):
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {groq_key}"}
            prompt = f"Investment-Check für {objekt} bei {preis}€. Link: {g_link}. Fokus: Málaga."
            payload = {"model": "llama-3.3-70b-versatile", "messages": [
                {"role": "system", "content": "Analysiere Immobilien-Fakten für Málaga."},
                {"role": "user", "content": prompt}]}
            try:
                r = requests.post(url, json=payload, headers=headers, timeout=12)
                st.write(r.json()['choices'][0]['message']['content'])
            except:
                st.error("KI-Dienst verzögert. Bitte nochmal drücken.")

    # B. STANDORT-KARTE (STABIL GELADEN)
    st.subheader("📍 Standort-Check")
    m_data = pd.DataFrame({'lat': [36.72, 36.65, 36.89], 'lon': [-4.42, -4.78, -4.52]})
    st.map(m_data)

    # C. MARKT-TRENDS (GRAFIK)
    st.subheader("📈 Wertentwicklung (Prognose)")
    t_data = pd.DataFrame({"Region": ["Umland", "Stadt", "Küste"], "Trend %": [18, 14, 12]}).set_index("Region")
    st.bar_chart(t_data)

st.divider()
st.caption("Fakten-Modus: 7% Steuer | KI-Analyse | Karte | Markttrends")
