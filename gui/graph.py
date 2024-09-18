import dearpygui.dearpygui as dpg
import networkx as nx
import pandas as pd
import random

infected_nodes = set()

# Leer el archivo CSV personalizado y generar el grafo
def load_graph_from_custom_csv(file_path):
    df = pd.read_csv(file_path, index_col=0,sep=',', on_bad_lines='skip', nrows=20, usecols=range(10))  # Leer el archivo CSV y omitir la primera columna que es el índice
    G = nx.Graph()

    # Iterar sobre cada fila y agregar las conexiones
    for node, connections in df.iterrows():
        for target in connections.dropna():
            G.add_edge(node, int(target))  # Agregar una arista entre 'node' y cada 'target'

    return G

# Función para dibujar el grafo en DearPyGUI
def draw_graph():
    file_path = 'output/data/facebook_connections.csv'  # Cambia esto por la ruta a tu archivo CSV
    G = load_graph_from_custom_csv(file_path)
    
    dpg.delete_item("canvas", children_only=True)  # Borra el canvas cada vez que actualizamos

    layout = nx.spring_layout(G, k=0.25, scale=1.0)  # Layout de NetworkX para las posiciones de los nodos
    
    for node in G.nodes:
        x, y = layout[node]  # Obtener las coordenadas del nodo
        x *= 300  # Ajustar las coordenadas para que se vean en el canvas
        y *= 300

        # Si el nodo está infectado, se dibuja en rojo
        color = (255, 0, 0) if node in infected_nodes else (0, 255, 0)  # Verde si está sano, rojo si infectado

        # Dibujar el nodo
        dpg.draw_circle((x+400, y+400), 10, color=color, parent="canvas", fill=color)
    
    # Dibujar las conexiones (aristas)
    for edge in G.edges:
        x1, y1 = layout[edge[0]]
        x2, y2 = layout[edge[1]]
        dpg.draw_line((x1 * 300 + 400, y1 * 300 + 400), (x2 * 300 + 400, y2 * 300 + 400), color=(200, 200, 200), parent="canvas")

# Función para infectar nodos aleatorios
def infect_nodes(sender, app_data, user_data):
    G = load_graph_from_custom_csv('output/data/facebook_connections.csv')  # Volver a cargar el grafo
    if len(infected_nodes) < len(G.nodes):
        next_infected = random.choice(list(set(G.nodes) - infected_nodes))
        infected_nodes.add(next_infected)
        draw_graph()

# Crear la ventana de DearPyGUI
def create_window():
    dpg.create_context()

    with dpg.window(label="Simulación de Propagación de Virus", width=800, height=800):
        dpg.add_button(label="Infectar Nodo", callback=infect_nodes)  # Botón para infectar nodos
        dpg.add_drawlist(width=800, height=800, tag="canvas")  # Canvas para dibujar el grafo

    draw_graph()  # Dibuja el grafo inicialmente

    dpg.create_viewport(title='Simulación Virus', width=800, height=800)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

