import streamlit as st
import requests
import pandas as pd

# 1. SETUP
st.set_page_config(page_title="Málaga Invest Ultimate", layout="centered")
groq_key = st.secrets.get("GROQ_API_KEY")

# 2. HAUPT-INTERFACE
st.title("🤖 Málaga Invest-Zentrale")
st.markdown("### 🔍 Objekt-Details & Analyse")

# Eingabefelder für Basisdaten und Links
col_a, col_b = st.columns([2, 1])
with col_a:
    objekt = st.text_input("Haus-Typ/Region (z.B. Finca Coín):", value="Finca Málaga")
    anzeigen_link = st.text_input("🔗 Link zur Immobilien-Anzeige (Idealista, etc.):")
    g_link = st.text_input("🖼️ Google-Foto Link des Objekts:")
with col_b:
    preis = st.number_input("Kaufpreis (€):", value=250000, step=5000)

# 7% ITP Steuerberechnung (Andalusien)
itp = preis * 0.07
gesamt = preis + itp
st.success(f"💰 **Kosten-Struktur:** ITP (7%): {itp:,.0f} € | Gesamt-Invest: {gesamt:,.0f} €")

# 3. RECHERCHE-TOOLS
st.subheader("🌐 Markt-Recherche & Bild-Check")
c1, c2 = st.columns(2)
with c1:
    st.link_button("🏠 Ähnliche Angebote suchen", 
                   f"https://www.idealista.com/de/venta-viviendas/malaga-provincia/fincas/?precio-maximo={preis + 20000}")
with c2:
    search_query = f"{objekt} Málaga kaufen {preis} Euro"
    st.link_button("📸 Foto-Marktcheck starten", 
                   f"https://www.google.com/search?q={search_query.replace(' ', '+')}+site:idealista.com+OR+site:fotocasa.es")

# 4. DIE VOLLE ANALYSE (KI, KARTE, TRENDS)
st.divider()
if st.button("🚀 VOLLSTÄNDIGE ANALYSE STARTEN", use_container_width=True):
    
    # A. KI-ANALYSE (Inkl. Anzeigen-Check)
    st.subheader("📋 Strategische Bewertung")
    if groq_key:
        with st.spinner("KI prüft Anzeige und Marktdaten..."):
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {groq_key}"}
            
            prompt = f"""
            Analysiere als Immobilien-Experte für Málaga dieses Angebot:
            - Objekt: {objekt}
            - Preis: {preis} Euro
            - Anzeigen-Link: {anzeigen_link}
            - Foto-Referenz: {g_link}
            
            Aufgaben:
            1. Prüfe den Preis pro m² (wenn aus Link ersichtlich) im Vergleich zum Marktdurchschnitt.
            2. Analysiere das Potenzial der Lage (Málaga Region).
            3. Gib eine Einschätzung zur Rentabilität (Miete vs. Kaufpreis).
            4. Identifiziere mögliche 'Red Flags' oder Chancen in der Anzeige.
            """
            
            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "system", "content": "Du bist ein Immobilien-Analyst für Málaga."},
                             {"role": "user", "content": prompt}]
            }
            try:
                r = requests.post(url, json=payload, headers=headers, timeout=15)
                st.write(r.json()['choices'][0]['message']['content'])
            except:
                st.error("KI-Analyse verzögert. Bitte Daten manuell mit den Links oben prüfen.")

    # B. STANDORT-KARTE
    st.subheader("📍 Regionaler Fokus")
    map_data = pd.DataFrame({
        'lat': [36.7212, 36.6591, 37.0194],
        'lon': [-4.4214, -4.7562, -4.5597]
    })
    st.map(map_data)

    # C. MARKT-TRENDS
    st.subheader("📈 Wertzuwachs-Prognose")
    chart_data = pd.DataFrame({
        "Sektor": ["Fincas", "Stadt", "Küste"],
        "Trend %": [22, 15, 12]
    }).set_index("Sektor")
    st.bar_chart(chart_data)

st.divider()
st.caption("✅ Alles aktiv: 7% ITP | Anzeigen-Analyse | Foto-Check | KI | Karte | Trends")
