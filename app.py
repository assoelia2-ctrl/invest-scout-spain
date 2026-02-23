import streamlit as st
import pandas as pd
import requests
from openai import OpenAI

# 1. SETUP
st.set_page_config(page_title="Málaga Invest Pro", layout="centered")

openai_key = st.secrets.get("OPENAI_API_KEY")
groq_key = st.secrets.get("GROQ_API_KEY")
client = OpenAI(api_key=openai_key) if openai_key else None

# 2. DER "BRÜCKEN-DIENST" (Damit die KI den Link lesen kann)
def fetch_page_content(url):
    """Verwandelt eine Webseite in Text, den die KI verstehen kann."""
    try:
        # Wir nutzen Jina AI als Reader-Brücke, um Blockaden zu umgehen
        reader_url = f"https://r.jina.ai/{url}"
        response = requests.get(reader_url, timeout=10)
        if response.status_code == 200:
            return response.text[:5000] # Die wichtigsten 5000 Zeichen
        else:
            return None
    except:
        return None

# 3. INTERFACE
st.title("🤖 Málaga Invest-Zentrale")

# Link-Eingabe
anzeigen_link = st.text_input("🔗 Link zur Anzeige (Idealista/Fotocasa):", placeholder="https://www.idealista.com/...")

# Sofort-Analyse wenn ein Link eingefügt wird
if anzeigen_link:
    with st.status("Verbinde mit Immobilienteil..."):
        content = fetch_page_content(anzeigen_link)
        
        if content:
            st.success("✅ Link-Daten erfolgreich geladen!")
            
            # KI-AUFGABE: Zusammenfassen und Analysieren
            if st.button("🚀 JETZT VOLLSTÄNDIG ANALYSIEREN"):
                with st.spinner("KI liest die Anzeige..."):
                    prompt = f"""
                    Analysiere diese Immobilienanzeige im Detail:
                    {content}
                    
                    Fasse zusammen:
                    1. Eckdaten (m2, Zimmer, Preis, Ort).
                    2. Rechtliche Risiken (Suelo Rústico, AFO/DAFO erwähnt?).
                    3. Fazit: Lohnt sich die Besichtigung?
                    """
                    
                    # Nutzt Groq (um deinen OpenAI Quota-Error 429 zu umgehen)
                    if groq_key:
                        url = "https://api.groq.com/openai/v1/chat/completions"
                        headers = {"Authorization": f"Bearer {groq_key}"}
                        payload = {
                            "model": "llama-3.3-70b-versatile",
                            "messages": [{"role": "user", "content": prompt}]
                        }
                        res = requests.post(url, json=payload, headers=headers).json()
                        st.markdown("### 📊 Analyse-Ergebnis")
                        st.write(res['choices'][0]['message']['content'])
        else:
            st.error("❌ Die Seite blockiert den Zugriff. Bitte Link prüfen.")

# 4. FINANZ-RECHNER
st.divider()
preis = st.number_input("Kaufpreis (€):", value=250000, step=5000)
itp = preis * 0.07
st.info(f"Steuern (7% ITP): {itp:,.0f} € | Gesamt-Invest: {preis + itp:,.0f} €")

st.caption("System: Brücken-Reader aktiv | Groq/OpenAI Dual-Core | ITP 7%")
