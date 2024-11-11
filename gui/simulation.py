import dearpygui.dearpygui as dpg
import networkx as nx
import pandas as pd
import random
import threading
from collections import deque

# Este conjunto de nodos infectados se mantendrá durante toda la simulación
infected_nodes = set()
node_ids = {}

def load_graph_from_custom_csv(file_path):
    # Intentar leer el archivo ignorando filas problemáticas usando on_bad_lines
    try:
        df = pd.read_csv(file_path, index_col=0, header=None, on_bad_lines='skip', usecols=range(10), nrows=10)
    except Exception as e:
        print(f"Error al leer el archivo CSV: {e}")
        return None

    G = nx.Graph()

    # Iteramos sobre cada fila, donde el índice es el nodo principal y las columnas son los vecinos
    for node, connections in df.iterrows():
        for target in connections.dropna():  # Ignorar valores NaN
            try:
                G.add_edge(int(node), int(target), weight=random.random())
            except ValueError:
                print(f"Advertencia: Nodo inválido '{target}' en fila {node}, ignorando esta conexión.")
    
    return G


# Función para dibujar el grafo completo (nodos y aristas)
def draw_graph(G):
    layout = nx.spring_layout(G, k=0.25, scale=1.0)

    # Guardar las posiciones de los nodos para mantenerlas constantes
    node_positions = {node: (x * 300, y * 300) for node, (x, y) in layout.items()}

    # Dibujar las aristas solo una vez al inicio
    for edge in G.edges:
        x1, y1 = node_positions[edge[0]]
        x2, y2 = node_positions[edge[1]]
        dpg.draw_line((x1 + 400, y1 + 400), (x2 + 400, y2 + 400), color=(200, 200, 200), parent="canvas")

    # Dibujar los nodos con un color verde inicial
    for node in G.nodes:
        x, y = node_positions[node]
        color = (0, 255, 0)  # Verde para los nodos no infectados
        node_id = dpg.draw_circle((x + 400, y + 400), 10, color=color, parent="canvas", fill=color)
        node_ids[node] = node_id  # Guardamos la referencia del nodo

    return node_positions  # Devolvemos las posiciones para usarlas más tarde

# Función para actualizar solo los nodos infectados
def update_infected_nodes(G, node_positions):
    for node in G.nodes:
        x, y = node_positions[node]
        color = (255, 0, 0) if node in infected_nodes else (0, 255, 0)  # Rojo para infectados, verde para no infectados

        # Solo actualizamos los nodos infectados
        if node in infected_nodes:
            if node in node_ids:
                # Borramos el nodo anterior si existe y lo redibujamos
                dpg.delete_item(node_ids[node])

            # Dibujar el nodo actualizado (infectado)
            node_ids[node] = dpg.draw_circle((x + 400, y + 400), 10, color=color, parent="canvas", fill=color)

# Propagar infección con probabilidades (esto se hace paso a paso, y la infección se propaga por todo el grafo)
def propagate_infection(G, infected_nodes):
    new_infected = set()  # Nuevos nodos infectados en cada paso
    nodes_to_infect = deque(infected_nodes)  # Usamos una cola para BFS (propagación en cascada)

    # Probabilidad mínima de contagio
    min_probability = 0.1

    # Mientras haya nodos infectados por procesar
    while nodes_to_infect:
        node = nodes_to_infect.popleft()
        print(f"Procesando nodo: {node}, vecinos: {list(G.neighbors(node))}")  # Diagnóstico de vecinos

        # Propagar infección a los vecinos del nodo actual
        for neighbor in G.neighbors(node):
            # Aseguramos que no se infecten nodos ya infectados
            if neighbor not in infected_nodes and neighbor not in new_infected:
                weight = G[node][neighbor]["weight"]
                infection_probability = max(weight, min_probability)  # Usamos la mayor de las dos probabilidades

                if random.random() < infection_probability:  # Si pasa la probabilidad, el vecino se infecta
                    new_infected.add(neighbor)
                    nodes_to_infect.append(neighbor)  # Agregamos al vecino a la cola para que se propague

    # Actualizamos los nodos infectados solo con los nuevos infectados
    infected_nodes.update(new_infected)
    print(f"Nuevos infectados: {new_infected}")
    
    return bool(new_infected)  # Devuelve True si hubo nuevos infectados, False si no

# Función para iniciar la simulación (sin necesidad de un botón)
def start_simulation():
    global infected_nodes
    infected_nodes = {0}  # Empezamos con el nodo 2 como infectado

    # Cargamos el grafo una sola vez
    G = load_graph_from_custom_csv('output/data/facebook_connections.csv')

    # Dibuja el grafo solo al principio y obtiene las posiciones
    node_positions = draw_graph(G)

    # Función para avanzar un paso en la simulación
    def run_step():
        nonlocal G, node_positions
        if propagate_infection(G, infected_nodes):  # Solo continuar si hay nuevos infectados
            update_infected_nodes(G, node_positions)  # Solo actualizar los nodos infectados
            threading.Timer(1.0, run_step).start()  # Llamar a run_step después de 1 segundo (1000 ms)

    run_step()  # Comienza la propagación

# Función para ejecutar DearPyGUI
def run_dearpygui():
    dpg.create_context()

    # Ventana principal sin botón, la simulación inicia automáticamente
    with dpg.window(label="Simulación de Propagación de Virus", width=800, height=800):
        dpg.add_drawlist(width=800, height=800, tag="canvas")

    # Inicia la simulación automáticamente al abrir la ventana
    start_simulation()

    dpg.create_viewport(title='Virus Simulator', width=800, height=800)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
