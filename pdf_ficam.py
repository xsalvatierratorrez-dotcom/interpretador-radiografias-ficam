from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import datetime
import os


def generar_pdf_ficam(
    nombre,
    ci,
    edad,
    sexo,
    motivo,
    fecha,
    diagnostico,
    ruta_radiografia=None
):

    os.makedirs(
        "reportes",
        exist_ok=True
    )

    fecha_actual = datetime.now()

    numero_informe = fecha_actual.strftime(
        "%Y%m%d%H%M%S"
    )

    nombre_archivo = (
        f"reportes/{nombre}_FICAM.pdf"
    )

    pdf = canvas.Canvas(
        nombre_archivo,
        pagesize=A4
    )

    ancho, alto = A4

    # =====================================
    # PLANTILLA FONDO
    # =====================================

    plantilla = "assets/plantilla_ficam.png"

    if os.path.exists(
        plantilla
    ):

        pdf.drawImage(
            plantilla,
            0,
            0,
            width=ancho,
            height=alto
        )

    # =====================================
    # TITULO
    # =====================================

    pdf.setFont(
        "Helvetica-Bold",
        14
    )

    pdf.drawCentredString(
        ancho / 2,
        740,
        "INFORME RADIOLOGICO ASISTIDO POR IA"
    )

    # =====================================
    # DATOS INFORME
    # =====================================

    pdf.setFont(
        "Helvetica",
        10
    )

    pdf.drawString(
        60,
        710,
        f"Informe N°: {numero_informe}"
    )

    pdf.drawString(
        300,
        710,
        f"Fecha: {fecha_actual.strftime('%d/%m/%Y')}"
    )

    pdf.drawString(
        450,
        710,
        f"Hora: {fecha_actual.strftime('%H:%M')}"
    )

    # =====================================
    # DATOS PACIENTE
    # =====================================

    pdf.setFont(
        "Helvetica-Bold",
        12
    )

    pdf.drawString(
        60,
        680,
        "DATOS DEL PACIENTE"
    )

    pdf.setFont(
        "Helvetica",
        10
    )

    pdf.drawString(
        60,
        660,
        f"Nombre: {nombre}"
    )

    pdf.drawString(
        60,
        640,
        f"CI: {ci}"
    )

    pdf.drawString(
        60,
        620,
        f"Edad: {edad}"
    )

    pdf.drawString(
        60,
        600,
        f"Sexo: {sexo}"
    )

    pdf.drawString(
        60,
        580,
        f"Fecha del estudio: {fecha}"
    )

    pdf.drawString(
        60,
        560,
        f"Motivo: {motivo}"
    )

    # =====================================
    # RADIOGRAFIA
    # =====================================

    if ruta_radiografia:

        try:

            pdf.drawImage(
                ruta_radiografia,
                60,
                300,
                width=220,
                height=220,
                preserveAspectRatio=True
            )

        except:
            pass

    # =====================================
    # RESULTADO IA
    # =====================================

    pdf.setFont(
        "Helvetica-Bold",
        12
    )

    pdf.drawString(
        320,
        540,
        "RESULTADO IA"
    )

    pdf.setFont(
        "Helvetica",
        10
    )

    texto = pdf.beginText(
        320,
        520
    )

    texto.textLines(
        diagnostico
    )

    pdf.drawText(
        texto
    )

    # =====================================
    # OBSERVACION
    # =====================================

    pdf.setFont(
        "Helvetica-Bold",
        12
    )

    pdf.drawString(
        60,
        250,
        "OBSERVACION"
    )

    pdf.setFont(
        "Helvetica",
        10
    )

    pdf.drawString(
        60,
        230,
        "El resultado fue generado mediante inteligencia artificial."
    )

    pdf.drawString(
        60,
        215,
        "Debe ser interpretado y validado por un profesional medico."
    )

    # =====================================
    # RECOMENDACIONES
    # =====================================

    pdf.setFont(
        "Helvetica-Bold",
        12
    )

    pdf.drawString(
        60,
        180,
        "RECOMENDACIONES"
    )

    pdf.setFont(
        "Helvetica",
        10
    )

    pdf.drawString(
        60,
        160,
        "• Correlacionar con la historia clinica."
    )

    pdf.drawString(
        60,
        145,
        "• Consultar con un medico especialista."
    )

    pdf.drawString(
        60,
        130,
        "• Realizar estudios complementarios si es necesario."
    )

    # =====================================
    # PIE
    # =====================================

    pdf.setFont(
        "Helvetica-Oblique",
        9
    )

    pdf.drawString(
        60,
        60,
        "Facultad de Ingenieria en Ciencias Aplicadas Meca-Electronicas (FICAM)"
    )

    pdf.drawString(
        60,
        45,
        "Sistema de Interpretacion Radiologica Asistida por Inteligencia Artificial"
    )

    pdf.save()

    return nombre_archivo 