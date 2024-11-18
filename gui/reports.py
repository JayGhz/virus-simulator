import random
import dearpygui.dearpygui as dpg
from collections import deque
import pandas as pd
from fpdf import FPDF

class VirusSimulationReport:
    def __init__(self, G):
        self.G = G
        self.infected_nodes = set()
        self.propagation_log = []
        self.total_nodes = len(G.nodes)
        self.step_count = 0

    def propagate_infection(self, min_probability=0.2):  # Probabilidad mínima ajustada (más baja)
        new_infected = set()
        nodes_to_infect = deque(self.infected_nodes)

        while nodes_to_infect:
            node = nodes_to_infect.popleft()
            for neighbor in self.G.neighbors(node):
                if neighbor not in self.infected_nodes and neighbor not in new_infected:
                    weight = self.G[node][neighbor].get("weight", 0.1)  # Peso por defecto bajo para asegurar propagación
                    infection_probability = max(weight, min_probability)  # Asegura una probabilidad de infección
                    if random.random() < infection_probability:
                        new_infected.add(neighbor)
                        nodes_to_infect.append(neighbor)

        if new_infected:
            self.infected_nodes.update(new_infected)
            self.step_count += 1
            self.propagation_log.append({
                "step": self.step_count,
                "new_infected": len(new_infected),
                "total_infected": len(self.infected_nodes),
                "percent_infected": len(self.infected_nodes) / self.total_nodes * 100
            })

    def start_simulation(self, initial_nodes=None):
        if initial_nodes is None:
            initial_nodes = [1]  # Empezar con un nodo infectado
        self.infected_nodes.clear()
        self.infected_nodes.update(initial_nodes)
        self.step_count = 0
        self.propagation_log = []

        # Corre la simulación hasta que todos los nodos estén infectados
        while len(self.infected_nodes) < self.total_nodes:
            previous_infected_count = len(self.infected_nodes)
            self.propagate_infection(min_probability=0.2)  # Probabilidad mínima más baja
            if len(self.infected_nodes) == previous_infected_count:  # Detener cuando no haya más infección
                break

    def generate_csv_report(self, filename="virus_propagation_report.csv"):
        df = pd.DataFrame(self.propagation_log)
        df.to_csv(filename, index=False)
        print(f"Reporte CSV guardado como {filename}")

    def generate_pdf_report(self, filename="virus_propagation_report.pdf"):
        df = pd.DataFrame(self.propagation_log)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="Reporte de Propagación del Virus", ln=True, align="C")
        pdf.cell(200, 10, txt=f"Pasos Totales de Infección: {self.step_count}", ln=True, align="L")

        pdf.cell(40, 10, "Paso", border=1, align="C")
        pdf.cell(40, 10, "Infectados Nuevos", border=1, align="C")
        pdf.cell(40, 10, "Total Infectados", border=1, align="C")
        pdf.cell(60, 10, "Porcentaje Infectados", border=1, align="C")
        pdf.ln()

        for i, row in df.iterrows():
            pdf.cell(40, 10, str(row['step']), border=1, align="C")
            pdf.cell(40, 10, str(int(row['new_infected'])), border=1, align="C")
            pdf.cell(40, 10, str(int(row['total_infected'])), border=1, align="C")
            pdf.cell(60, 10, f"{row['percent_infected']:.2f}%", border=1, align="C")
            pdf.ln()

        pdf.output(filename)
        print(f"Reporte PDF guardado como {filename}")

    def generar_reportes(self):
        self.start_simulation(initial_nodes=[1, 2, 3])  # Empezar con 3 nodos infectados para acelerar
        self.generate_csv_report("virus_propagation_report.csv")
        self.generate_pdf_report("virus_propagation_report.pdf")
        # Mostrar mensaje de éxito
        dpg.configure_item("messagebox", label="¡Reporte Generado!", description="Los reportes CSV y PDF se han guardado correctamente.")
        dpg.show_item("messagebox")
