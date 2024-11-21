import tkinter as tk
from tkinter import messagebox
import threading
import cv2
import networkx as nx
from PIL import Image, ImageTk
from gui.import_func import importar_csv
from gui.simulation import run_dearpygui as run_dearpygui_sim
from gui.key_nodes import run_dearpygui as run_dearpygui_key_nodes
from gui.simulation import load_graph_from_custom_csv
from gui.reports import VirusSimulationReport

# Crear el grafo G para pasar a VirusSimulationReport
G = load_graph_from_custom_csv("output/data/facebook_connections.csv")
report_instance = VirusSimulationReport(G)

# Función para ejecutar la simulación a través de DearPyGUI en un hilo separado
def iniciar_simulacion():
    print("Iniciando simulación...")
    thread = threading.Thread(target=run_dearpygui_sim)
    thread.start()

# Función para visualizar los nodos clave a través de DearPyGUI
def ver_grafo():
    print("Visualizando nodos clave...")
    thread = threading.Thread(target=run_dearpygui_key_nodes)
    thread.start()

# Función para generar reportes
def generar_reportes():
    report_instance.start_simulation()  # Inicia la simulación antes de generar el reporte
    report_instance.generate_pdf_report("virus_propagation_report.pdf")
    messagebox.showinfo("Reportes Generados", "El reporte CSV y PDF se han guardado correctamente.")

# Función para importar CSV
def importar_csv_opcion():
    importar_csv(frame, volver_al_menu_principal)

# Función para actualizar el marco de video
def update_video_frame():
    ret, frame = cap.read()
    if ret:
        frame_resized = cv2.resize(frame, (canvas.winfo_width(), canvas.winfo_height()))
        frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        img_tk = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, image=img_tk, anchor="nw")
        canvas.img_tk = img_tk
    canvas.after(10, update_video_frame)

# Crear la interfaz principal
def crear_menu():
    root = tk.Tk()
    root.title("Simulación de Propagación de Virus")
    root.geometry("800x600")  
    root.config(bg="#34495e") 

    global canvas
    canvas = tk.Canvas(root, width=800, height=600)
    canvas.pack(fill="both", expand=True)

    global cap
    cap = cv2.VideoCapture("assets/background.mp4") 
    update_video_frame()

    global frame
    frame = tk.Frame(root, bg="#34495e", bd=10)  
    frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=450) 

    actualizar_menu()

    root.mainloop()

# Actualizar el menú principal
def actualizar_menu():
    def on_enter(event, button):
        button.config(bg="#4b5d6b", fg="white")  

    def on_leave(event, button):
        button.config(bg="#5d6d7e", fg="white")  

    for widget in frame.winfo_children():
        widget.destroy()

    title_label = tk.Label(frame, text="Virus Prop. Simulator", font=("Segoe UI", 24, "bold"), fg="#ecf0f1", bg="#34495e")
    title_label.pack(pady=20)


    buttons = [
        ("Iniciar Simulación", iniciar_simulacion),
        ("Nodos clave", ver_grafo),
        ("Generar Reportes", generar_reportes),
        ("Importar CSV", importar_csv_opcion),
    ]


    for text, command in buttons:
        button = tk.Button(
            frame,
            text=text,
            width=25,
            height=2,
            bg="#5d6d7e",
            fg="white",
            font=("Segoe UI", 12),
            relief="flat",
            bd=2,
            command=command
        )
        button.pack(pady=10)

        button.bind("<Enter>", lambda event, b=button: on_enter(event, b))
        button.bind("<Leave>", lambda event, b=button: on_leave(event, b))


# Función para volver al menú principal
def volver_al_menu_principal():
    actualizar_menu()
