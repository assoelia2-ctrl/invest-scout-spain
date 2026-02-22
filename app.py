import streamlit as st
import requests
import pandas as pd
import pydeck as pdk

# 1. SETUP
st.set_page_config(page_title="Málaga Invest Pro", layout="wide")
api_key = st.secrets.get("GROQ_API_KEY")

def call_groq(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"Fehler: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Verbindung fehlgeschlagen: {e}"

# 2. UI STRUKTUR
st.title("🚀 Málaga Invest-Scout (Groq Edition)")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["🔍 KI-Analyse", "📊 Portfolio", "🗺️ Karte"])

with tab1:
    query = st.text_input("Was suchst du in Málaga?", value="Finca bis 250.000€")
    if st.button("Analyse starten", use_container_width=True):
        if not api_key:
            st.error("API Key fehlt in den Secrets!")
        else:
            with st.spinner("KI berechnet Marktchancen..."):
                antwort = call_groq(f"Analysiere kurz: {query} in Málaga. Lohnt sich das als Investment?")
                st.info("### Analyse-Ergebnis:")
                st.write(antwort)
                st.divider()
                st.link_button("🏠 Direkt zu Idealista", "https://www.idealista.com")

with tab2:
    st.subheader("⚖️ Dein Investment-Portfolio")
    st.write("Hier werden deine zukünftigen Suchen gespeichert.")

with tab3:
    st.subheader("🗺️ Immobilien-Hotspots")
    # Ansicht auf Málaga zentriert
    view = pdk.ViewState(latitude=36.72, longitude=-4.42, zoom=11)
    st.pydeck_chart(pdk.Deck(
        initial_view_state=view,
        layers=[pdk.Layer('ScatterplotLayer', 
                          data=pd.DataFrame({'lat':[36.72], 'lon':[-4.42]}), 
                          get_position='[lon, lat]', 
                          get_radius=1000, 
                          get_color='[255, 75, 75]')]
    ))
