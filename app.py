        import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np

# Konfiguration
st.set_page_config(page_title="Invest-Scout Spain PRO", layout="wide")

# Daten laden
@st.cache_data
def load_data():
    # Lädt die CSV-Datei. Falls nicht vorhanden, werden Demo-Daten erzeugt.
    try:
        df = pd.read_csv("preise_spanien.csv")
    except:
        data = {
            'city': ['Malaga', 'Marbella', 'Alicante', 'Palma', 'Madrid'],
            'lat': [36.72, 36.51, 38.34, 39.57, 40.41],
            'lon': [-4.42, -4.88, -0.48, 2.65, -3.70],
            'price_m2': [2800, 4500, 1900, 3800, 4200],
            'yield': [5.4, 4.2, 6.1, 4.5, 3.8]
        }
        df = pd.DataFrame(data)
    return df

df_spain = load_data()

st.title("🏠 Invest-Scout Spain PRO")
st.caption("KI-Agent für Immobilien-Investments")

# --- SUCHE ---
with st.sidebar:
    st.header("🔍 Such-Parameter")
    stadt_wahl = st.selectbox("Wähle eine Fokus-Region", df_spain['city'].unique())
    budget = st.number_input("Budget (€)", value=300000, step=10000)
    st.divider()
    st.write("Der KI-Agent scannt den Markt basierend auf Echtzeit-Durchschnittswerten.")

# --- HAUPTBEREICH ---
col_map, col_info = st.columns([2, 1])

with col_map:
    st.subheader("📍 Investment-Hotspots (Preisniveau)")
    # Karte mit Pydeck
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=36.72, longitude=-4.42, zoom=5, pitch=45
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=df_spain,
                get_position='[lon, lat]',
                get_color='[200, 30, 0, 160]',
                get_radius='price_m2 / 10', # Größere Kreise bei höheren Preisen
                pickable=True,
            ),
        ],
    ))

with col_info:
    selected_data = df_spain[df_spain['city'] == stadt_wahl].iloc[0]
    st.subheader(f"Analyse: {stadt_wahl}")
    st.metric("Ø Preis / m²", f"{selected_data['price_m2']} €")
    st.metric("Durchschnitts-Rendite", f"{selected_data['yield']} %")
    
    # Berechneter Link
    link = f"https://www.idealista.com/de/buscar/venta-viviendas/{stadt_wahl.lower()}/"
    st.markdown(f"[👉 Aktuelle Angebote in {stadt_wahl}]({link})")

# --- RENDITE-RECHNER ---
st.divider()
st.subheader("📊 Interaktiver Rendite-Rechner")
c1, c2, c3 = st.columns(3)

flaeche = c1.number_input("Wohnfläche (m²)", value=80)
kaufpreis = selected_data['price_m2'] * flaeche
c2.info(f"Geschätzter Kaufpreis: **{kaufpreis:,.0f} €**")

miete_est = (kaufpreis * (selected_data['yield']/100)) / 12
c3.success(f"Empfohlene Kaltmiete: **{miete_est:,.0f} € / Monat**")

st.warning("Hinweis: Dies ist eine KI-basierte Schätzung. Kaufnebenkosten in Spanien (ca. 10-12%) sind hier noch nicht eingerechnet.")    
