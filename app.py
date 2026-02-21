import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np

# 1. Konfiguration
st.set_page_config(page_title="Invest-Scout Spain 2026", layout="wide")

# 2. Daten laden (KI-Agent Basisdaten)
@st.cache_data
def load_agent_data():
    data = {
        'city': ['Malaga', 'Marbella', 'Alicante', 'Palma', 'Madrid', 'Barcelona', 'Valencia'],
        'lat': [36.72, 36.51, 38.34, 39.57, 40.41, 41.38, 39.46],
        'lon': [-4.42, -4.88, -0.48, 2.65, -3.70, 2.17, -0.37],
        'price_m2': [2800, 4500, 1900, 3800, 4200, 4800, 2100],
        'yield': [5.4, 4.2, 6.1, 4.5, 3.8, 3.6, 5.9]
    }
    return pd.DataFrame(data)

df = load_agent_data()

# 3. Header
st.title("🏠 Invest-Scout Spain")
st.write("Dein KI-Agent für den spanischen Immobilienmarkt.")
st.divider()

# 4. Suche (Direkt auf der Hauptseite)
with st.container():
    st.subheader("🔍 Marktanalyse starten")
    col_in1, col_in2 = st.columns(2)
    
    with col_in1:
        stadt_wahl = st.selectbox("Wähle eine Stadt", df['city'].unique())
        budget = st.number_input("Dein Budget (€)", value=300000, step=10000)
    
    with col_in2:
        objekttyp = st.multiselect("Objekttyp", ["Wohnung", "Haus", "Finca"], default="Wohnung")
        search_btn = st.button("🚀 Jetzt analysieren", use_container_width=True)

# 5. Ergebnisse (Erscheinen auf derselben Seite)
if search_btn:
    st.divider()
    selected = df[df['city'] == stadt_wahl].iloc[0]
    
    # Metriken
    m1, m2, m3 = st.columns(3)
    m1.metric("Ø Preis / m²", f"{selected['price_m2']} €")
    m2.metric("Rendite-Chance", f"{selected['yield']} %")
    m3.metric("Status", "Top Investment")

    # Karte
    st.subheader(f"📍 Standort-Check: {stadt_wahl}")
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=selected['lat'], longitude=selected['lon'], zoom=10, pitch=45
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=df,
                get_position='[lon, lat]',
                get_color='[255, 75, 75, 150]',
                get_radius=1000,
            ),
        ],
    ))

    # Links & Rechner
    st.divider()
    c_link, c_calc = st.columns(2)
    
    with c_link:
        st.subheader("🔗 Portale")
        url = f"https://www.idealista.com/de/buscar/venta-viviendas/{stadt_wahl.lower()}/"
        st.markdown(f"**[👉 Passende Objekte auf Idealista anzeigen]({url})**")
        st.info("Klicke auf den Link, um direkt zu den Live-Angeboten zu springen.")

    with c_calc:
        st.subheader("📊 Schneller Rendite-Check")
        miete = st.slider("Geschätzte Miete/Monat", 500, 4000, 1200)
        roi = (miete * 12 / budget) * 100
        st.write(f"Voraussichtlicher ROI: **{roi:.2f}% p.a.**")

else:
    st.info("Gib deine Daten oben ein und klicke auf 'Jetzt analysieren', um die Karte und die Details zu sehen.")
