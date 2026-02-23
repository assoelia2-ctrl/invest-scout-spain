from fpdf import FPDF
import os

class MalagaReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Immobilien-Analyse: Málaga Projekt', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Seite {self.page_no()}', 0, 0, 'C')

def generate_pdf(image_folder, output_name):
    pdf = MalagaReport()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Alle Bilder im Ordner finden
    images = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    images.sort() # Alphabetische Sortierung

    for img_name in images:
        pdf.add_page()
        
        # Titel aus Dateinamen generieren (Unterstriche zu Leerzeichen)
        title = os.path.splitext(img_name)[0].replace('_', ' ')
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, title, 0, 1, 'L')
        
        # Bild einfügen (Skalierung auf Seitenbreite)
        img_path = os.path.join(image_folder, img_name)
        pdf.image(img_path, x=10, y=30, w=190) 

    pdf.output(output_name)
    print(f"Erfolg! Das Dossier '{output_name}' wurde erstellt.")

# Beispielaufruf (Passe den Pfad an deinen Screenshot-Ordner an)
# generate_pdf('./screenshots', 'Malaga_Investment_Report.pdf')
