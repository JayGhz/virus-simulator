import dearpygui.dearpygui as dpg
import networkx as nx
import pandas as pd
import random
import threading
from collections import deque

infected_nodes = set()
node_ids = {}
node_positions = {}

def load_graph_from_custom_csv(file_path):
    global G
    try:
        df = pd.read_csv(file_path, header=None, index_col=False, on_bad_lines='skip')
    except Exception as e:
        print(f"Error al leer el archivo CSV: {e}")
        return None

    G = nx.Graph()
    for _, row in df.iterrows():
        node = int(row[0])
        connections = row[1:].dropna()
        for target in connections:
            try:
                target = int(target)
                G.add_edge(node, target, weight=random.random())
            except ValueError:
                print(f"Advertencia: Nodo inválido '{target}' en fila {node}, ignorando esta conexión.")
    return G

def draw_graph(G):
    layout = nx.spring_layout(G, k=0.25, scale=1.0)
    global node_positions
    node_positions = {node: (x * 300, y * 300) for node, (x, y) in layout.items()}

    offset_x, offset_y = 600, 400 

    # Dibujar las aristas
    for edge in G.edges:
        x1, y1 = node_positions[edge[0]]
        x2, y2 = node_positions[edge[1]]
        dpg.draw_line((x1 + offset_x, y1 + offset_y), (x2 + offset_x, y2 + offset_y), color=(250, 250, 250), parent="canvas")

    # Dibujar los nodos
    for node in G.nodes:
        x, y = node_positions[node]
        color = (60, 219, 65)
        border_color = (250, 250, 250)  
        
      
        dpg.draw_circle((x + offset_x, y + offset_y), 12, color=border_color, parent="canvas")

        node_id = dpg.draw_circle((x + offset_x, y + offset_y), 10, color=color, parent="canvas", fill=color)
        node_ids[node] = node_id

def update_infected_nodes(G):
    for node in infected_nodes:
        x, y = node_positions[node]
        if node in node_ids:
            dpg.delete_item(node_ids[node])
            node_ids[node] = dpg.draw_circle((x + 600, y + 400), 12, color=(150, 150, 150), parent="canvas")  # Borde
            node_ids[node] = dpg.draw_circle((x + 600, y + 400), 10, color=(190, 25, 25), parent="canvas", fill=(190, 25, 25))  # Nodo infectado

    dpg.set_value("infected_count", f"Nodos infectados: {len(infected_nodes)}")
    dpg.set_value("healthy_count", f"Nodos sanos: {len(G.nodes) - len(infected_nodes)}")

# Funcion de propagación de infección basado en el algoritmo BFS
def propagate_infection(G):
    new_infected = set()
    nodes_to_infect = deque(infected_nodes)
    min_probability = 0.1

    while nodes_to_infect:
        node = nodes_to_infect.popleft()
        for neighbor in G.neighbors(node):
            if neighbor not in infected_nodes and neighbor not in new_infected:
                weight = G[node][neighbor]["weight"]
                infection_probability = max(weight, min_probability)
                if random.random() < infection_probability:
                    new_infected.add(neighbor)
                    nodes_to_infect.append(neighbor)
                    print(f"Nodo infectado: {neighbor}")

    infected_nodes.update(new_infected)
    return bool(new_infected)

def start_simulation(G):
    infected_nodes.clear()
    infected_nodes.add(1)
    print("Paciente cero es el nodo: 1")

    def run_step():
        if propagate_infection(G):
            update_infected_nodes(G)
            threading.Timer(1.0, run_step).start()

    run_step()

def run_dearpygui():
    dpg.create_context()

    with dpg.window(label="Simulación de Propagación de Virus", width=1200, height=800):
        dpg.add_text("Nodos infectados: 0", tag="infected_count")
        dpg.add_text("Nodos sanos: 4000", tag="healthy_count")
        dpg.add_button(label="Iniciar Simulación", callback=lambda: start_simulation(G))
        dpg.add_spacer(height=10)
        
        dpg.add_drawlist(width=1000, height=900, tag="canvas")

    dpg.create_viewport(title='Virus Simulator', width=1200, height=800)
    dpg.setup_dearpygui()
    dpg.show_viewport()

    global G
    G = load_graph_from_custom_csv('output/data/facebook_connections.csv')
    draw_graph(G)  

    dpg.start_dearpygui()
    dpg.destroy_context()

