import dearpygui.dearpygui as dpg
import networkx as nx
import pandas as pd
import random

# Variables globales
key_node = None
subgraph_nodes = set()
node_ids = {}
node_positions = {}
key_nodes = []  # Lista de nodos clave
current_index = 0  # Índice actual de nodo clave

# Cargar el grafo desde un archivo CSV
def load_graph_from_custom_csv(file_path):
    try:
        df = pd.read_csv(file_path, index_col=0, header=None, on_bad_lines='skip')
    except Exception as e:
        print(f"Error al leer el archivo CSV: {e}")
        return None

    G = nx.Graph()
    for node, connections in df.iterrows():
        for target in connections.dropna():
            try:
                G.add_edge(int(node), int(target), weight=random.random())
            except ValueError:
                print(f"Advertencia: Nodo inválido '{target}' en fila {node}, ignorando esta conexión.")
    return G

# Algoritmo para encontrar el primer nodo clave (usando Dijkstra, por ejemplo)
def find_key_node(G):
    global key_node, subgraph_nodes, key_nodes
    # Usamos el grado de los nodos para determinar el nodo clave (o Dijkstra o alguna heurística similar)
    node_degrees = dict(G.degree())  # Calcular el grado de todos los nodos
    key_node = max(node_degrees, key=node_degrees.get)  # Nodo con el mayor grado
    subgraph_nodes = set(G.neighbors(key_node))
    key_nodes = [key_node]

# Dibujar el grafo completo con todos los nodos y agregar bordes a los nodos
def draw_full_graph(G):
    dpg.delete_item("canvas", children_only=True)
    offset_x, offset_y = 600, 400  # Desplazar el grafo a la izquierda

    # Primero, dibujamos todas las aristas
    for edge in G.edges:
        x1, y1 = node_positions[edge[0]]
        x2, y2 = node_positions[edge[1]]
        dpg.draw_line((x1 + offset_x, y1 + offset_y), (x2 + offset_x, y2 + offset_y), color=(250, 250, 250), parent="canvas")

    # Identificar los nodos clave dinámicamente (por ejemplo, con el grado más alto)
    global key_nodes
    key_nodes = [node for node in G.nodes if G.degree(node) > 5]  # Filtramos nodos con grado mayor a 5

    # Luego, dibujamos todos los nodos en verde y los nodos clave en azul, con borde
    for node in G.nodes:
        x, y = node_positions[node]
        if node in key_nodes:
            color = (0, 0, 255)  # Nodo clave en azul
            border_color = (250, 250, 250)  # Borde blanco
        else:
            color = (60, 219, 65)
            border_color =  (250, 250, 250)  # Borde negro

        dpg.draw_circle((x + offset_x, y + offset_y), 12, color=border_color, fill=color, parent="canvas")  # Nodo con borde

    # Dibujar el nodo clave por encima de todos los nodos y aristas
    key_node_x, key_node_y = node_positions[key_node]
    dpg.draw_circle((key_node_x + offset_x, key_node_y + offset_y), 15, color=(0, 0, 255), fill=(255, 255, 255), parent="canvas")
    dpg.draw_text((key_node_x + offset_x + 10, key_node_y + offset_y - 10), str(key_node), color=(0, 0, 0), parent="canvas")

# Dibujar solo el subgrafo del nodo clave (nodo clave y sus vecinos)
def draw_subgraph(G):
    dpg.delete_item("canvas", children_only=True)  # Eliminar el contenido previo en el canvas
    offset_x, offset_y = 600, 400  # Desplazar el grafo a la izquierda

    # Dibujar el nodo clave por encima de todo
    key_node_x, key_node_y = node_positions[key_node]
    dpg.draw_circle((key_node_x + offset_x, key_node_y + offset_y), 15, color=(0, 0, 255), fill=(255, 255, 255), parent="canvas")
    dpg.draw_text((key_node_x + offset_x + 10, key_node_y + offset_y - 10), str(key_node), color=(0, 0, 0), parent="canvas")

    # Dibujar los vecinos del nodo clave (en blanco)
    for neighbor in subgraph_nodes:
        x, y = node_positions[neighbor]
        dpg.draw_circle((x + offset_x, y + offset_y), 12, color=(0, 0, 0), fill=(255, 255, 255), parent="canvas")  # Vecinos en blanco
        dpg.draw_text((x + offset_x + 10, y + offset_y - 10), str(neighbor), color=(255, 255, 255), parent="canvas")

        # Dibujar las aristas entre el nodo clave y sus vecinos
        x1, y1 = node_positions[key_node]
        x2, y2 = node_positions[neighbor]
        dpg.draw_line((x1 + offset_x, y1 + offset_y), (x2 + offset_x, y2 + offset_y), color=(200, 200, 200), parent="canvas")

# Función para pasar al siguiente nodo clave
def next_node(G):
    global current_index
    if len(key_nodes) > 1:  # Solo continuar si hay más de un nodo clave
        current_index = (current_index + 1) % len(key_nodes)  # Avanzar al siguiente nodo clave
        find_key_node(G)  # Actualizar el nodo clave y sus vecinos
        draw_subgraph(G)  # Dibujar el nuevo subgrafo del nodo clave

# Ejecutar DearPyGUI
def run_dearpygui():
    dpg.create_context()
    G = load_graph_from_custom_csv('output/data/facebook_connections.csv')

    # Calcular posiciones para el grafo y dibujar el primer subgrafo
    global node_positions
    layout = nx.spring_layout(G, k=0.25, scale=1.0)
    node_positions = {node: (x * 300, y * 300) for node, (x, y) in layout.items()}

    with dpg.handler_registry():
        with dpg.window(label="Simulación de Nodos Claves", width=1400, height=900):  # Ajuste en el tamaño de la ventana
            # Crear los botones en la parte superior y configurar el canvas
            with dpg.group(horizontal=True):
                dpg.add_button(label="Siguiente Nodo", callback=lambda: next_node(G))
                dpg.add_button(label="Identificar Todos los Nodos Clave", callback=lambda: draw_full_graph(G))

            # Crear el canvas para el grafo
            with dpg.drawlist(width=1400, height=850, tag="canvas"):  # Ajuste en el tamaño del canvas (más alto)
                find_key_node(G)  # Encontrar el primer nodo clave y sus vecinos
                draw_subgraph(G)  # Dibujar el primer subgrafo

    dpg.create_viewport(title='Nodo Clave Simulador', width=1400, height=900)  # Ajuste de la ventana para mejor visibilidad
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
