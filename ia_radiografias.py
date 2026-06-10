import cv2
import torch
import numpy as np
import torchxrayvision as xrv

# ==========================================
# MODELO IA
# ==========================================

modelo = xrv.models.DenseNet(
    weights="densenet121-res224-all"
)

# ==========================================
# TRADUCCIONES
# ==========================================

TRADUCCIONES = {
    "Atelectasis": "Atelectasia",
    "Cardiomegaly": "Cardiomegalia",
    "Consolidation": "Consolidación Pulmonar",
    "Edema": "Edema Pulmonar",
    "Effusion": "Derrame Pleural",
    "Emphysema": "Enfisema Pulmonar",
    "Fibrosis": "Fibrosis Pulmonar",
    "Infiltration": "Infiltrado Pulmonar",
    "Mass": "Masa Pulmonar",
    "Nodule": "Nódulo Pulmonar",
    "Pleural_Thickening": "Engrosamiento Pleural",
    "Pneumonia": "Neumonía",
    "Pneumothorax": "Neumotórax",
    "Lung Opacity": "Opacidad Pulmonar",
    "Lung Lesion": "Lesión Pulmonar",
    "Fracture": "Fractura",
    "Enlarged Cardiomediastinum": "Ensanchamiento Cardiomediastínico",
    "Hernia": "Hernia"
}

# ==========================================
# EXPLICACIONES
# ==========================================

EXPLICACIONES = {
    "Atelectasis": "Posible colapso parcial de una región pulmonar.",
    "Cardiomegaly": "Posible aumento del tamaño cardíaco.",
    "Consolidation": "Posible consolidación pulmonar compatible con infección o inflamación.",
    "Edema": "Posible acumulación de líquido pulmonar.",
    "Effusion": "Posible acumulación de líquido en la cavidad pleural.",
    "Emphysema": "Posibles cambios compatibles con enfisema pulmonar.",
    "Fibrosis": "Posibles cambios fibróticos pulmonares.",
    "Infiltration": "Posible infiltrado pulmonar.",
    "Mass": "Posible masa pulmonar que requiere evaluación médica.",
    "Nodule": "Posible nódulo pulmonar.",
    "Pleural_Thickening": "Posible engrosamiento pleural.",
    "Pneumonia": "Posibles hallazgos compatibles con neumonía.",
    "Pneumothorax": "Posible presencia de aire en la cavidad pleural.",
    "Lung Opacity": "Posible opacidad pulmonar.",
    "Lung Lesion": "Posible lesión pulmonar.",
    "Fracture": "Posible fractura ósea visible.",
    "Enlarged Cardiomediastinum": "Posible aumento del tamaño cardiomediastínico.",
    "Hernia": "Posible hernia."
}

# ==========================================
# ANALISIS IA
# ==========================================

def analizar_radiografia(ruta_imagen):

    img = cv2.imread(
        ruta_imagen,
        cv2.IMREAD_GRAYSCALE
    )

    if img is None:

        raise Exception(
            "No se pudo cargar la imagen."
        )

    # Normalización recomendada por TorchXRayVision

    img = xrv.datasets.normalize(
        img,
        255
    )

    img = cv2.resize(
        img,
        (224, 224)
    )

    img = img.astype(
        np.float32
    )

    img = img[None, :, :]

    img = torch.from_numpy(
        img
    )

    with torch.no_grad():

        pred = modelo(
            img.unsqueeze(0)
        )

    resultados = {}

    for i, patologia in enumerate(
        modelo.pathologies
    ):

        resultados[patologia] = float(
            pred[0][i]
        )

    return resultados

# ==========================================
# DIAGNOSTICO
# ==========================================

def diagnosticar(ruta_imagen):

    resultados = analizar_radiografia(
        ruta_imagen
    )

    # Filtrar hallazgos relevantes

    resultados_filtrados = {}

    for nombre, valor in resultados.items():

        if valor >= 0.40:

            resultados_filtrados[nombre] = valor

    if len(resultados_filtrados) == 0:

        resultados_filtrados = resultados

    top = sorted(
        resultados_filtrados.items(),
        key=lambda x: x[1],
        reverse=True
    )

    top3 = top[:3]

    mejor_patologia = top3[0][0]

    confianza = top3[0][1]

    patologia_es = TRADUCCIONES.get(
        mejor_patologia,
        mejor_patologia
    )

    explicacion = EXPLICACIONES.get(
        mejor_patologia,
        "Hallazgo detectado por IA."
    )

    top3_es = []

    for nombre, valor in top3:

        top3_es.append({

            "patologia":
            TRADUCCIONES.get(
                nombre,
                nombre
            ),

            "confianza":
            round(
                valor * 100,
                2
            )
        })

    diferencia = (
        top3[0][1] -
        top3[1][1]
    )

    if diferencia < 0.05:

        conclusion = (
            "Se observan varios hallazgos con "
            "probabilidades similares. Se recomienda "
            "correlación clínica y valoración médica."
        )

    else:

        conclusion = (
            f"El hallazgo predominante es "
            f"{patologia_es}."
        )

    return {

        "patologia":
        patologia_es,

        "confianza":
        round(
            confianza * 100,
            2
        ),

        "explicacion":
        explicacion,

        "conclusion":
        conclusion,

        "top3":
        top3_es,

        "resultados":
        resultados
    }

# ==========================================
# PRUEBA
# ==========================================

if __name__ == "__main__":

    resultado = diagnosticar(
        "reportes/radiografia_temporal.png"
    )

    print("\nDIAGNOSTICO IA\n")

    print(
        resultado["patologia"]
    )

    print(
        resultado["confianza"],
        "%"
    )

    print(
        resultado["explicacion"]
    ) 