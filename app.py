import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
import pydeck as pdk
import datetime
import re

# 1. SEITE INITIALISIEREN
st.set_page_config(page_title="Invest-Scout: Málaga Pro", layout="wide")

# 2. STABILER API-SETUP (Hardcoded Fix)
api_key = st.secrets.get("GEMINI_API_KEY") or st.secrets.get("GOOGLE_API_KEY")

if api_key:
    try:
        # Hier ist der Trick: Wir setzen den Transport auf 'rest', 
        # das umgeht oft gRPC-Probleme in Cloud-Umgebungen
        genai.configure(api_key=api_key, transport='rest')
        
        # Wir nutzen das Modell direkt über das stabile GenerativeModel-Objekt
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"Verbindungsfehler: {e}")
        st.stop()
else:
    st.warning("Kein API-Key gefunden. Bitte in den Secrets hinterlegen.")
    st.stop()
