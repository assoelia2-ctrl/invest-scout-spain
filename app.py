import gradio as gr
import google.generativeai as genai
from PIL import Image
from fpdf import FPDF
import tempfile
import os

# API Setup
def setup_genai(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash')

def create_pdf(text, image):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Immobilien-Analyse: Andalusien", ln=True, align='C')
    pdf.ln(10)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        image.save(tmp.name, format="PNG")
        pdf.image(tmp.name, x=10, y=30, w=90)
        tmp_path = tmp.name

    pdf.ln(85)
    pdf.set_font("Arial", size=11)
    clean_text = text.replace("**", "").replace("*", "-").replace("€", "Euro")
    pdf.multi_cell(0, 8, clean_text.encode('latin-1', 'ignore').decode('latin-1'))
    
    output_path = tempfile.mktemp(suffix=".pdf")
    pdf.output(output_path)
    return output_path

def analyze_and_report(api_key, input_img):
    if not api_key:
        return "Bitte API-Key eingeben!", None
    
    try:
        model = setup_genai(api_key)
        prompt = "Du bist Baugutachter in Andalusien. Analysiere Substanz, Zufahrt und Solar-Potential. Gliedere in RISIKEN, CHANCEN und KOSTEN."
        response = model.generate_content([prompt, input_img])
        analysis_text = response.text
        
        pdf_file = create_pdf(analysis_text, input_img)
        return analysis_text, pdf_file
    except Exception as e:
        return f"Fehler: {str(e)}", None

# Gradio Interface
with gr.Blocks(title="Andalusien Invest Scout") as demo:
    gr.Markdown("# ☀️ Andalusien Real Estate Master (Gradio Edition)")
    
    with gr.Row():
        api_input = gr.Textbox(label="Dein Gemini API-Key", type="password")
        image_input = gr.Image(type="pil", label="Objekt-Screenshot")
    
    analyze_btn = gr.Button("🔍 Analyse starten & PDF erstellen")
    
    output_text = gr.Textbox(label="KI-Analyse", lines=10)
    output_pdf = gr.File(label="📥 Download Gutachten (PDF)")
    
    analyze_btn.click(
        fn=analyze_and_report, 
        inputs=[api_input, image_input], 
        outputs=[output_text, output_pdf]
    )

demo.launch()
