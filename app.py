import streamlit as st
from docxtpl import DocxTemplate
from datetime import datetime

st.set_page_config(page_title="Generador BRIEF", layout="centered")

st.title("📄 Generador de BRIEF")

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

if st.button("🚀 Generar BRIEF"):
    if not all([helppeople, iniciativa, usuario, unidad, objetivo, problema, detalle, nombre_usuario, gerente]):
        st.error("⚠️ Completa todos los campos obligatorios (*)")
    else:
        doc = DocxTemplate("template_brief.docx")
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
            "gerente": gerente
        }
        doc.render(context)

        nombre_archivo = f"BRIEF_{helppeople}.docx"
        doc.save(nombre_archivo)

        with open(nombre_archivo, "rb") as file:
            st.download_button("📥 Descargar BRIEF", file, file_name=nombre_archivo)

        st.success("✅ BRIEF generado correctamente")
