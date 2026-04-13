import tkinter as tk
from PIL import Image, ImageTk
import random
import time
import platform
import sys

# 👉 keyboard solo en Windows
if platform.system() == "Windows":
    import keyboard

ventana_anterior = ""
tiempo_ultimo_cambio = time.time()

# -------- FRASES --------
frases = {
    "inicio": ["¡BIENVENIDO AL INCREÍBLE CIRCO DIGITAL! 🎪"],

    "entretenido": ["Hmm… interesante 🍿","No puedes parar de ver eso 😏","Esto sí me entretiene","Curioso contenido…","Podría ver esto todo el día"],

    "dibujo": ["¡Arte en proceso! 🎨","Eso se ve bien","Me gusta tu estilo","Interesante trazo…","Sigue así, artista"],

    "juego": ["Ohhh… esto me interesa 🎮","¡Eso sí es acción!","No pierdas 😈","Vamos, puedes ganar","Esto se puso bueno"],

    "general": ["Curioso… 😏","Veamos qué haces ahora","Hmm… interesante","No esperaba eso","Sigue adelante…"],

    "aburrido": ["Esto es aburrido…","¿Sigues ahí?","Me estoy durmiendo…","Haz algo interesante…","Esto no me gusta nada"],

    "enojado": ["¡YA BASTA! 😡","¡Esto es desesperante!","¡Cambia algo YA!","¡Me estás aburriendo!","¡No puedo con esto!"]
}

# -------- IMÁGENES --------
imagenes = {
    "inicio": ["caine_inicio.png"],
    "feliz": ["caine_feliz1.png","caine_feliz2.png","caine_feliz3.png"],
    "enojado": ["caine_enojado1.png","caine_enojado2.png","caine_enojado3.png"],
    "dibujo": ["caine_dibujo1.png","caine_dibujo2.png","caine_dibujo3.png"],
    "interesado": ["caine_interesado1.png","caine_interesado2.png","caine_interesado3.png"],
    "entretenido": ["caine_entretenido1.png","caine_entretenido2.png","caine_entretenido3.png"],
    "aburrido": ["caine_aburrido1.png","caine_aburrido2.png","caine_aburrido3.png"],
    "dormido": ["caine_dormido.png"],
    "asustado": ["caine_asustado.png"]
}

# -------- DETECTAR VENTANA --------
def obtener_ventana():
    sistema = platform.system()

    if sistema == "Linux":
        try:
            import subprocess
            return subprocess.check_output(
                "xdotool getactivewindow getwindowname 2>/dev/null",
                shell=True
            ).decode().lower()
        except:
            return ""

    elif sistema == "Windows":
        try:
            import pygetwindow as gw
            w = gw.getActiveWindow()
            return w.title.lower() if w else ""
        except:
            return ""

    return ""

# -------- MOSTRAR CAINE --------
def mostrar_caine(texto, tipo):
    ventana = tk.Tk()
    ventana.overrideredirect(True)
    ventana.attributes("-topmost", True)

    img_path = random.choice(imagenes[tipo])
    img = Image.open(img_path).resize((250, 250))
    img = ImageTk.PhotoImage(img)

    label_img = tk.Label(ventana, image=img)
    label_img.image = img
    label_img.pack()

    tk.Label(ventana, text=texto, font=("Arial", 11)).pack()

    # 👉 clic para apagar (Linux seguro)
    ventana.bind("<Button-1>", lambda e: apagar())

    x = random.randint(0, 800)
    y = random.randint(0, 500)
    ventana.geometry(f"300x300+{x}+{y}")

    ventana.after(random.randint(6000, 10000), ventana.destroy)
    ventana.mainloop()

# -------- REACCIÓN --------
def reaccionar(nombre):
    if "youtube" in nombre:
        return random.choice(frases["entretenido"]), "entretenido"

    elif any(p in nombre for p in ["chrome", "firefox"]):
        return random.choice(frases["entretenido"]), "entretenido"

    elif any(p in nombre for p in ["krita", "ibis", "paint", "gimp"]):
        return random.choice(frases["dibujo"]), "dibujo"

    elif any(p in nombre for p in ["steam", "game"]):
        return random.choice(frases["juego"]), "interesado"

    else:
        return random.choice(frases["general"]), "feliz"

# -------- APAGADO --------
def apagar():
    mostrar_caine("...", "asustado")
    mostrar_caine("...Zzz...", "dormido")
    time.sleep(2)
    sys.exit()

# -------- INICIO --------
def mostrar_inicio():
    mostrar_caine(frases["inicio"][0], "inicio")

# -------- MONITOR --------
def monitor():
    global ventana_anterior, tiempo_ultimo_cambio

    mostrar_inicio()

    while True:

        # 👉 Windows ESC + 1
        if platform.system() == "Windows":
            try:
                if keyboard.is_pressed("esc") and keyboard.is_pressed("1"):
                    apagar()
            except:
                pass

        ventana_actual = obtener_ventana()

        if ventana_actual != "" and ventana_actual != ventana_anterior:
            texto, tipo = reaccionar(ventana_actual)

            # 🔥 SIN THREADS
            mostrar_caine(texto, tipo)

            ventana_anterior = ventana_actual
            tiempo_ultimo_cambio = time.time()

        tiempo_sin_cambio = time.time() - tiempo_ultimo_cambio

        if tiempo_sin_cambio > 60:
            tipo = "aburrido"
            if tiempo_sin_cambio > 120:
                tipo = "enojado"

            mostrar_caine(random.choice(frases[tipo]), tipo)

            tiempo_ultimo_cambio = time.time()

        time.sleep(1)

# -------- START --------
monitor()