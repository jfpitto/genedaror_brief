import streamlit as st
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
from datetime import datetime

st.set_page_config(page_title="Generador BRIEF", layout="centered")

st.title("📄 Generador de BRIEF")

# =========================
# CAMPOS
# =========================

helppeople = st.text_input("N° Helppeople *")
iniciativa = st.text_input("Nombre de la Iniciativa *")
fecha = st.date_input("Fecha solicitud *", value=datetime.today())
fecha_str = fecha.strftime("%d/%m/%Y")
usuario = st.text_input("Usuario Solicitante *")
unidad = st.text_input("Unidad de Negocio *")
objetivo = st.text_area("Objetivo *")
problema = st.text_area("Descripción de la problemática existente *")
detalle = st.text_area("Detalle del requerimiento *")
nombre_usuario = st.text_input("Nombre del Usuario *")
gerente = st.text_input("Nombre del Gerente del área *")

# ✅ NUEVO: subir múltiples imágenes
imagenes = st.file_uploader(
    "Subir imágenes (opcional)",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

# =========================
# GENERAR DOCUMENTO
# =========================

if st.button("🚀 Generar BRIEF"):

    if not all([helppeople, iniciativa, usuario, unidad,
                objetivo, problema, detalle, nombre_usuario, gerente]):
        st.error("⚠️ Completa todos los campos obligatorios (*)")
    else:
        doc = DocxTemplate("template_brief.docx")

        # ✅ PROCESAR IMÁGENES
        lista_imagenes = []

        if imagenes:
            for img in imagenes:
                image = InlineImage(doc, img, width=Mm(120))  # ajustar tamaño
                lista_imagenes.append(image)

            # ✅ Unir con salto de línea (una debajo de otra)
            imagenes_render = "\n".join(["{{imagen_item}}"] * len(lista_imagenes))
        else:
            lista_imagenes = []
            imagenes_render = ""

        # ✅ CONTEXTO
        context = {
            "helppeople": helppeople,
            "iniciativa": iniciativa,
            "fecha": fecha_str,
            "usuario": usuario,
            "unidad": unidad,
            "objetivo": objetivo,
            "problema": problema,
            "detalle": detalle,
            "nombre_usuario": nombre_usuario,
            "gerente": gerente,
            "imagen": lista_imagenes if lista_imagenes else ""
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
