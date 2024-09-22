import gzip
import csv

# Descomprime y lee el archivo
with gzip.open('assets/dataset/facebook_combined.txt.gz', 'rt') as f:
    edges = [line.strip().split() for line in f]

# Procesa las conexiones
connections_dict = {}
for node, target in edges:
    if node not in connections_dict:
        connections_dict[node] = []
    connections_dict[node].append(target)

# Limitar la cantidad de datos para pruebas 
limiter = list(connections_dict.items())[:1500]

# Encuentra la máxima cantidad de conexiones (targets) para un nodo para definir cuántas columnas tendrá cada fila
max_targets = max(len(target_list) for _, target_list in limiter)

# Guardar en un archivo CSV con targets como columnas separadas
with open('output/data/facebook_connections.csv', 'w', newline='') as f:
    writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL, escapechar='\\')

    # Escribe cada fila con el nodo y sus conexiones, completando con vacíos si no tiene suficientes targets
    for node, target_list in limiter:
        row = [node] + target_list
        writer.writerow(row)