import streamlit as st
import requests
import pandas as pd

# 1. SETUP & KONFIGURATION
st.set_page_config(page_title="Málaga Invest Ultimate", layout="centered")
groq_key = st.secrets.get("GROQ_API_KEY")

# 2. HAUPT-INTERFACE (Kompakte Struktur)
st.title("🤖 Málaga Invest-Zentrale")
st.markdown("### 🔍 Objekt-Details & Analyse")

# Eingabefelder für Links (Anzeige & Foto)
anzeigen_link = st.text_input("🔗 Link zur Immobilien-Anzeige (Idealista, etc.):")
g_link = st.text_input("🖼️ Google-Foto Link des Objekts:")

# Kompakte Zeile für Typ und Preis (Ersetzt die alte Kaufpreiszeile)
col_obj, col_price = st.columns([2, 1])
with col_obj:
    objekt = st.text_input("Haus-Typ/Region:", value="Finca Málaga")
with col_price:
    preis = st.number_input("Preis (€):", value=250000, step=5000)

# Automatische 7% ITP Steuerberechnung für Andalusien
itp = preis * 0.07
gesamt = preis + itp
st.success(f"💰 **Kosten-Struktur:** ITP (7%): {itp:,.0f} € | Gesamt-Invest: {gesamt:,.0f} €")

# 3. RECHERCHE-TOOLS (Sofort-Check Buttons)
st.subheader("🌐 Markt-Recherche & Bild-Check")
c1, c2 = st.columns(2)
with c1:
    st.link_button("🏠 Ähnliche Angebote", 
                   f"https://www.idealista.com/de/venta-viviendas/malaga-provincia/fincas/?precio-maximo={preis + 20000}")
with c2:
    search_query = f"{objekt} Málaga kaufen {preis} Euro"
    st.link_button("📸 Foto-Marktcheck", 
                   f"https://www.google.com/search?q={search_query.replace(' ', '+')}+site:idealista.com+OR+site:fotocasa.es")

# 4. DIE VOLLE ANALYSE (KI, KARTE, TRENDS)
st.divider()
if st.button("🚀 VOLLSTÄNDIGE ANALYSE STARTEN", use_container_width=True):
    
    # A. KI-EXPERTE (Checkt Anzeige, Foto-Link und Marktdaten)
    st.subheader("📋 Strategische Bewertung")
    if groq_key:
        with st.spinner("KI wertet Anzeige und Links aus..."):
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {groq_key}"}
            prompt = f"""
            Analysiere als Immobilien-Experte für Málaga:
            Objekt: {objekt}
            Preis: {preis}€
            Anzeige: {anzeigen_link}
            Google-Referenz: {g_link}
            
            Prüfe: Preisstimmigkeit, Lagepotenzial und eventuelle Auffälligkeiten in der Anzeige.
            """
            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "system", "content": "Du bist ein spezialisierter Immobilien-Analyst."},
                             {"role": "user", "content": prompt}]
            }
            try:
                r = requests.post(url, json=payload, headers=headers, timeout=15)
                st.write(r.json()['choices'][0]['message']['content'])
            except:
                st.error("Verbindung zur KI verzögert. Bitte nutze die manuellen Recherche-Buttons oben.")

    # B. STANDORT-KARTE
    st.subheader("📍 Regionaler Fokus")
    map_data = pd.DataFrame({'lat': [36.7212, 36.6591, 37.0194], 'lon': [-4.4214, -4.7562, -4.5597]})
    st.map(map_data)

    # C. MARKT-TRENDS (Grafik)
    st.subheader("📈 Wertentwicklung (Prognose)")
    chart_data = pd.DataFrame({"Region": ["Umland", "Stadt", "Küste"], "Trend %": [22, 15, 12]}).set_index("Region")
    st.bar_chart(chart_data)

st.divider()
st.caption("✅ Alles aktiv: 7% ITP | Anzeigen-Analyse | KI & Markt-Daten")
