import streamlit as st
from PIL import Image, ImageDraw, ImageFont

# Configuración
st.set_page_config(page_title="Briceida RAH - Generador Pro", layout="wide")
st.title("🏠 Briceida RAH - Creador de Contenido")

# --- MENÚ LATERAL ---
st.sidebar.header("Configuración")
formato = st.sidebar.radio("¿Qué quieres crear hoy?", ["Post (Cuadrado)", "Story (Vertical)"])

# --- COORDENADAS SEGÚN FORMATO ---
if formato == "Post (Cuadrado)":
    archivo_plantilla = "plantilla.png"
    size_final = (1080, 1080)
    coord_principal = (0, 0)
    # Coordenadas de las 4 fotos pequeñas (Post)
    coords_internas = [(725, 50), (725, 305), (725, 555), (725, 810)] 
    size_internas = (310, 240)
    cant_internas = 4
    # Textos
    coord_urb = (360, 785)
    coord_precio = (360, 885)
    coords_iconos = [(130, 985), (280, 985), (430, 985), (580, 985)]
else:
    archivo_plantilla = "story.png"
    size_final = (1080, 1920)
    coord_principal = (0, 350)
    # Coordenadas de las 3 fotos pequeñas (Story)
    coords_internas = [(65, 1680), (395, 1680), (725, 1680)]
    size_internas = (290, 200)
    cant_internas = 3
    # Textos
    coord_urb = (540, 1300)
    coord_precio = (540, 1420)
    coords_iconos = [(200, 1550), (420, 1550), (650, 1550), (880, 1550)]

# --- ENTRADA DE DATOS ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("🖼️ Fotos")
    foto_fachada = st.file_uploader("Foto Principal (Fachada)", type=["jpg", "png", "jpeg"])
    fotos_in = []
    for i in range(cant_internas):
        fotos_in.append(st.file_uploader(f"Foto Interna {i+1}", type=["jpg", "png", "jpeg"], key=f"in_{i}"))

with col2:
    st.subheader("📝 Datos")
    urbanizacion = st.text_input("Urbanización / Sector", "EL PARRAL")
    precio = st.text_input("Precio", "$ 55.000")
    c1, c2 = st.columns(2)
    mts = c1.text_input("Mts²", "120")
    hab = c2.text_input("Hab", "3")
    ban = c1.text_input("Baños", "2")
    est = c2.text_input("Puestos", "2")

if st.button(f"🚀 GENERAR {formato.upper()}"):
    if foto_fachada:
        # Cargar base
        base = Image.open(archivo_plantilla).convert("RGBA")
        final = Image.new("RGBA", size_final, (255, 255, 255, 255))
        
        # 1. Pegar Fachada
        fachada = Image.open(foto_fachada).convert("RGBA")
        if formato == "Post (Cuadrado)":
            fachada = fachada.resize((720, 720))
        else:
            fachada = fachada.resize((1080, 950))
        final.paste(fachada, coord_principal, fachada)
        
        # 2. Pegar Fotos Internas
        for i in range(cant_internas):
            if fotos_in[i]:
                img_temp = Image.open(fotos_in[i]).convert("RGBA").resize(size_internas)
                final.paste(img_temp, coords_internas[i], img_temp)
        
        # 3. Pegar Plantilla (encima de las fotos)
        final.paste(base, (0, 0), base)
        
        # 4. Textos
        draw = ImageDraw.Draw(final)
        try:
            f_bold = ImageFont.truetype("Montserrat-Bold.ttf", 60)
            f_detalles = ImageFont.truetype("Montserrat-Bold.ttf", 35)
        except:
            f_bold = ImageFont.load_default()
            f_detalles = ImageFont.load_default()
            
        draw.text(coord_urb, urbanizacion.upper(), font=f_bold, fill="white", anchor="mm")
        draw.text(coord_precio, precio, font=f_bold, fill="#FFD700", anchor="mm")
        
        detalles = [mts, hab, ban, est]
        for i, texto in enumerate(detalles):
            draw.text(coords_iconos[i], texto, font=f_detalles, fill="white", anchor="mm")
            
        st.image(final)
        final.convert("RGB").save("resultado.jpg")
        with open("resultado.jpg", "rb") as f:
            st.download_button("📥 Descargar", f, f"{formato}.jpg", "image/jpeg")
    else:
        st.error("Sube al menos la foto principal.")
