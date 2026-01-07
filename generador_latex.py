# ==============================================================================
# GENERADOR DE INFORME TÉCNICO PROFESIONAL (FPDF)
# ==============================================================================
# Autor: Gemini (Tu Asistente de IA)
# Descripción: Genera un PDF académico/profesional resumiendo todo el proyecto.
# Requisitos: !pip install fpdf

import os
try:
    from fpdf import FPDF
except ImportError:
    print("Instalando librería fpdf...")
    import subprocess
    subprocess.check_call(["pip", "install", "fpdf"])
    from fpdf import FPDF

# --- CLASE DE REPORTE PERSONALIZADA ---
class ProfessionalReport(FPDF):
    def header(self):
        # Logo o encabezado corporativo (Simulado)
        self.set_font('Arial', 'B', 10)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, 'Data Science Project: Facebook Metrics Analysis', 0, 1, 'R')
        self.line(10, 20, 200, 20) # Línea horizontal
        self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Pagina {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, num, label):
        self.set_font('Arial', 'B', 14)
        self.set_text_color(0, 51, 102) # Azul oscuro profesional
        self.cell(0, 10, f"{num}. {label}", 0, 1, 'L')
        self.ln(4)

    def chapter_body(self, text):
        self.set_font('Arial', '', 11)
        self.set_text_color(0, 0, 0)
        # Latin-1 encoding para evitar problemas con tildes
        self.multi_cell(0, 6, text.encode('latin-1', 'replace').decode('latin-1'))
        self.ln()

    def add_bullet(self, text):
        self.set_font('Arial', '', 11)
        self.cell(5) # Sangría
        self.cell(5, 6, chr(149), 0, 0) # Bullet point
        self.multi_cell(0, 6, text.encode('latin-1', 'replace').decode('latin-1'))

    def draw_table_results(self):
        # Configuración de tabla
        self.set_font('Arial', 'B', 10)
        self.set_fill_color(240, 240, 240)
        
        # Encabezados
        cols = [45, 45, 45, 45]
        headers = ["Modelo", "Esc 1 (Paper)", "Esc 2 (Pred)", "Esc 3 (Diag)"]
        
        for i, h in enumerate(headers):
            self.cell(cols[i], 8, h, 1, 0, 'C', 1)
        self.ln()
        
        # Datos (Valores aproximados de nuestra sesión)
        self.set_font('Arial', '', 10)
        data = [
            ("Ridge Regression", "139.9%", "136.2%", ">1000% (Fail)"),
            ("SVM (RBF)", "137.8%", "157.8%", "45.7%"),
            ("XGBoost", "105.5% (Best)", "105.8%", "38.4%"),
            ("Random Forest", "115.0%", "114.6%", "36.8% (Best)")
        ]
        
        for row in data:
            for i, datum in enumerate(row):
                # Resaltar ganadores en negrita si es necesario
                if "(Best)" in datum: self.set_font('Arial', 'B', 10)
                else: self.set_font('Arial', '', 10)
                
                self.cell(cols[i], 8, datum, 1, 0, 'C')
            self.ln()
        self.ln(5)

# --- CREACIÓN DEL DOCUMENTO ---
pdf = ProfessionalReport()
pdf.add_page()

# 1. PORTADA
pdf.set_font('Arial', 'B', 24)
pdf.ln(40)
pdf.cell(0, 10, 'INFORME FINAL:', 0, 1, 'C')
pdf.cell(0, 15, 'Prediccion de Engagement en Facebook', 0, 1, 'C')
pdf.ln(10)
pdf.set_font('Arial', '', 14)
pdf.cell(0, 10, 'Analisis Comparativo, Diagnostico y Modelado Predictivo', 0, 1, 'C')
pdf.ln(20)
pdf.set_font('Arial', 'I', 12)
pdf.cell(0, 10, 'Dataset: Cosmetic Brand (Moro et al., 2016)', 0, 1, 'C')
pdf.ln(50)
pdf.set_font('Arial', '', 10)
pdf.cell(0, 10, 'Generado automaticamente tras analisis exhaustivo en Python', 0, 1, 'C')
pdf.add_page()

# 2. INTRODUCCIÓN
pdf.chapter_title(1, 'Introduccion y Contexto de Negocio')
pdf.chapter_body(
    "El presente informe detalla el proceso de analisis, limpieza y modelado predictivo realizado sobre un conjunto de datos "
    "perteneciente a una reconocida marca de cosmeticos en Facebook. El objetivo principal no es solo predecir metricas, "
    "sino entender la dinamica detras de la interaccion del usuario.\n\n"
    "A diferencia de enfoques tradicionales, este proyecto distingue dos necesidades de negocio fundamentales:"
)
pdf.add_bullet("Necesidad A (Prediccion a Priori): Estimar el exito de un post ANTES de publicarlo, usando solo variables disponibles al momento de la creacion (Hora, Mes, Tipo).")
pdf.add_bullet("Necesidad B (Diagnostico Post-Hoc): Entender las causas del exito UNA VEZ publicado el post, analizando correlaciones con la viralidad (Shares, Reach).")
pdf.ln()

