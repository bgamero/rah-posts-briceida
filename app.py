import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps
import io
import os

# --- 1. CONFIGURACIÓN ---
CANVAS_SIZE = (1080, 1350)

def cargar_fuente(nombre, tamano):
    if os.path.exists(nombre):
        try: return ImageFont.truetype(nombre, tamano)
        except: return ImageFont.load_default()
    return ImageFont.load_default()

# --- 2. CARGA DE ACTIVOS AL INICIO (Blindado estilo Story v1.18) ---
try:
    plantilla_trans = Image.open("plantilla.png").convert("RGBA").resize(CANVAS_SIZE)
    logo_rah = Image.open("logo.png").convert("RGBA")
    
    icon_hab = Image.open("icono_hab.png").convert("RGBA")
    path_ban = "icono_baño.png" if os.path.exists("icono_baño.png") else "icono_banos.png"
    icon_ban = Image.open(path_ban).convert("RGBA")
    icon_mts = Image.open("icono_mts.png").convert("RGBA")
    icon_est = Image.open("icono_estac.png").convert("RGBA")
except Exception as e:
    st.error(f"❌ Error crítico cargando archivos base. Verifica los nombres en la carpeta INMOBILIARIA. Detalle: {e}")
    st.stop()

# --- 3. INTERFAZ ---
st.set_page_config(layout="wide", page_title="RAH POST v1.43b")
st.title("📸 Briceida RAH - POST v1.43b (Blindado Final)")

with st.sidebar:
    st.header("📝 Datos del Post")
    urb = st.text_input("Urbanización", "NOMBRE URB.").upper()
    op = st.selectbox("Operación", ["VENTA", "ALQUILER"])
    precio_raw = st.text_input("Precio ($)", "")
    
    st.subheader("📊 Detalles Técnicos")
    mts_v = st.text_input("Metraje (solo números)", "")
    hab_v = st.text_input("Habitaciones (solo números)", "")
    ban_v = st.text_input("Baños (solo números)", "")
    est_v = st.text_input("Estac. (solo números)", "")

# Subida de fotos
f_p = st.file_uploader("Fachada", type=['png', 'jpg', 'jpeg'])
c1, c2, c3, c4 = st.columns(4)
file1 = c1.file_uploader("Int 1", type=['png', 'jpg', 'jpeg'])
file2 = c2.file_uploader("Int 2", type=['png', 'jpg', 'jpeg'])
file3 = c3.file_uploader("Int 3", type=['png', 'jpg', 'jpeg'])
file4 = c4.file_uploader("Int 4", type=['png', 'jpg', 'jpeg'])

if st.button("✨ GENERAR POST"):
    # PASO 1: LIENZO Y FOTOS AL FONDO
    canvas = Image.new('RGBA', CANVAS_SIZE, (255, 255, 255, 255))
    draw_borders = ImageDraw.Draw(canvas) # Para los bordes negros

    def paste_with_border(target, f, x, y, w, h):
        if f:
            img = Image.open(f).convert("RGBA")
            target.paste(ImageOps.fit(img, (int(w), int(h))), (int(x), int(y)))
            # Dibujar borde negro delgado (lo que te gustó)
            draw_borders.rectangle([int(x), int(y), int(x)+int(w), int(y)+int(h)], outline="black", width=1)

    # Pegamos fachada al fondo (sin borde)
    if f_p:
        f_img = Image.open(f_p).convert("RGBA")
        canvas.paste(ImageOps.fit(f_img, (1108, 1080)), (0, 0))

    # Pegamos las 4 pequeñas CON borde negro (Y exactas Briceida)
    y_f = [32.4, 304.8, 577.2, 849.6]
    for idx, f_file in enumerate([file1, file2, file3, file4]):
        if f_file:
            paste_with_border(canvas, f_file, 64.1, y_f[idx], 230, 230)

    # PASO 2: LA PLANTILLA TRANSPARENTE (Tus marcos rojos y datos)
    canvas.paste(plantilla_trans, (0, 0), plantilla_trans)

    # PASO 3: DIBUJAR TEXTOS E ICONOS (CAPA FINAL - ENCIMA DE TODO)
    draw = ImageDraw.Draw(canvas)
    f_urb = cargar_fuente("Montserrat-Bold.ttf", 42)
    f_op = cargar_fuente("Montserrat-Bold.ttf", 52) # Operación grande
    f_pr = cargar_fuente("Montserrat-Bold.ttf", 55) # Precio grande
    f_det = cargar_fuente("Montserrat-Bold.ttf", 35)

    # Formatear Precio
    try:
        p_limpio = precio_raw.replace('.','').replace(',','').replace('$','').strip()
        precio_f = f"${int(p_limpio):,}".replace(",", ".")
    except:
        precio_f = f"${precio_raw}" if precio_raw else ""

    # Dibujar Textos Principales (Margen Derecho 1000)
    for txt_main, y_coord, font_main in [(urb, 601, f_urb), (op, 675, f_op), (precio_f, 807, f_pr)]:
        if txt_main:
            w_txt = draw.textbbox((0, 0), txt_main, font=font_main)[2]
            draw.text((1000 - w_txt, y_coord), txt_main, font=font_main, fill="white")

    # DIBUJAR ICONOS (Modo Seguro v1.39)
    y_ic = 1120
    # Nombres de variables ultra-específicos para evitar Shadowing (Miedo de Claude)
    icon_list_expert = [
        (icon_mts, mts_v, "m²", 60),
        (icon_hab, hab_v, "Hab", 310),
        (icon_ban, ban_v, "Baños", 560),
        (icon_est, est_v, "Est.", 810)
    ]

    for ico_img, val_in, tag_txt, x_pos_ico in icon_list_expert:
        if val_in: # Si escribiste algo en el sidebar
            # Redimensionar icono original (60x60)
            ico_resized = ico_img.resize((60, 60), Image.Resampling.LANCZOS)
            # Pegar directo usando el icono como su propia máscara (Estilo Story v1.18)
            # Esto asume que tus iconos YA son blancos y con transparencia, como en el Story.
            canvas.paste(ico_resized, (x_pos_ico, y_ic), ico_resized)
            # Dibujar Texto del Valor
            draw.text((x_pos_ico + 75, y_ic + 10), f"{val_in} {tag_txt}", font=f_det, fill="white")

    # LOGO RAH FINAL (X=779.7;Y=924.5;W=252.3;H=151.4)
    logo_f = ImageOps.contain(logo_rah, (252, 151))
    canvas.paste(logo_f, (780, 925), logo_f)

    # MOSTRAR Y DESCARGAR
    st.image(canvas, use_container_width=True)
    buf = io.BytesIO()
    canvas.convert("RGB").save(buf, format="PNG")
    st.download_button("⬇️ DESCARGAR POST COMPLETO", buf.getvalue(), f"post_{urb}.png", "image/png")