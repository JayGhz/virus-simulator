import dearpygui.dearpygui as dpg
import networkx as nx
import pandas as pd
import heapq

key_node = None
subgraph_nodes = set()
node_ids = {}
node_positions = {}
key_nodes = []
current_index = 0
G = None

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
                G.add_edge(node, target)
            except ValueError:
                print(f"Advertencia: Nodo inválido '{target}' en fila {node}, ignorando esta conexión.")
    return G

# Función para encontrar los nodos clave en el grafo segun el grado de conexión
def find_key_nodes(G, top_n=250):
    global key_nodes
    if G is not None and isinstance(G, nx.Graph):
        key_nodes = sorted(G.nodes, key=lambda node: len(list(G.neighbors(node))), reverse=True)[:top_n]
        if key_nodes:
            print(f"Nodos clave encontrados: {key_nodes}")
        else:
            print("No se encontraron nodos clave.")

def draw_subgraph(G, local_subgraph_nodes, key_node, canvas_tag):
    global node_positions
    if key_node is None or key_node not in node_positions:
        return
    if not dpg.does_item_exist(canvas_tag):
        return
    dpg.delete_item(canvas_tag, children_only=True)

    subgraph = G.subgraph([key_node] + local_subgraph_nodes)
    subgraph_layout = nx.spring_layout(subgraph, k=1.0, scale=1.0)  
    subgraph_positions = {node: (x * 300, y * 300) for node, (x, y) in subgraph_layout.items()}  #

    # Dibujar nodo clave (nodo azul)
    key_node_x, key_node_y = subgraph_positions[key_node]
    offset_x, offset_y = 600, 400
    dpg.draw_circle((key_node_x + offset_x, key_node_y + offset_y), 12, color=(255, 255, 255), fill=(0, 0, 255), parent=canvas_tag)
    dpg.draw_text((key_node_x + offset_x + 14, key_node_y + offset_y - 12), str(key_node), color=(255, 255, 255), parent=canvas_tag, size=16)

    # Dibujar los vecinos y conexiones del nodo clave
    for neighbor in local_subgraph_nodes:
        x, y = subgraph_positions[neighbor]
        dpg.draw_circle((x + offset_x, y + offset_y), 12, color=(255, 255, 255), fill=(255, 255, 255), parent=canvas_tag)
        dpg.draw_text((x + offset_x + 14, y + offset_y - 12), str(neighbor), color=(255, 255, 255), parent=canvas_tag, size=16)
        dpg.draw_line((key_node_x + offset_x, key_node_y + offset_y), (x + offset_x, y + offset_y), color=(150, 150, 150), parent=canvas_tag)

def draw_full_graph(G, canvas_tag, node_info):
    global node_positions
    if G is None:
        return
    if not dpg.does_item_exist(canvas_tag):
        return
    dpg.delete_item(canvas_tag, children_only=True)

    layout = nx.spring_layout(G, k=0.3, scale=0.8)
    node_positions = {node: (x * 300, y * 300) for node, (x, y) in layout.items()}

    offset_x, offset_y = 600, 400  

    # Dibujar las aristas (líneas entre nodos)
    for edge in G.edges:
        x1, y1 = node_positions[edge[0]]
        x2, y2 = node_positions[edge[1]]
        dpg.draw_line((x1 + offset_x, y1 + offset_y), (x2 + offset_x, y2 + offset_y), color=(255, 255, 255), parent=canvas_tag)

    # Dibujar los nodos
    for node in G.nodes:
        x, y = node_positions[node]
        color = (60, 219, 65)  # Verde para nodos no clave
        if node in key_nodes:
            color = (0, 0, 255)  # Azul para nodos clave

        border_color = (255, 255, 255)  # Borde blanco para todos los nodos

        dpg.draw_circle((x + offset_x, y + offset_y), 12, color=border_color, parent=canvas_tag)
        dpg.draw_circle((x + offset_x, y + offset_y), 10, color=color, parent=canvas_tag, fill=color)

    # Actualizar el mensaje con la cantidad de nodos clave identificados
    dpg.set_value(node_info, f"La cantidad de nodos clave identificados en el grafo es: {len(key_nodes)}")

def next_node(G, canvas_tag, node_info):
    global current_index, key_node
    if key_nodes:
        current_index = (current_index + 1) % len(key_nodes)
        key_node = key_nodes[current_index]
        draw_subgraph(G, list(G.neighbors(key_node)), key_node, canvas_tag)
        num_connections = len(list(G.neighbors(key_node)))
        dpg.set_value(node_info, f"El nodo clave actual es {key_node} y tiene {num_connections} conexiones.")

def run_dearpygui():
    global G, node_positions, key_node
    dpg.create_context()
    G = load_graph_from_custom_csv('output/data/facebook_connections.csv')

    if G is not None:
        layout = nx.spring_layout(G, k=0.3, scale=1.5)
        node_positions = {node: (x * 400, y * 400) for node, (x, y) in layout.items()}

        find_key_nodes(G)
        if key_nodes:
            key_node = key_nodes[0]
            canvas_tag = "canvas"
            with dpg.window(label="Información del Nodo", width=300, height=100):
                node_info = dpg.add_text(f"El nodo clave actual es {key_node} y tiene {len(list(G.neighbors(key_node)))} conexiones.")
            
            draw_subgraph(G, list(G.neighbors(key_node)), key_node, canvas_tag)
    
    with dpg.handler_registry():
        with dpg.window(label="Simulación de Nodos Claves", width=1400, height=900):
            with dpg.group(horizontal=True):
                dpg.add_button(label="Siguiente Nodo", callback=lambda: next_node(G, "canvas", node_info))
                dpg.add_button(label="Identificar Todos los Nodos Clave", callback=lambda: draw_full_graph(G, "canvas", node_info))
            with dpg.group(horizontal=True):
                node_info = dpg.add_text(f"El nodo clave actual es {key_node} y tiene {len(list(G.neighbors(key_node)))} conexiones.")
            with dpg.drawlist(width=1400, height=850, tag="canvas"):
                if key_nodes:
                    draw_subgraph(G, list(G.neighbors(key_node)), key_node, "canvas")

    dpg.create_viewport(title='Nodo Clave Simulador', width=1400, height=900)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
