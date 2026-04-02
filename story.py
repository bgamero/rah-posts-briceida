import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps
import io
import os

# --- 1. CONFIGURACIÓN ---
CANVAS_SIZE = (1080, 1920)

# --- 2. CARGA DE FUENTES ---
def cargar_fuente(nombre, tamano):
    rutas = [
        nombre,                                      
        os.path.join("Open_Sans", nombre),           
        os.path.join("Open_Sans", "static", nombre)  
    ]
    for ruta in rutas:
        if os.path.exists(ruta):
            try:
                return ImageFont.truetype(ruta, tamano)
            except:
                continue
    if os.path.exists("Montserrat-Bold.ttf"):
        return ImageFont.truetype("Montserrat-Bold.ttf", tamano)
    return ImageFont.load_default()

try:
    plantilla_story = Image.open("story.png").convert("RGBA").resize(CANVAS_SIZE)
    logo_rah = Image.open("logo.png").convert("RGBA")
    icon_hab = Image.open("icono_hab.png").convert("RGBA")
    icon_ban = Image.open("icono_baño.png").convert("RGBA")
    icon_mts = Image.open("icono_mts.png").convert("RGBA")
    icon_est = Image.open("icono_estac.png").convert("RGBA")
except FileNotFoundError as e:
    st.error(f"❌ No encuentro el archivo: {e.filename}")
    st.stop()

# --- 3. INTERFAZ ---
st.set_page_config(page_title="RAH Story Master v1.18", layout="wide")
st.title("📸 Generador de Stories RAH - v1.18 Master")

with st.sidebar:
    st.header("📝 Datos del Inmueble")
    zona = st.text_input("Urbanización", "NOMBRE URB.").upper()
    op = st.selectbox("Operación", ["VENTA", "ALQUILER"])
    precio_raw = st.text_input("Precio ($)", "0")
    
    st.subheader("📊 Detalles Técnicos")
    mts_v = st.text_input("Metraje", "0")
    hab_v = st.text_input("Habitaciones", "0")
    ban_v = st.text_input("Baños", "0")
    est_v = st.text_input("Garage", "0")

col1, col2, col3, col4 = st.columns(4)
f_p = col1.file_uploader("Fachada", type=['png', 'jpg', 'jpeg'])
f1 = col2.file_uploader("Interna 1", type=['png', 'jpg', 'jpeg'])
f2 = col3.file_uploader("Interna 2", type=['png', 'jpg', 'jpeg'])
f3 = col4.file_uploader("Interna 3", type=['png', 'jpg', 'jpeg'])

# --- 4. ENSAMBLADO ---
if st.button("✨ GENERAR STORY v1.18 FINAL"):
    if not (zona and f_p):
        st.warning("⚠️ Ingresa Urbanización y Fachada.")
        st.stop()

    canvas = plantilla_story.copy()
    overlay = Image.new('RGBA', CANVAS_SIZE, (0,0,0,0))
    draw_ov = ImageDraw.Draw(overlay)
    draw = ImageDraw.Draw(canvas)

    # Formatear precio con comas para miles
    try:
        # Limpiamos puntos o comas que el usuario haya puesto para re-formatear limpio
        limpio = precio_raw.replace(".", "").replace(",", "")
        precio_formateado = "{:,}".format(int(limpio))
    except:
        precio_formateado = precio_raw

    def paste_pro(target, file, x, y, w, h):
        if file is not None:
            img = Image.open(file).convert("RGBA")
            img = ImageOps.fit(img, (int(w), int(h)), centering=(0.5, 0.5))
            mask = Image.new('L', (int(w), int(h)), 0)
            ImageDraw.Draw(mask).rounded_rectangle((0, 0, int(w), int(h)), radius=30, fill=255)
            img.putalpha(mask)
            target.paste(img, (int(x), int(y)), img)

    # A) Fotos y Logo
    paste_pro(canvas, f1, 97.3, 1025.6, 265, 482.2)
    paste_pro(canvas, f2, 396.8, 1025.6, 265, 482.2)
    paste_pro(canvas, f3, 696.3, 1025.6, 265, 482.2)
    paste_pro(canvas, f_p, 0, 0, 1079, 973.6)
    
    logo_fixed = ImageOps.contain(logo_rah, (300, 150))
    lw, lh = logo_fixed.size
    canvas.paste(logo_fixed, (1079 - lw - 40, 973 - lh - 40), logo_fixed)

    # B) Franja Gris
    draw_ov.rectangle([141.5, 0, 141.5+432, 973.6], fill=(217, 217, 217, 128))
    canvas.alpha_composite(overlay)
    
    # C) TEXTOS - AJUSTE DE ALTURAS
    xc = 141.5 + (432 / 2) # Centro de la franja
    
    # 1. Urbanización
    draw.text((xc, 300), zona, font=cargar_fuente("Montserrat-Bold.ttf", 41), fill="black", anchor="mm")

    # 2. Operación
    draw.text((xc, 380), op, font=cargar_fuente("OpenSans-Bold.ttf", 51), fill="black", anchor="mm")

    # 3. Raya Negra (Más abajo: Y=430)
    draw.line([(170.7, 430), (170.7 + 342.6, 430)], fill="black", width=2)

    # 4. Precio (Más arriba: Y=530 y más grande: 51)
    draw.text((xc, 530), f"${precio_formateado}", font=cargar_fuente("Montserrat-Bold.ttf", 51), fill="black", anchor="mm")

    # D) ICONOS Y VALORES
    y_icons = 1630
    i_sz = (60, 60)
    f_det = cargar_fuente("Montserrat-Bold.ttf", 35)
    
    canvas.paste(icon_mts.resize(i_sz), (40, int(y_icons)), icon_mts.resize(i_sz))
    draw.text((105, int(y_icons)+10), f"{mts_v}m²", font=f_det, fill="white")
    
    canvas.paste(icon_hab.resize(i_sz), (290, int(y_icons)), icon_hab.resize(i_sz))
    draw.text((355, int(y_icons)+10), f"{hab_v} Hab", font=f_det, fill="white")
    
    canvas.paste(icon_ban.resize(i_sz), (560, int(y_icons)), icon_ban.resize(i_sz))
    draw.text((625, int(y_icons)+10), f"{ban_v} Baños", font=f_det, fill="white")
    
    canvas.paste(icon_est.resize(i_sz), (820, int(y_icons)), icon_est.resize(i_sz))
    draw.text((885, int(y_icons)+10), f"{est_v} Est.", font=f_det, fill="white")

    # --- MOSTRAR RESULTADO ---
    post_final = canvas.convert("RGB")
    st.image(post_final, use_container_width=True)
    buf = io.BytesIO()
    post_final.save(buf, format="PNG")
    st.download_button("⬇️ DESCARGAR STORY v1.18", buf.getvalue(), f"story_{zona}.png", "image/png")
