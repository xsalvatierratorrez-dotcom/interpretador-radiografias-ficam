import streamlit as st
import sqlite3
import pandas as pd

# -------------------------
# CONFIGURACIÓN DE PÁGINA
# -------------------------

st.set_page_config(
    page_title="Interpretador de Radiografías de Tórax",
    page_icon="🩻",
    layout="wide"
)

# -------------------------
# BASE DE DATOS SQLITE
# -------------------------

conexion = sqlite3.connect("historial.db", check_same_thread=False)
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

# -------------------------
# TÍTULO
# -------------------------

st.title("🩻 INTERPRETADOR DE RADIOGRAFÍAS DE TÓRAX")
st.subheader("Facultad de Ingeniería en Ciencias Aplicadas Meca-Electrónicas (FICAM)")

st.markdown("---")

# -------------------------
# DATOS DEL PACIENTE
# -------------------------

st.header("Datos del Paciente")

col1, col2 = st.columns(2)

with col1:
    nombre = st.text_input("Nombre Completo")
    ci = st.text_input("CI / ID")
    edad = st.number_input("Edad", min_value=0, max_value=120)

with col2:
    sexo = st.selectbox(
        "Sexo",
        ["Masculino", "Femenino"]
    )

    fecha = st.date_input("Fecha del Estudio")

    motivo = st.text_input("Motivo de Consulta")

st.markdown("---")

# -------------------------
# RADIOGRAFÍA
# -------------------------

st.header("Radiografía de Tórax")

imagen = st.file_uploader(
    "Seleccione una radiografía",
    type=["png", "jpg", "jpeg"]
)

if imagen is not None:
    st.image(imagen, caption="Radiografía cargada", width=500)

st.markdown("---")

# -------------------------
# BOTÓN ANALIZAR
# -------------------------

if st.button("Analizar Radiografía"):

    diagnostico = "Pendiente de integración con IA"

    cursor.execute("""
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
    ))

    conexion.commit()

    st.success("Paciente guardado correctamente")

    st.header("Resultados de Inteligencia Artificial")

    st.write("Patología detectada:")
    st.info(diagnostico)

    st.write("Nivel de confianza:")
    st.info("0 %")

    st.header("Hallazgos Radiológicos")

    st.text_area(
        "",
        "Aquí aparecerán los hallazgos radiológicos generados por la IA.",
        height=120
    )

    st.header("Impresión Diagnóstica")

    st.text_area(
        "",
        "Aquí aparecerá la impresión diagnóstica.",
        height=120
    )

    st.header("Explicación Médica")

    st.text_area(
        "",
        "Aquí aparecerá la explicación médica.",
        height=120
    )

    st.header("Explicación para el Paciente")

    st.text_area(
        "",
        "Aquí aparecerá la explicación para el paciente.",
        height=120
    )

    st.header("Recomendaciones")

    st.write("• Recomendación 1")
    st.write("• Recomendación 2")
    st.write("• Recomendación 3")

# -------------------------
# HISTORIAL
# -------------------------

st.markdown("---")

st.header("Historial de Pacientes")

datos = pd.read_sql_query(
    "SELECT * FROM pacientes",
    conexion
)

st.dataframe(
    datos,
    use_container_width=True
)