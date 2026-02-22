import streamlit as st
import requests
import pandas as pd
import pydeck as pdk
import datetime
import re

# 1. SETUP & AGENTEN-GEHIRN
st.set_page_config(page_title="Málaga Invest Agent Pro", layout="wide")
api_key = st.secrets.get("GROQ_API_KEY") or st.secrets.get("GEMINI_API_KEY")

def call_agent(prompt):
    # Wir nutzen ein stabileres Modell (Llama 3), um 'Überlastet'-Fehler zu vermeiden
    if st.secrets.get("GROQ_API_KEY"):
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}]}
        response = requests.post(url, headers=headers, json=payload)
        return response.json()['choices'][0]['message']['content']
    else:
        # Fallback auf Google mit Fehlerbehandlung
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        res = requests.post(url, json=payload)
        if res.status_code == 200:
            return res.json()['candidates'][0]['content']['parts'][0]['text']
        return "Agent macht gerade Pause (Limit erreicht). Bitte in 1 Minute nochmal."

# Speicher für den Agenten
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = []

# 2. DAS AGENTEN-DASHBOARD
st.title("🤖 Dein Málaga Investment-Agent")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["🔎 Agenten-Suche", "📋 Portfolio & Auswertung", "📍 Markt-Karte"])

with tab1:
    col1, col2 = st.columns([2, 1])
    with col1:
        query = st.text_input("Was soll ich für dich finden?", value="Finca mit Pool im Umland von Málaga")
        budget = st.number_input("Budget (€)", value=250000, step=5000)
    
    with col2:
        st.write("**Agenten-Status**")
        st.success("Bereit zur Analyse")
        idealista_link = f"https://www.idealista.com/de/venta-viviendas/malaga-provincia/?precio-maximo={budget}"
        st.link_button("🏠 Direkt zu den Angeboten", idealista_link, use_container_width=True)

    if st.button("🚀 Agenten-Analyse starten", use_container_width=True):
        with st.spinner("Agent wertet Marktdaten aus..."):
            agent_prompt = f"""
            Du bist ein Immobilien-KI-Agent. Analysiere: {query} für {budget}€.
            1. Gebiets-Check: Wo in Málaga passt das? (z.B. Axarquía, Guadalhorce Tal)
            2. Finanz-Check: Berechne 7% ITP Steuer und 1% Notar.
            3. Rendite-Check: Kurze Einschätzung der Miet-Chancen.
            Beende mit SCORE: [X]/10
            """
            antwort = call_agent(agent_prompt)
            st.markdown("### 🤖 Agenten-Bericht:")
            st.write(antwort)
            
            # Score extrahieren & Speichern
            score = re.search(r"SCORE:\s*(\d+)", antwort).group(1) if "SCORE" in antwort else "7"
            st.session_state.portfolio.append({
                "Datum": datetime.date.today(),
                "Objekt": query,
                "Budget": budget,
                "Score": f"{score}/10"
            })

with tab2:
    st.subheader("📋 Vom Agenten ausgewertete Objekte")
    if st.session_state.portfolio:
        df = pd.DataFrame(st.session_state.portfolio)
        st.table(df)
        st.download_button("📥 Liste als CSV speichern", df.to_csv().encode('utf-8'), "agent_portfolio.csv")
    else:
        st.info("Noch keine Objekte im Portfolio.")

with tab3:
    st.subheader("📍 Analyse-Hotspots")
    # Markiert Málaga auf der Karte
    view = pdk.ViewState(latitude=36.72, longitude=-4.42, zoom=10)
    st.pydeck_chart(pdk.Deck(initial_view_state=view, layers=[
        pdk.Layer('ScatterplotLayer', data=pd.DataFrame({'lat':[36.72], 'lon':[-4.42]}), 
                  get_position='[lon, lat]', get_radius=1000, get_color='[200, 30, 0]')
    ]))
