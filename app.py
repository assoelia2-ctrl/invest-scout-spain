import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
import pydeck as pdk
import datetime
import re

# 1. Konfiguration & KI-Setup
st.set_page_config(page_title="Invest-Scout: Málaga Pro", layout="wide", page_icon="🏢")

try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    model_name = next((m for m in available_models if 'gemini-1.5-flash' in m), available_models[0])
    model = genai.GenerativeModel(model_name)
except Exception as e:
    st.error(f"KI-Verbindungsproblem: {e}")
    st.stop()

if 'visit_history' not in st.session_state:
    st.session_state.visit_history = []

# 2. Agenten-Logik mit Strategie & Link-Parameter-Berechnung
def run_expert_ai(query, image=None):
    instruction = """
    Du bist ein Immobilien-Analyst und Verhandlungsexperte für Málaga.
    1. ANALYSE: Prüfe das Objekt/Bild auf Mängel und Investitionspotenzial.
    2. STRATEGIE: Erstelle eine Argumentationsliste für Preisverhandlungen.
    3. SCORING: Gib am Ende IMMER exakt dieses Format aus:
    SCORE: [1-10]
    RENDITE: [%]
    RISIKO: [Niedrig/Mittel/Hoch]
    MAX-PREIS: [Euro-Wert]
    """
    content = [instruction, query]
    if image:
        content.append(image)
    
    response = model.generate_content(content)
    text = response.text
    
    # Daten-Extraktion für die Tabelle
    try:
        score = re.search(r"SCORE:\s*(\d+)", text).group(1)
        rendite = re.search(r"RENDITE:\s*([\d,.]+%?)", text).group(1)
        risiko = re.search(r"RISIKO:\s*(\w+)", text).group(1)
        max_p = re.search(r"MAX-PREIS:\s*(.*)", text).group(1)
    except:
        score, rendite, risiko, max_p = "N/A", "N/A", "N/A", "N/A"
        
    return text, score, rendite, risiko, max_p

# 3. Benutzeroberfläche
st.title("🤖 Invest-Scout Pro: Málaga Dashboard")
st.caption(f"Modell: {model_name} | {datetime.date.today().strftime('%d.%m.%Y')}")

tabs = st.tabs(["📋 Neuer Objekt-Check", "⚖️ Investment-Ranking", "📍 Standort-Map"])

# --- TAB 1: BESICHTIGUNG & LIVE-LINKS ---
with tabs[0]:
    col_a, col_b = st.columns([1, 1])
    with col_a:
        st.subheader("🔍 Datenaufnahme")
        obj_name = st.text_input("Objekt-Name (z.B. Finca Axarquía)", placeholder="Finca Almáchar")
        list_price = st.number_input("Angebotspreis (€)", min_value=0, step=5000, value=250000)
        inspect_file = st.file_uploader("Besichtigungs-Foto hochladen", type=["jpg", "png", "jpeg"])
    
    with col_b:
        st.subheader("📝 Analyse-Fokus")
        notes = st.text_area("Notizen zum Objekt", "Analysiere das Bild und gib mir eine Verhandlungsstrategie für Málaga.")
        
    if st.button("🚀 Experten-Analyse & Suche starten", use_container_width=True):
        if obj_name:
            with st.spinner("Agent berechnet Investment-Score und sucht Angebote..."):
                img = Image.open(inspect_file) if inspect_file else None
                full_query = f"Objekt: {obj_name}, Preis: {list_price}€. Notizen: {notes}"
                bericht, score, rendite, risiko, max_p = run_expert_ai(full_query, img)
                
                # Speicherung in der Historie
                st.session_state.visit_history.append({
                    "Datum": datetime.date.today().strftime("%d.%m.%Y"),
                    "Objekt": obj_name,
                    "Preis": list_price,
                    "Score": score,
                    "Rendite": rendite,
                    "Risiko": risiko,
                    "Max-Preis": max_p,
                    "Bericht": bericht
                })
                
                # Anzeige des Berichts
                st.success(f"Analyse abgeschlossen! Score: {score}/10")
                st.markdown(bericht)

                # NEU: Dynamische Link-Erstellung für Live-Angebote
                st.divider()
                st.subheader("🌐 Live-Marktplatz: Passende Angebote")
                st.info(f"Hier findest du aktuelle Angebote in der Provinz Málaga bis {list_price:,} €:")
                
                col_l1, col_l2 = st.columns(2)
                # Filtert direkt nach Preis und Region Málaga
                idealista_url = f"https://www.idealista.com/de/venta-viviendas/malaga-provincia/?precio-maximo={list_price}"
                kyero_url = f"https://www.kyero.com/de/malaga-provinz-immobilien-kaufen-0l3?max_price={list_price}"
                
                with col_l1:
                    st.link_button("🏠 Idealista: Live-Treffer", idealista_url, use_container_width=True)
                with col_l2:
                    st.link_button("🌍 Kyero: Internationale Angebote", kyero_url, use_container_width=True)
        else:
            st.warning("Bitte gib einen Namen für das Objekt ein.")

# --- TAB 2: DAS RANKING ---
with tabs[1]:
    st.subheader("⚖️ Deine Favoriten im Vergleich")
    if st.session_state.visit_history:
        df = pd.DataFrame(st.session_state.visit_history)
        st.dataframe(df[["Score", "Objekt", "Preis", "Max-Preis", "Rendite", "Risiko"]].sort_values(by="Score", ascending=False), use_container_width=True)
        
        st.divider()
        selected = st.selectbox("Detail-Bericht öffnen:", df["Objekt"].tolist())
        sel_item = next(item for item in st.session_state.visit_history if item["Objekt"] == selected)
        st.info(sel_item['Bericht'])
    else:
        st.info("Noch keine Objekte analysiert.")

# --- TAB 3: KARTE ---
with tabs[2]:
    st.subheader("📍 Regionale Übersicht")
    view = pdk.ViewState(latitude=36.72, longitude=-4.42, zoom=9, pitch=45)
    st.pydeck_chart(pdk.Deck(
        map_style=None, 
        initial_view_state=view, 
        layers=[pdk.Layer('ScatterplotLayer', data=pd.DataFrame({'lat':[36.72],'lon':[-4.42]}), 
                get_position='[lon, lat]', get_color='[197, 255, 0, 160]', get_radius=5000)]
    ))
