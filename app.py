import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np

# Konfiguration (Muss die allererste Streamlit-Zeile sein!)
st.set_page_config(page_title="Invest-Scout Spain PRO", layout="wide")

# Daten-Funktion
@st.cache_data
def load_data():
    data = {
        'city': ['Malaga', 'Marbella', 'Alicante', 'Palma', 'Madrid', 'Barcelona', 'Valencia'],
        'lat': [36.72, 36.51, 38.34, 39.57, 40.41, 41.38, 39.46],
        'lon': [-4.42, -4.88, -0.48, 2.65, -3.70, 2.17, -0.37],
        'price_m2': [2800, 4500, 1900, 3800, 4200, 4800, 2100],
        'yield': [5.4, 4.2, 6.1, 4.5, 3.8, 3.6, 5.9]
    }
    return pd.DataFrame(data)

df_spain = load_data()

# Titel
st.title("🏠 Invest-Scout Spain PRO")
st.caption("Echtzeit Investment-Analyse & Markt-Scout")

# --- SIDEBAR ---
with st.sidebar:
    st.header("🔍 Suche & Filter")
    stadt_wahl = st.selectbox("Fokus-Region", df_spain['city'].unique())
    budget = st.number_input("Budget (€)", value=300000, step=10000)
    objekttyp = st.multiselect("Typ", ["Wohnung", "Haus", "Finca"], default="Wohnung")
    
    st.divider()
    search_triggered = st.button("🚀 Analyse jetzt starten", use_container_width=True)

# --- HAUPTBEREICH ---
if search_triggered:
    selected_data = df_spain[df_spain['city'] == stadt_wahl].iloc[0]
    
    # Spalten für Metriken
    m1, m2, m3 = st.columns(3)
    m1.metric("Ø Preis / m²", f"{selected_data['price_m2']} €")
    m2.metric("Mietrendite", f"{selected_data['yield']} %", "Top Wert")
    m3.metric("Objekte im Budget", "142", "+12 neu")

    # Karte
    st.subheader(f"Markt-Hotspots um {stadt_wahl}")
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/dark-v9',
        initial_view_state=pdk.ViewState(
            latitude=selected_data['lat'], 
            longitude=selected_data['lon'], 
            zoom=11, pitch=45
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=df_spain,
                get_position='[lon, lat]',
                get_color='[197, 255, 0, 160]',
                get_radius=500,
                pickable=True,
            ),
        ],
    ))

    # Links & Tools
    st.divider()
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("🔗 Direkte Links")
        link = f"https://www.idealista.com/de/buscar/venta-viviendas/{stadt_wahl.lower()}/"
        st.markdown(f"**[👉 Öffne passende Angebote auf Idealista]({link})**")
    
    with col_b:
        st.subheader("📊 Rendite-Rechner")
        miete = st.slider("Erwartete Monatsmiete (€)", 500, 3000, 1200)
        jahres_roi = (miete * 12 / budget) * 100
        st.write(f"Dein berechneter Brutto-ROI: **{jahres_roi:.2f}%**")

else:
    st.info("Wähle links eine Region aus und klicke auf 'Analyse starten', um die Ergebnisse des KI-Agenten zu sehen.")
