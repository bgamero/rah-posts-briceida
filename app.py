import streamlit as st
from PIL import Image, ImageDraw, ImageFont

# Configuración
st.set_page_config(page_title="Briceida RAH - Generador", layout="wide")

st.title("🏠 Briceida RAH - Creador de Contenido")

# --- MENÚ LATERAL ---
st.sidebar.header("Configuración")
formato = st.sidebar.radio("¿Qué quieres crear hoy?", ["Post (Cuadrado)", "Story (Vertical)"])

# Configuración según el formato elegido
if formato == "Post (Cuadrado)":
    archivo_plantilla = "plantilla.png"
    size_final = (1080, 1080)
    coord_foto = (0, 0) 
    coord_urb = (540, 785)
    coord_precio = (540, 885)
    # Coordenadas iconos (mts, hab, ban, est)
    coords_iconos = [(200, 985), (420, 985), (650, 985), (880, 985)]
else:
    archivo_plantilla = "story.png"
    size_final = (1080, 1920)
    coord_foto = (0, 350) # La foto empieza más abajo en Story
    coord_urb = (540, 1300)
    coord_precio = (540, 1420)
    coords_iconos = [(200, 1550), (420, 1550), (650, 1550), (880, 1550)]

# --- ENTRADA DE DATOS ---
col1, col2 = st.columns(2)
with col1:
    foto_casa = st.file_uploader("1. Subir foto de la casa", type=["jpg", "png", "jpeg"])
    urbanizacion = st.text_input("2. Urbanización / Sector", "EL PARRAL")
    precio = st.text_input("3. Precio", "$ 55.000")

with col2:
    st.write("4. Detalles de la propiedad:")
    c1, c2 = st.columns(2)
    mts = c1.text_input("Mts²", "120")
    hab = c2.text_input("Hab", "3")
    ban = c1.text_input("Baños", "2")
    est = c2.text_input("Puestos", "2")

if st.button(f"🚀 GENERAR {formato.upper()}"):
    if foto_casa:
        # Cargar imágenes
        base = Image.open(archivo_plantilla).convert("RGBA")
        casa = Image.open(foto_casa).convert("RGBA")
        
        # Redimensionar foto de la casa
        if formato == "Post (Cuadrado)":
            casa = casa.resize((1080, 720))
        else:
            casa = casa.resize((1080, 950))
            
        # Crear imagen final
        final = Image.new("RGBA", size_final, (255, 255, 255, 255))
        final.paste(casa, coord_foto, casa)
        final.paste(base, (0, 0), base)
        
        draw = ImageDraw.Draw(final)
        try:
            f_bold = ImageFont.truetype("Montserrat-Bold.ttf", 65)
            f_detalles = ImageFont.truetype("Montserrat-Bold.ttf", 40)
        except:
            f_bold = ImageFont.load_default()
            f_detalles = ImageFont.load_default()
            
        # Escribir textos principales
        draw.text(coord_urb, urbanizacion.upper(), font=f_bold, fill="white", anchor="mm")
        draw.text(coord_precio, precio, font=f_bold, fill="#FFD700", anchor="mm")
        
        # Escribir detalles al lado de los iconos
        detalles = [mts, hab, ban, est]
        for i, texto in enumerate(detalles):
            draw.text(coords_iconos[i], texto, font=f_detalles, fill="white", anchor="mm")
        
        st.image(final, caption="¡Listo! Revisa si todo quedó bien")
        
        # Descarga
        final.convert("RGB").save("resultado.jpg")
        with open("resultado.jpg", "rb") as f:
            st.download_button("📥 Descargar Imagen", f, f"RAH_{formato}.jpg", "image/jpeg")
    else:
        st.error("¡Falta la foto de la casa!")
