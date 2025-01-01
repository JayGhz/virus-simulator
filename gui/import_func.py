import tkinter as tk
from tkinter import messagebox, filedialog


def importar_csv(frame, volver_funcion):
    for widget in frame.winfo_children():
        widget.destroy()

    title_label = tk.Label(
        frame,
        text="Importar Archivo CSV",
        font=("Segoe UI", 24, "bold"),
        bg="#34495e",
        fg="#ecf0f1",
    )
    title_label.pack(pady=20)

    # Función para seleccionar archivo
    def seleccionar_archivo():
        archivo_seleccionado = filedialog.askopenfilename(
            filetypes=[("Archivos CSV", "*.csv")]
        )
        if archivo_seleccionado:
            messagebox.showinfo(
                "Archivo Seleccionado",
                f"Se ha seleccionado el archivo: {archivo_seleccionado}",
            )

    def usar_archivo_predeterminado():
        archivo_predeterminado = "/output/data/facebook_connections.csv"
        messagebox.showinfo(
            "Archivo Predeterminado", f"Usando el archivo: {archivo_predeterminado}"
        )

    btn_seleccionar = tk.Button(
        frame,
        text="Seleccionar Archivo",
        width=25,
        height=2,
        bg="#5d6d7e",
        fg="white",
        font=("Segoe UI", 12),
        relief="flat",
        command=seleccionar_archivo,
    )
    btn_seleccionar.pack(pady=20)
    btn_seleccionar.config(highlightbackground="#5d6d7e", highlightthickness=2)

    btn_predeterminado = tk.Button(
        frame,
        text="Usar Archivo Predeterminado",
        width=25,
        height=2,
        bg="#5d6d7e",
        fg="white",
        font=("Segoe UI", 12),
        relief="flat",
        command=usar_archivo_predeterminado,
    )
    btn_predeterminado.pack(pady=20)
    btn_predeterminado.config(highlightbackground="#5d6d7e", highlightthickness=2)

    btn_volver = tk.Button(
        frame,
        text="Volver",
        width=25,
        height=2,
        bg="#5d6d7e",
        fg="white",
        font=("Segoe UI", 12),
        relief="flat",
        command=volver_funcion,
    )
    btn_volver.pack(pady=20)
    btn_volver.config(highlightbackground="#5d6d7e", highlightthickness=2)

    for button in [btn_seleccionar, btn_predeterminado, btn_volver]:
        button.config(activebackground="#4b5d6b", activeforeground="white")
        button.bind("<Enter>", lambda event, b=button: b.config(bg="#4b5d6b"))
        button.bind(
            "<Leave>",
            lambda event, b=button: b.config(bg=b.cget("highlightbackground")),
        )
