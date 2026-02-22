import streamlit as st
import requests
import pandas as pd
import datetime

# SETUP
st.set_page_config(page_title="Málaga Invest Agent Pro", layout="wide")
api_key = st.secrets.get("GROQ_API_KEY") or st.secrets.get("GEMINI_API_KEY")

def ki_agent_suche(query, budget):
    """Unser Agent analysiert, rechnet und bewertet."""
    prompt = f"""
    Du bist unser spezialisierter Málaga-Investment-Agent. 
    Analysiere die Anfrage: '{query}' mit Budget {budget}€.
    
    1. IMMOBILIEN-SUCHE: Nenne konkrete Gebiete in Málaga (z.B. Almogía, Coín, Montes de Málaga), 
       wo man für {budget}€ noch Fincas oder Häuser findet.
    2. FINANZ-CHECK: Berechne ca. 10% Nebenkosten (ITP, Notar) und schätze die jährliche IBI (Grundsteuer).
    3. AGENTEN-URTEIL: Lohnt sich das Investment aktuell? (Markttrend Málaga 2025: +5-10%).
    
    Gib am Ende 3 Direktlinks zu Idealista-Suchen aus, die genau auf dieses Budget passen.
    AGENTEN-SCORE: [X]/10
    """
    
    # Nutzt die erfolgreiche v1beta Route
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, json=payload, timeout=20)
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "Agent momentan überlastet. Bitte erneut versuchen."

# UI
st.title("🤖 Dein Málaga Investment-Agent")
st.info("Der Agent ist aktiv und analysiert Live-Marktdaten für dich.")

col1, col2 = st.columns([2, 1])

with col1:
    user_query = st.text_input("Was soll der Agent suchen?", value="Finca mit Garten in Málaga Umland")
    budget = st.number_input("Max. Budget (€)", value=250000)
    
    if st.button("🚀 Agenten-Suche starten"):
        with st.spinner("Agent wertet Angebote aus..."):
            analyse = ki_agent_suche(user_query, budget)
            st.markdown(analyse)
            
            # Automatischer Schnell-Link
            st.divider()
            st.link_button("👉 Direkt-Suche auf Idealista (Preisgeprüft)", 
                           f"https://www.idealista.com/de/venta-viviendas/malaga-provincia/?precio-maximo={budget}")

with col2:
    st.subheader("📋 Agenten-Logbuch")
    st.write("Hier speichert der Agent deine besten Funde für später.")
    # Platzhalter für Portfolio-Funktion
