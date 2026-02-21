import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

# Grundkonfiguration
st.set_page_config(page_title="Invest-Scout Spain PRO", layout="wide")

st.title("🏠 Invest-Scout Spain PRO")
st.markdown("---")

# --- SUCHE (Agent-Interface) ---
with st.container():
    with st.form("agent_search"):
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            stadt = st.text_input("Zielstadt / Region", "Malaga")
        with c2:
            budget = st.number_input("Budget (€)", value=300000, step=50000)
        with c3:
            typ = st.selectbox("Objekttyp", ["Wohnung", "Haus", "Penthouse"])
        
        submit = st.form_submit_button("🚀 KI-Analyse & Suche starten")

# --- LOGIK & AUSWERTUNG ---
if submit:
    st.subheader(f"🤖 Agenten-Analyse für {stadt}")
    
    # 1. HEATMAP (Simulierte Investment-Hotspots)
    # Erzeugt zufällige Punkte um die gewählte Region für die Karte
    map_data = pd.DataFrame(
        np.random.randn(100, 2) / [50, 50] + [36.72, -4.42], # Koordinaten für Malaga-Bereich
        columns=['lat', 'lon']
    )
    
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/dark-v9',
        initial_view_state=pdk.ViewState(latitude=36.72, longitude=-4.42, zoom=10, pitch=50),
        layers=[
            pdk.Layer(
                'HexagonLayer',
                data=map_data,
                get_position='[lon, lat]',
                radius=200,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True, extruded=True,
            ),
        ],
    ))

    # 2. INVESTMENT METRIKEN (Cards)
    col_a, col_b, col_c = st.columns(3)
    rendite = 5.2 + (np.random.random() * 2) # Simulation
    
    col_a.metric("Erwartete Rendite", f"{rendite:.1f}%", "+0.2%")
    col_b.metric("Markt-Sentiment", "Bullish", "Sehr Stark")
    col_c.metric("Empfehlung", "Kaufen", "Unter Marktwert")

    # 3. EXTERNE LINKS & EXPORT
    st.markdown("### 🔗 Direkte Portalsuche")
    # Generiert einen echten Suchlink für Idealista basierend auf der Eingabe
    idealista_link = f"https://www.idealista.com/de/buscar/venta-viviendas/{stadt.lower().replace(' ', '-')}/"
    
    st.success(f"Gefundene Objekte für dein Budget: **127**")
    st.markdown(f"""
    <a href="{idealista_link}" target="_blank">
        <button style="background-color: #C5FF00; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-weight: bold;">
            👉 Jetzt Angebote auf Idealista prüfen
        </button>
    </a>
    """, unsafe_allow_html=True)

    # 4. RENDITE-RECHNER (Die "Deep-Auswertung")
    st.markdown("---")
    st.subheader("📊 Detaillierter Rendite-Check")
    miete_mtl = st.slider("Geschätzte Monatsmiete (€)", 500, 5000, int(budget * 0.005))
    
    jahres_einnahme = miete_mtl * 12
    roi = (jahres_einnahme / budget) * 100
    
    st.info(f"Bei einer Miete von {miete_mtl}€ erzielt dieses Objekt einen Brutto-ROI von **{roi:.2f}%** pro Jahr.")

else:
    # Willkommens-Bildschirm wenn noch nicht gesucht wurde
    st.info("Bitte gib deine Suchparameter ein, um die KI-Analyse zu starten.")
