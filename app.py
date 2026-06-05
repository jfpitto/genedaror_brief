import streamlit as st
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
from datetime import datetime

st.set_page_config(page_title="Generador BRIEF", layout="centered")

st.title("📄 Generador de BRIEF")

# =========================
# CAMPOS (ORDEN NUEVO)
# =========================

helppeople = st.text_input("N° Helppeople *")
fecha = st.date_input("Fecha solicitud *", value=datetime.today())
fecha_str = fecha.strftime("%d/%m/%Y")

iniciativa = st.text_input("Nombre de la Iniciativa *")
descripcion_iniciativa = st.text_area("Descripción de la Iniciativa *")

objetivo = st.text_area("Objetivo *")

usuario = st.text_input("Usuario Solicitante *")
unidad = st.text_input("Unidad de Negocio *")

beneficio = st.text_area("Beneficio Cuantitativo/cualitativo *")

problema = st.text_area("Descripción de la problemática existente *")

areas_roles = st.text_area("Indicar las áreas– roles que intervienen en la situación actual *")

detalle = st.text_area("Detalle del requerimiento *")

riesgo = st.text_area("¿Cuál es el riesgo de NO implementar esta solución? *")

gerente = st.text_input("Nombre del Gerente del área *")

# ✅ Subir múltiples imágenes
imagenes = st.file_uploader(
    "Subir imágenes (opcional)",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

# =========================
# GENERAR DOCUMENTO
# =========================

if st.button("🚀 Generar BRIEF"):

    if not all([
        helppeople, iniciativa, descripcion_iniciativa, objetivo,
        usuario, unidad, beneficio, problema,
        areas_roles, detalle, riesgo, gerente
    ]):
        st.error("⚠️ Completa todos los campos obligatorios (*)")
    else:
        doc = DocxTemplate("template_brief.docx")

        # ✅ PROCESAR IMÁGENES
        imagenes_render = []

        if imagenes:
            for img in imagenes:
                imagen_word = InlineImage(doc, img, width=Mm(120))
                imagenes_render.append(imagen_word)

        # ✅ CONTEXTO
        context = {
            "helppeople": helppeople,
            "fecha": fecha_str,
            "iniciativa": iniciativa,
            "descripcion_iniciativa": descripcion_iniciativa,
            "objetivo": objetivo,
            "usuario": usuario,
            "unidad": unidad,
            "beneficio": beneficio,
            "problema": problema,
            "areas_roles": areas_roles,
            "detalle": detalle,
            "riesgo": riesgo,
            "gerente": gerente,
            "imagenes": imagenes_render
        }

        doc.render(context)

        nombre_archivo = f"BRIEF_{helppeople}.docx"
        doc.save(nombre_archivo)

        with open(nombre_archivo, "rb") as file:
            st.download_button(
                "📥 Descargar BRIEF",
                file,
                file_name=nombre_archivo
            )

        st.success("✅ BRIEF generado correctamente")
