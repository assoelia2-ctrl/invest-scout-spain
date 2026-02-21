import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
import pydeck as pdk

# 1. Initiale Konfiguration
st.set_page_config(page_title="Invest-Scout Pro: Málaga", layout="wide", page_icon="🏠")

# API Setup (Automatische Modellwahl)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    model_name = next((m for m in available_models if 'gemini-1.5-flash' in m), available_models[0])
    model = genai.GenerativeModel(model_name)
except Exception as e:
    st.error(f"KI-Verbindungsproblem: {e}")
    st.stop()

# 2. Agenten-Logik für Besichtigungen
def run_inspection_ai(query, image=None):
    instruction = """
    Du bist ein Bau-Sachverständiger und Immobilien-Agent in Spanien. 
    Wenn der User ein Bild hochlädt, analysiere es auf Mängel (Risse, Feuchtigkeit, Elektro).
    Wenn der User Fragen stellt, erstelle eine spezifische Checkliste für Fincas in Málaga (AFO, Wasserrechte, Zufahrt).
    Antworte kurz, präzise und fachlich fundiert.
    """
    inputs = [instruction + "\n\nAnfrage: " + query]
    if image:
        inputs.append(image)
    response = model.generate_content(inputs)
    return response.text

# 3. Benutzeroberfläche
st.title("🤖 Dein KI-Agent: Besichtigungs-Modus")
st.markdown("---")

# Navigation über Tabs
tab_suche, tab_besichtigung = st.tabs(["🔍 Markt-Analyse", "📋 Besichtigungs-Check"])

with tab_suche:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Neuer Suchauftrag")
        user_query = st.text_area("Was suchst du?", placeholder="Suche Finca in der Axarquía bis 250k...", key="main_search")
        if st.button("🚀 Markt scannen", use_container_width=True):
            with st.spinner("Agent analysiert..."):
                st.session_state.last_result = run_inspection_ai(user_query)
    
    with col2:
        st.subheader("📍 Fokus-Region")
        # Karte zentriert auf Málaga
        df = pd.DataFrame({'lat': [36.72], 'lon': [-4.42]})
        st.pydeck_chart(pdk.Deck(
            map_style=None,
            initial_view_state=pdk.ViewState(latitude=36.72, longitude=-4.42, zoom=9, pitch=45),
            layers=[pdk.Layer('ScatterplotLayer', data=df, get_position='[lon, lat]', get_color='[197, 255, 0]', get_radius=5000)]
        ))
    
    if 'last_result' in st.session_state:
        st.info(st.session_state.last_result)

with tab_besichtigung:
    st.subheader("📸 Live-Check vor Ort")
    st.write("Lade ein Foto von der Besichtigung hoch (z.B. Fassade, Dach, Dokumente), um eine Sofort-Einschätzung zu erhalten.")
    
    inspect_file = st.file_uploader("Foto zur Mängel-Analyse", type=["jpg", "png", "jpeg"], key="inspect_upload")
    inspect_query = st.text_input("Spezielle Frage zum Objekt?", "Worauf muss ich hier besonders achten?")

    if st.button("🧐 Objekt prüfen", use_container_width=True):
        with st.spinner("KI-Gutachter analysiert..."):
            img = Image.open(inspect_file) if inspect_file else None
            st.session_state.inspect_result = run_inspection_ai(inspect_query, img)

    if 'inspect_result' in st.session_state:
        st.success("### 🛠️ Agenten-Gutachten")
        st.markdown(st.session_state.inspect_result)
        
        # Interaktive Checkliste (Standard-Punkte)
        st.markdown("---")
        st.subheader("✅ Deine Sofort-Checkliste")
        st.checkbox("Legalität: Liegt ein AFO-Zertifikat vor?")
        st.checkbox("Wasser: Sind die Wasserrechte im 'Registro de Aguas' eingetragen?")
        st.checkbox("Zufahrt: Ist der Weg öffentlich oder privat (Servidumbre de paso)?")
        st.checkbox("Bausubstanz: Anzeichen von aufsteigender Feuchtigkeit (Salpeter)?")
