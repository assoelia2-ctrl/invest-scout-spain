import streamlit as st
import requests
import pandas as pd
import pydeck as pdk

# 1. SETUP
st.set_page_config(page_title="Málaga Invest Pro", layout="wide")
api_key = st.secrets.get("GEMINI_API_KEY")

def call_ki_final(prompt):
    # Wir nutzen die ABSOLUTE Standard-Route v1 (nicht v1beta)
    # Und wir hängen den Key als Header an, nicht als URL-Parameter
    url = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent"
    headers = {
        'Content-Type': 'application/json',
        'x-goog-api-key': api_key  # Key im Header ist sicherer
    }
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            # Hier geben wir die genaue Google-Fehlermeldung aus
            error_details = response.json().get('error', {}).get('message', 'Unbekannter Fehler')
            return f"Google sagt: {error_details} (Code: {response.status_code})"
    except Exception as e:
        return f"Verbindung fehlgeschlagen: {e}"

# UI
st.title("🤖 Málaga Invest-Scout")
tab1, tab2, tab3 = st.tabs(["🔍 Analyse", "⚖️ Portfolio", "📍 Karte"])

with tab1:
    query = st.text_input("Deine Suchanfrage:", value="Finca in Málaga")
    if st.button("🚀 Markt-Analyse starten"):
        if not api_key:
            st.error("Kein Key in den Secrets gefunden!")
        else:
            with st.spinner("Frage Google-Server an..."):
                antwort = call_ki_final(f"Kurze Immobilien-Analyse für: {query} in Málaga.")
                st.info(antwort)

with tab2:
    st.write("Hier landen deine Ergebnisse, sobald die KI antwortet.")

with tab3:
    st.pydeck_chart(pdk.Deck(
        initial_view_state=pdk.ViewState(latitude=36.72, longitude=-4.42, zoom=10),
        layers=[pdk.Layer('ScatterplotLayer', data=pd.DataFrame({'lat':[36.72], 'lon':[-4.42]}), get_position='[lon, lat]', get_radius=1000, get_color='[200, 30, 0]')]
    ))
