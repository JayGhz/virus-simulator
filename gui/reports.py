import random
import dearpygui.dearpygui as dpg
import pandas as pd
from fpdf import FPDF
import graphviz
import os

class VirusSimulationReport:
    def __init__(self, G):
        self.G = G
        self.infected_nodes = set()
        self.propagation_log = []
        self.total_nodes = len(G.nodes)
        self.step_count = 0

    def propagate_infection(self, min_probability=0.05):
        new_infected = set()

        for node in list(self.infected_nodes):
            neighbors = list(self.G.neighbors(node))

            for neighbor in neighbors:
                if neighbor not in self.infected_nodes and neighbor not in new_infected:
                    weight = self.G[node][neighbor].get("weight", 0.1)
                    infection_probability = max(weight, min_probability)

                    if random.random() < infection_probability:
                        new_infected.add(neighbor)

        if new_infected:
            self.infected_nodes.update(new_infected)
            self.step_count += 1
            self.propagation_log.append({
                "step": self.step_count,
                "new_infected": len(new_infected),
                "total_infected": len(self.infected_nodes),
                "percent_infected": len(self.infected_nodes) / self.total_nodes * 100
            })
            print(f"Paso {self.step_count}: {len(self.infected_nodes)} infectados.")
        return bool(new_infected)

    def start_simulation(self, initial_nodes=None):
        if initial_nodes is None:
            initial_nodes = [1]  # Nodo inicial por defecto

        self.infected_nodes.clear()
        self.infected_nodes.update(initial_nodes)
        self.step_count = 0
        self.propagation_log = []

        print(f"Nodo(s) inicial(es): {initial_nodes}")

        while len(self.infected_nodes) < self.total_nodes:
            if not self.propagate_infection(min_probability=0.05):
                print("Propagación detenida: no hay más infecciones.")
                break

    def generate_pdf_report(self, filename="virus_propagation_report.pdf"):
        # Crear carpeta de salida si no existe
        output_folder = "output"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        filepath = os.path.join(output_folder, filename)

        df = pd.DataFrame(self.propagation_log)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="Reporte de Propagación del Virus", ln=True, align="C")
        pdf.cell(200, 10, txt=f"Pasos Totales de Infección: {self.step_count}", ln=True, align="L")

        # Agregar tabla de pasos de infección
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

        # Añadir tasa de probabilidad promedio de contagio
        avg_probability = self.calculate_avg_probability()
        pdf.ln(10)
        pdf.cell(200, 10, f"Tasa Promedio de Probabilidad de Contagio: {avg_probability:.2f}", ln=True, align="L")

        # Mostrar el número de nodos en el grafo cargado
        pdf.cell(200, 10, f"Número de Nodos en el Grafo Cargado: {self.total_nodes}", ln=True, align="L")

        # Añadir imagen del subgrafo del nodo más importante en una página completa
        important_node = 0  # Usamos el nodo 0 como el nodo más importante
        self.add_graph_image(pdf, important_node, output_folder)

        pdf.output(filepath)
        print(f"Reporte PDF guardado como {filepath}")

    def add_graph_image(self, pdf, node, output_folder):
        # Generamos el subgrafo en base al nodo más importante
        graph = self.generate_subgraph(node)
        filename = f"subgraph_{node}.png"

        filepath = os.path.join(output_folder, filename)

        # Generar y guardar la imagen del subgrafo
        graph.render(filepath, format='png', cleanup=True)

        # Eliminar extensiones redundantes si se generan automáticamente
        if os.path.exists(filepath + ".png"):
            os.rename(filepath + ".png", filepath)

        # Añadir título y luego la imagen en una página completa
        if os.path.exists(filepath):
            pdf.add_page()  # Nueva página para la imagen
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Subgrafo del Nodo Más Importante (Nodo {node})", ln=True, align="C")
            pdf.image(filepath, x=10, y=30, w=190)  # Ajustar la imagen para ocupar la página
        else:
            print(f"Error: La imagen no fue generada en {filepath}")



    def generate_subgraph(self, node, max_connections=350):
        graph = graphviz.Graph(format='png', engine='fdp')
        graph.attr(dpi='300', bgcolor='white', layout='fdp', size='10,10', nodesep='0.5', width='10', height='10')

        nodes_to_include = set([node])
        edges_to_include = []

        for neighbor in self.G.neighbors(node):
            nodes_to_include.add(neighbor)
            for neighbor_of_neighbor in self.G.neighbors(neighbor):
                if neighbor_of_neighbor in nodes_to_include:
                    edges_to_include.append((neighbor, neighbor_of_neighbor))
                    if len(edges_to_include) >= max_connections:
                        break
            if len(edges_to_include) >= max_connections:
                break

        for u, v in edges_to_include:
            if u in nodes_to_include and v in nodes_to_include:
                weight = self.G[u][v].get("weight", 0.1)
                graph.node(str(u), color='orange', style='solid', fontcolor='black', shape='circle', width='0.3', fontsize='6')
                graph.node(str(v), color='orange', style='solid', fontcolor='black', shape='circle', width='0.3', fontsize='6')
                graph.edge(str(u), str(v), color='black', penwidth='0.5', label=f"{weight:.2f}", fontsize='6')

        return graph

    def calculate_avg_probability(self):
        total_probability = 0
        total_edges = 0

        for u, v, data in self.G.edges(data=True):
            weight = data.get("weight", 0.1)
            total_probability += weight
            total_edges += 1

        if total_edges > 0:
            return total_probability / total_edges
        return 0

    def generate_report(self):
        self.start_simulation(initial_nodes=[1])
        self.generate_pdf_report("virus_propagation_report.pdf")
        dpg.configure_item("messagebox", label="¡Reporte Generado!", description="El reporte PDF se ha guardado correctamente.")
        dpg.show_item("messagebox")
