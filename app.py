import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
import pydeck as pdk

# 1. Grundkonfiguration
st.set_page_config(page_title="Invest-Scout Pro 2026", layout="wide")

# 2. KI-Setup mit Modell-Automatik
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    # Wir suchen automatisch nach dem verfügbaren Modell
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    # Bevorzugt 1.5-flash, sonst das erste verfügbare
    model_name = next((m for m in available_models if 'gemini-1.5-flash' in m), available_models[0])
    model = genai.GenerativeModel(model_name)
    
    st.sidebar.success(f"🤖 Aktiv: {model_name}")
except Exception as e:
    st.error(f"Kritischer Fehler beim Start: {e}")
    st.stop()

# 3. Agenten-Logik
def run_agent(query, image=None):
    try:
        prompt = f"Du bist ein Immobilien-Experte für Spanien. Analysiere: {query}"
        content = [prompt]
        if image:
            content.append(image)
        
        response = model.generate_content(content)
        return response.text
    except Exception as e:
        return f"Unerwarteter Fehler: {e}"

# 4. Dashboard (Wie in deinem Interface-Vorbild)
st.title("🤖 Invest-Scout: Full Access")
st.markdown("---")

c1, c2 = st.columns([1, 1])

with c1:
    st.subheader("Befehl an den Agenten")
    user_query = st.text_area("Was soll ich tun?", placeholder="Suche Neubauten in Valencia...", height=150)
    file = st.file_uploader("Bild hochladen", type=["jpg", "png", "jpeg"])
    
    if st.button("🚀 Agenten beauftragen", use_container_width=True):
        if user_query:
            with st.spinner("Agent analysiert..."):
                img = Image.open(file) if file else None
                st.session_state.result = run_agent(user_query, img)
        else:
            st.warning("Bitte gib eine Anfrage ein.")

with c2:
    st.subheader("📍 Standort-Check")
    # Fokus auf Andalusien/Malaga wie in deinem Screenshot
    df = pd.DataFrame({'lat': [36.72], 'lon': [-4.42]})
    st.pydeck_chart(pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(latitude=36.72, longitude=-4.42, zoom=8, pitch=45),
        layers=[pdk.Layer('ScatterplotLayer', data=df, get_position='[lon, lat]', get_color='[197, 255, 0]', get_radius=5000)]
    ))

# Ergebnisanzeige
if 'result' in st.session_state:
    st.divider()
    st.markdown("### 📩 Agenten-Bericht")
    st.info(st.session_state.result)
