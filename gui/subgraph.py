import dearpygui.dearpygui as dpg
import networkx as nx
import pandas as pd

# Leer el archivo CSV personalizado y generar el grafo
def load_graph_from_custom_csv(file_path):
    df = pd.read_csv(file_path, index_col=0, sep=',', on_bad_lines='skip')
    G = nx.Graph()

    for node, connections in df.iterrows():
        for target in connections.dropna():
            G.add_edge(node, int(target))

    return G

# Función para dibujar el grafo en DearPyGUI
def draw_graph():
    file_path = 'output/data/facebook_connections.csv'  # Cambia esto por la ruta a tu archivo CSV
    G = load_graph_from_custom_csv(file_path)

    # Filtrar el grafo para incluir solo el nodo 7 y sus amigos
    subgraph_nodes = {7} | set(G.neighbors(7))  # Nodo 7 y sus vecinos
    subgraph = G.subgraph(subgraph_nodes)

    dpg.delete_item("canvas", children_only=True)  # Borra el canvas cada vez que actualizamos

    layout = nx.spring_layout(subgraph, k=0.5, scale=1.0)  # Aumentar 'k' para mayor separación

    # Centrar el nodo 7
    layout[7] = (0, 0)  # Posición central (0, 0)

    # Dibujar las conexiones (aristas) en azul
    for edge in subgraph.edges:
        x1, y1 = layout[edge[0]]
        x2, y2 = layout[edge[1]]
        dpg.draw_line((x1 * 300 + 400, y1 * 300 + 400), (x2 * 300 + 400, y2 * 300 + 400), color=(0, 0, 255), thickness=2, parent="canvas")

    # Dibujar los nodos
    for node in subgraph.nodes:
        x, y = layout[node]
        x *= 300  # Ajustar las coordenadas
        y *= 300

        # Color del nodo
        color = (0, 0, 255) if node == 7 else (0, 255, 0)  # Azul para el nodo 7, verde para los demás

        # Dibujar el nodo
        dpg.draw_circle((x + 400, y + 400), 15, color=color, parent="canvas", fill=color)  # Tamaño de 15

    # Dibujar los números de los nodos encima de los nodos y las aristas
    for node in subgraph.nodes:
        x, y = layout[node]
        x *= 300
        y *= 300
        dpg.draw_text((x + 400, y + 400 + 20), str(node), color=(255, 255, 255), parent="canvas", size=20)  # Número encima

# Crear la ventana de DearPyGUI
def create_window():
    dpg.create_context()

    with dpg.window(label="Simulación de Propagación de Virus", width=800, height=800):
        dpg.add_drawlist(width=800, height=800, tag="canvas")  # Canvas para dibujar el grafo

    draw_graph()  # Dibuja el grafo inicialmente

    dpg.create_viewport(title='Virus Simulator', width=800, height=800)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

