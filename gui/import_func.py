import tkinter as tk
from tkinter import messagebox, filedialog

def importar_csv(frame, volver_funcion):
    # Limpiar el frame de botones del menú principal
    for widget in frame.winfo_children():
        widget.destroy()

    # Título para la opción de importación
    title_label = tk.Label(frame, text="Importar Archivo CSV", font=("Segoe UI", 24, "bold"), bg="#34495e", fg="#ecf0f1")
    title_label.pack(pady=20)

    # Función para seleccionar archivo
    def seleccionar_archivo():
        archivo_seleccionado = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])
        if archivo_seleccionado:
            messagebox.showinfo("Archivo Seleccionado", f"Se ha seleccionado el archivo: {archivo_seleccionado}")

    # Función para usar el archivo predeterminado
    def usar_archivo_predeterminado():
        archivo_predeterminado = "/output/data/facebook_connections.csv"
        messagebox.showinfo("Archivo Predeterminado", f"Usando el archivo: {archivo_predeterminado}")

    # Botones para las opciones de importación con el mismo estilo que el menú principal
    btn_seleccionar = tk.Button(frame, text="Seleccionar Archivo", width=25, height=2, bg="#5d6d7e", fg="white",
                                font=("Segoe UI", 12), relief="flat", command=seleccionar_archivo)
    btn_seleccionar.pack(pady=20)
    btn_seleccionar.config(highlightbackground="#5d6d7e", highlightthickness=2)

    btn_predeterminado = tk.Button(frame, text="Usar Archivo Predeterminado", width=25, height=2, bg="#5d6d7e", fg="white",
                                   font=("Segoe UI", 12), relief="flat", command=usar_archivo_predeterminado)
    btn_predeterminado.pack(pady=20)
    btn_predeterminado.config(highlightbackground="#5d6d7e", highlightthickness=2)

    # Botón para volver al menú principal con el mismo estilo
    btn_volver = tk.Button(frame, text="Volver", width=25, height=2, bg="#5d6d7e", fg="white",
                           font=("Segoe UI", 12), relief="flat", command=volver_funcion)
    btn_volver.pack(pady=20)
    btn_volver.config(highlightbackground="#5d6d7e", highlightthickness=2)

    # Aplicar efecto de hover a todos los botones en el frame
    for button in [btn_seleccionar, btn_predeterminado, btn_volver]:
        button.config(activebackground="#4b5d6b", activeforeground="white")
        button.bind("<Enter>", lambda event, b=button: b.config(bg="#4b5d6b"))
        button.bind("<Leave>", lambda event, b=button: b.config(bg=b.cget("highlightbackground")))