# 3. EDA
pdf.chapter_title(2, 'Hallazgos del Analisis Exploratorio (EDA)')
pdf.chapter_body(
    "Se realizo un analisis estadistico riguroso que arrojo los siguientes descubrimientos clave:"
)
pdf.add_bullet("Distribucion del Target: La variable 'Likes' presenta una distribucion log-normal con fuerte sesgo positivo. El test de Shapiro-Wilk confirmo la no-normalidad (p < 0.05), justificando la transformacion logaritmica (Log1p) para el modelado.")
pdf.add_bullet("Diferencia con la Literatura: Contrario al paper de Moro et al., en este dataset el 'Tipo de Contenido' (Foto vs Video) mostro menor relevancia que las variables temporales y el tamaño de la comunidad (Page Likes).")
pdf.add_bullet("Data Leakage: Se detecto una correlacion de Spearman > 0.85 entre 'Shares' y 'Likes', lo que confirma que la viralidad es el predictor mas potente, aunque no este disponible 'a priori'.")
pdf.ln()

# 4. METODOLOGÍA
pdf.chapter_title(3, 'Definicion de Escenarios de Modelado')
pdf.chapter_body(
    "Para garantizar la honestidad metodologica, se diseñaron tres escenarios experimentales:"
)
pdf.set_font('Arial', 'B', 11)
pdf.cell(0, 8, 'Escenario 1: Paper Original (Benchmark)', 0, 1)
pdf.set_font('Arial', '', 11)
pdf.chapter_body("Replicacion exacta de las 7 variables usadas por Moro et al. para establecer una linea base.")

pdf.set_font('Arial', 'B', 11)
pdf.cell(0, 8, 'Escenario 2: Optimizado (Sin Leakage)', 0, 1)
pdf.set_font('Arial', '', 11)
pdf.chapter_body("Ingenieria de caracteristicas temporal. Se crearon variables como 'Is_Weekend' y 'Time_Segment' (Morning/Evening) para mejorar la prediccion a priori sin usar datos del futuro.")

pdf.set_font('Arial', 'B', 11)
pdf.cell(0, 8, 'Escenario 3: Lifetime (Diagnostico)', 0, 1)
pdf.set_font('Arial', '', 11)
pdf.chapter_body("Inclusion de metricas post-publicacion seleccionadas via Information Gain (Mutual Information). Este escenario modela la relacion Viralidad-Exito.")
pdf.ln()

# 5. RESULTADOS
pdf.chapter_title(4, 'Resultados del Benchmark y Evaluacion')
pdf.chapter_body(
    "Se evaluaron 4 algoritmos (Ridge, RF, XGBoost, SVM) utilizando validacion cruzada de 5 pliegues (K-Fold). "
    "La metrica principal fue el MAPE (Error Porcentual Absoluto Medio)."
)
pdf.ln(2)
pdf.draw_table_results()
pdf.chapter_body(
    "Analisis de Resultados:\n"
    "- La prediccion a priori (Esc 1 y 2) presenta un error alto (~105%), indicando que el exito en redes sociales tiene un componente estocastico alto que no depende solo de la hora de publicacion.\n"
    "- El modelo de diagnostico (Esc 3) reduce el error drasticamente al 36% con Random Forest, confirmando que el sistema es predecible si se conoce el alcance (Reach) y la viralidad (Shares)."
)
pdf.ln()

# 6. SHAP Y CONCLUSIONES
pdf.chapter_title(5, 'Interpretacion (SHAP) y Conclusiones')
pdf.chapter_body(
    "El analisis de valores SHAP revelo la 'Caja Negra' de los modelos:\n"
    "1. En el Escenario 3, la variable 'Shares' domina la prediccion. Un post compartido actua como multiplicador exponencial de Likes.\n"
    "2. En el Escenario 2, las variables temporales como 'Month' y 'Hour' tienen impacto, pero insuficiente para explicar los outliers virales.\n\n"
    "CONCLUSION FINAL:\n"
    "El proyecto demuestra que es posible diagnosticar con precision el rendimiento (R2 > 0.6) basandose en la viralidad. "
    "Sin embargo, la prediccion 'a ciegas' requiere incorporar nuevas fuentes de datos (analisis de imagen/texto) para superar la barrera del 100% de error."
)

# Guardar PDF
output_path = 'Informe_Final_Facebook_Profesional.pdf'
pdf.output(output_path)
print(f"✅ ¡Informe Generado! Busca el archivo: {output_path}")