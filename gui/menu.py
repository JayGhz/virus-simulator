import tkinter as tk
import threading
import cv2
import gui.simulation as sim
from tkinter import messagebox
from PIL import Image, ImageTk
from gui.import_func import importar_csv

def run_dearpygui():
    sim.run_dearpygui()

# Funciones para las acciones del menú
def iniciar_simulacion():
    print("Iniciando simulación...")
    thread = threading.Thread(target=run_dearpygui)
    thread.start()

def ver_grafo():
    print("Visualizando grafo...")
    messagebox.showinfo("Grafo", "Mostrando el grafo de la persona")

def generar_reportes():
    print("Generando reportes...")
    messagebox.showinfo("Reportes", "Reportes generados")

def importar_csv_opcion():
    # Pasar el frame y la función de volver para actualizar la vista con los botones de importación CSV
    importar_csv(frame, volver_al_menu_principal)

# Función para actualizar el fondo del video
def update_video_frame():
    ret, frame = cap.read()
    if ret:
        # Convertir el frame a una imagen compatible con Tkinter
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        img_tk = ImageTk.PhotoImage(img)
        
        # Actualizar la imagen en el fondo del canvas
        canvas.create_image(0, 0, image=img_tk, anchor="nw")
        canvas.img_tk = img_tk  # Mantener una referencia a la imagen

    # Llamar a esta función nuevamente en 10ms
    canvas.after(10, update_video_frame)

# Crear la ventana principal del menú
def crear_menu():
    # Crear ventana principal
    root = tk.Tk()
    root.title("Simulación de Propagación de Virus")
    root.geometry("800x600")  # Tamaño de la ventana
    root.config(bg="#34495e")  # Fondo gris oscuro elegante

    # Crear un canvas para mostrar el fondo de video
    global canvas
    canvas = tk.Canvas(root, width=800, height=600)
    canvas.pack(fill="both", expand=True)

    # Cargar el video
    global cap
    cap = cv2.VideoCapture("assets/background.mp4") 

    # Comenzar a actualizar el video en el fondo
    update_video_frame()

    # Crear un Frame para los botones, para que estén centrados
    global frame
    frame = tk.Frame(root, bg="#34495e", bd=10)  # Se eliminó el borde extra
    frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=450) 

    # Llamar a la función para crear los botones del menú
    actualizar_menu()

    # Iniciar el loop de la interfaz gráfica
    root.mainloop()

# Función para actualizar el menú
def actualizar_menu():
    # Limpiar el frame de cualquier contenido previo
    for widget in frame.winfo_children():
        widget.destroy()

    # Título
    title_label = tk.Label(frame, text="Virus Simulator", font=("Segoe UI", 24, "bold"), fg="#ecf0f1", bg="#34495e")
    title_label.pack(pady=20)

    # Botón de inicio de simulación
    start_button = tk.Button(frame, text="Iniciar Simulación", width=25, height=2, bg="#5d6d7e", fg="white", font=("Segoe UI", 12), relief="flat", bd=2, command=iniciar_simulacion)
    start_button.pack(pady=10)
    start_button.config(highlightbackground="#5d6d7e", highlightthickness=2)

    # Botón para ver grafo
    graph_button = tk.Button(frame, text="Ver Grafo", width=25, height=2, bg="#5d6d7e", fg="white", font=("Segoe UI", 12), relief="flat", bd=2, command=ver_grafo)
    graph_button.pack(pady=10)
    graph_button.config(highlightbackground="#5d6d7e", highlightthickness=2)

    # Botón para generar reportes
    report_button = tk.Button(frame, text="Generar Reportes", width=25, height=2, bg="#5d6d7e", fg="white", font=("Segoe UI", 12), relief="flat", bd=2, command=generar_reportes)
    report_button.pack(pady=10)
    report_button.config(highlightbackground="#5d6d7e", highlightthickness=2)

    # Botón para importar CSV
    import_button = tk.Button(frame, text="Importar CSV", width=25, height=2, bg="#5d6d7e", fg="white", font=("Segoe UI", 12), relief="flat", bd=2, command=importar_csv_opcion)
    import_button.pack(pady=10)
    import_button.config(highlightbackground="#5d6d7e", highlightthickness=2)

    # Cambiar color al pasar el ratón (hover) a un gris más oscuro, sin blanco
    for button in frame.winfo_children():
        if isinstance(button, tk.Button):
            button.config(activebackground="#4b5d6b", activeforeground="white")
            button.bind("<Enter>", lambda event, b=button: b.config(bg="#4b5d6b"))
            button.bind("<Leave>", lambda event, b=button: b.config(bg=b.cget("highlightbackground")))

# Función para volver al menú principal
def volver_al_menu_principal():
    actualizar_menu()
