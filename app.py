import streamlit as st
import sqlite3
import pandas as pd
import os

from pdf_ficam import generar_pdf_ficam
from ia_radiografias import diagnosticar

# ==========================================
# CONFIGURACION PAGINA
# ==========================================

st.set_page_config(
    page_title="Interpretador de Radiografías de Tórax",
    page_icon="🩻",
    layout="wide"
)

# ==========================================
# BASE DE DATOS SQLITE
# ==========================================

conexion = sqlite3.connect(
    "historial.db",
    check_same_thread=False
)

cursor = conexion.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS pacientes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    ci TEXT,
    edad INTEGER,
    sexo TEXT,
    motivo TEXT,
    fecha TEXT,
    diagnostico TEXT
)
""")

conexion.commit()

# ==========================================
# TITULO
# ==========================================

st.title("🩻 INTERPRETADOR DE RADIOGRAFÍAS DE TÓRAX")
st.subheader(
    "Facultad de Ingeniería en Ciencias Aplicadas Meca-Electrónicas (FICAM)"
)

# ==========================================
# DASHBOARD
# ==========================================

total_pacientes = cursor.execute(
    "SELECT COUNT(*) FROM pacientes"
).fetchone()[0]

st.header("📊 Dashboard")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Pacientes Registrados",
        total_pacientes
    )

with c2:
    st.metric(
        "Informes Generados",
        total_pacientes
    )

with c3:
    st.metric(
        "Radiografías Analizadas",
        total_pacientes
    )

st.markdown("---")

# ==========================================
# DATOS PACIENTE
# ==========================================

st.header("Datos del Paciente")

col1, col2 = st.columns(2)

with col1:

    nombre = st.text_input(
        "Nombre Completo"
    )

    ci = st.text_input(
        "CI / ID"
    )

    edad = st.number_input(
        "Edad",
        min_value=0,
        max_value=120
    )

with col2:

    sexo = st.selectbox(
        "Sexo",
        [
            "Masculino",
            "Femenino"
        ]
    )

    fecha = st.date_input(
        "Fecha del Estudio"
    )

    motivo = st.text_input(
        "Motivo de Consulta"
    )

st.markdown("---")

# ==========================================
# RADIOGRAFIA
# ==========================================

st.header("Radiografía de Tórax")

imagen = st.file_uploader(
    "Seleccione una radiografía",
    type=["png", "jpg", "jpeg"]
)

ruta_temporal = None

if imagen is not None:

    st.image(
        imagen,
        caption="Radiografía cargada",
        width=500
    )

    os.makedirs(
        "reportes",
        exist_ok=True
    )

    ruta_temporal = (
        "reportes/radiografia_temporal.png"
    )

    with open(
        ruta_temporal,
        "wb"
    ) as f:

        f.write(
            imagen.getbuffer()
        )

st.markdown("---")

# ==========================================
# BOTON NUEVO PACIENTE
# ==========================================

if st.button(
    "🔄 Nuevo Paciente"
):
    st.rerun()

# ==========================================
# ANALISIS IA
# ==========================================

if st.button(
    "Analizar Radiografía"
):

    if ruta_temporal is None:

        st.error(
            "Debe cargar una radiografía."
        )

    else:

        try:

            resultado_ia = diagnosticar(
                ruta_temporal
            )

            patologia = resultado_ia[
                "patologia"
            ]

            confianza = resultado_ia[
                "confianza"
            ]

            explicacion = resultado_ia[
                "explicacion"
            ]

            diagnostico = f"""
Patología detectada: {patologia}

Nivel de confianza: {confianza} %

{explicacion}
"""

            cursor.execute(
                """
                INSERT INTO pacientes(
                    nombre,
                    ci,
                    edad,
                    sexo,
                    motivo,
                    fecha,
                    diagnostico
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    nombre,
                    ci,
                    edad,
                    sexo,
                    motivo,
                    str(fecha),
                    diagnostico
                )
            )

            conexion.commit()

            pdf_generado = generar_pdf_ficam(
                nombre,
                ci,
                edad,
                sexo,
                motivo,
                fecha,
                diagnostico,
                ruta_temporal
            )

            st.success(
                "Paciente guardado correctamente"
            )

            st.header(
                "Resultados de Inteligencia Artificial"
            )

            st.success(
                f"Patología detectada: {patologia}"
            )

            st.metric(
                "Nivel de confianza",
                f"{confianza}%"
            )

            st.subheader(
                "🏆 Top 3 Patologías Detectadas"
            )

            if "top3" in resultado_ia:

                for item in resultado_ia["top3"]:

                    st.write(
                        f"• {item['patologia']} → {item['confianza']}%"
                    )

            st.subheader(
                "📊 Resultados completos IA"
            )

            st.json(
                resultado_ia["resultados"]
            )

            st.info(
                explicacion
            )

            st.header(
                "Hallazgos Radiológicos"
            )

            st.write(
                explicacion
            )

            st.header(
                "Impresión Diagnóstica"
            )

            st.write(
                diagnostico
            )

            st.header(
                "Explicación para el Paciente"
            )

            st.write(
                f"""
La inteligencia artificial detectó principalmente:

{patologia}

con una confianza aproximada de

{confianza} %

Este resultado es orientativo y debe ser
confirmado por un profesional médico.
"""
            )

            st.header(
                "Recomendaciones"
            )

            st.write(
                "• Consultar con un médico especialista."
            )

            st.write(
                "• Correlacionar con síntomas clínicos."
            )

            st.write(
                "• Solicitar estudios complementarios si es necesario."
            )

            with open(
                pdf_generado,
                "rb"
            ) as archivo:

                st.download_button(
                    label="📄 Descargar Informe PDF FICAM",
                    data=archivo,
                    file_name=f"{nombre}_FICAM.pdf",
                    mime="application/pdf"
                )

        except Exception as e:

            st.error(
                f"Error durante el análisis: {e}"
            )

# ==========================================
# HISTORIAL
# ==========================================

st.markdown("---")

st.header(
    "📚 Historial de Pacientes"
)

busqueda = st.text_input(
    "🔍 Buscar por nombre o CI"
)

if busqueda:

    consulta = f"""
    SELECT *
    FROM pacientes
    WHERE nombre LIKE '%{busqueda}%'
    OR ci LIKE '%{busqueda}%'
    ORDER BY id DESC
    """

else:

    consulta = """
    SELECT *
    FROM pacientes
    ORDER BY id DESC
    """

datos = pd.read_sql_query(
    consulta,
    conexion
)

st.dataframe(
    datos,
    use_container_width=True
) 