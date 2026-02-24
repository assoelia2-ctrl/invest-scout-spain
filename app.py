import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. API Setup
api_key = st.secrets.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

st.title("☀️ Andalusien Real Estate Master")

# 2. Tiefenprüfung der Modelle (erscheint in der Sidebar)
with st.sidebar:
    st.header("System-Check")
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        st.write("Verfügbare Modelle:", available_models)
        # Wir wählen automatisch das beste verfügbare Modell
        selected_model = "models/gemini-1.5-flash" if "models/gemini-1.5-flash" in available_models else available_models[0]
        st.success(f"Nutze: {selected_model}")
    except Exception as e:
        st.error(f"Verbindung zu Google fehlgeschlagen: {e}")
        selected_model = None

# 3. Analyse Logik
def analyze(img, model_name):
    model = genai.GenerativeModel(model_name)
    prompt = "Du bist Baugutachter in Andalusien. Analysiere Substanz, Zufahrt und Solar-Potential. Gliedere in RISIKEN, CHANCEN, KOSTEN."
    response = model.generate_content([prompt, img])
    return response.text

uploaded_file = st.file_uploader("Bild hochladen", type=['png', 'jpg', 'jpeg'])

if uploaded_file and selected_model:
    img = Image.open(uploaded_file)
    st.image(img, width=400)
    if st.button("Analyse starten"):
        with st.spinner("Prüfe..."):
            try:
                result = analyze(img, selected_model)
                st.markdown(result)
            except Exception as e:
                st.error(f"Fehler: {e}")
