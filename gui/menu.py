import tkinter as tk
from tkinter import messagebox
import threading
import cv2
import networkx as nx
from PIL import Image, ImageTk
from gui.import_func import importar_csv
from gui.simulation import run_dearpygui as run_dearpygui_sim
from gui.key_nodes import run_dearpygui as run_dearpygui_key_nodes
from gui.reports import VirusSimulationReport

# Crear el grafo G para pasar a VirusSimulationReport
G = nx.erdos_renyi_graph(50, 0.1)  # Esto es un ejemplo; ajusta el grafo según tu simulación
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
    report_instance.generate_csv_report("virus_propagation_report.csv")
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
    for widget in frame.winfo_children():
        widget.destroy()

    title_label = tk.Label(frame, text="Virus Simulator", font=("Segoe UI", 24, "bold"), fg="#ecf0f1", bg="#34495e")
    title_label.pack(pady=20)

    start_button = tk.Button(frame, text="Iniciar Simulación", width=25, height=2, bg="#5d6d7e", fg="white", font=("Segoe UI", 12), relief="flat", bd=2, command=iniciar_simulacion)
    start_button.pack(pady=10)

    graph_button = tk.Button(frame, text="Nodos clave", width=25, height=2, bg="#5d6d7e", fg="white", font=("Segoe UI", 12), relief="flat", bd=2, command=ver_grafo)
    graph_button.pack(pady=10)

    report_button = tk.Button(frame, text="Generar Reportes", width=25, height=2, bg="#5d6d7e", fg="white", font=("Segoe UI", 12), relief="flat", bd=2, command=generar_reportes)
    report_button.pack(pady=10)

    import_button = tk.Button(frame, text="Importar CSV", width=25, height=2, bg="#5d6d7e", fg="white", font=("Segoe UI", 12), relief="flat", bd=2, command=importar_csv_opcion)
    import_button.pack(pady=10)

# Función para volver al menú principal
def volver_al_menu_principal():
    actualizar_menu()
