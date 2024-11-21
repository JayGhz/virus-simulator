# class UnionFind:
#     def __init__(self, n):
#         self.parent = list(range(n))  # Asegúrate de que 'n' sea el número correcto de nodos
#         self.rank = [0] * n  
#     def find(self, x):
#         if self.parent[x] != x:
#             self.parent[x] = self.find(self.parent[x])  # Compresión de caminos
#         return self.parent[x]

#     def union(self, x, y):
#         rootX = self.find(x)
#         rootY = self.find(y)

#         if rootX != rootY:
#             if self.rank[rootX] > self.rank[rootY]:
#                 self.parent[rootY] = rootX
#             elif self.rank[rootX] < self.rank[rootY]:
#                 self.parent[rootX] = rootY
#             else:
#                 self.parent[rootY] = rootX
#                 self.rank[rootX] += 1


# def kruskal_algorithm(nodes, edges):
#     uf = UnionFind(max(nodes) + 1)  # Inicializamos el UnionFind con el tamaño de nodos

#     # Ordenar las aristas por peso (esto asegura que Kruskal lo haga en orden)
#     edges = sorted(edges, key=lambda x: x[2])  # Ordenamos por el tercer valor (peso)

#     mst = []  # Árbol de expansión mínima

#     for u, v, weight in edges:
#         if uf.find(u) != uf.find(v):  # Si están en componentes distintas
#             uf.union(u, v)  # Unir los nodos
#             mst.append((u, v, weight))  # Añadir la arista al MST

#     return mst


# def dijkstra_max_path(nodes, edges, start, end):
#     # Construir el adj_list a partir de las aristas
#     adj_list = {node: [] for node in nodes}
#     for u, v, weight in edges:
#         adj_list[u].append((v, weight))
#         adj_list[v].append((u, weight))  # Si el grafo es no dirigido

#     # Inicialización
#     distances = {node: float('-inf') for node in nodes}
#     predecessors = {node: None for node in nodes}
#     distances[start] = 0
#     visited = set()

#     # Algoritmo de Dijkstra (modificado para maximizar pesos)
#     while visited != set(nodes):
#         max_node = None
#         for node in nodes:
#             if node not in visited:
#                 if max_node is None or distances[node] > distances[max_node]:
#                     max_node = node
        
#         if distances[max_node] == float('-inf'):
#             break

#         for neighbor, weight in adj_list[max_node]:
#             if neighbor not in visited:
#                 new_dist = distances[max_node] + weight
#                 if new_dist > distances[neighbor]:
#                     distances[neighbor] = new_dist
#                     predecessors[neighbor] = max_node

#         visited.add(max_node)

#     # Reconstruir la ruta más larga
#     path = []
#     current = end
#     while current is not None:
#         path.append(current)
#         current = predecessors[current]

#     path.reverse()

#     return distances[end], path



# # DJS Algorithm (Find connected components)
# def djs_algorithm(nodes, edges):
#     # Inicializamos UnionFind con el número de nodos
#     uf = UnionFind(max(nodes) + 1)

#     # Unimos los nodos según las aristas
#     for u, v, _ in edges:
#         uf.union(u, v)

#     # Diccionario para almacenar las componentes conectadas
#     components = {}  # El valor debe ser una lista de nodos

#     # Clasificamos los nodos según su componente (según la raíz del nodo)
#     for node in nodes:
#         root = uf.find(node)  # Encontramos la raíz del nodo
#         if root not in components:
#             components[root] = []  # Si no existe, inicializamos como lista
#         components[root].append(node)  # Añadimos el nodo a la lista correspondiente

#     # Ahora 'components' es un diccionario donde la clave es la raíz de la componente
#     # y el valor es una lista de nodos en esa componente

#     # Encontramos la componente más grande
#     largest_component = max(components.values(), key=len)  # Componente más grande

#     return largest_component


# def betweenness_centrality(nodes, edges):
#     centrality = {node: 0 for node in nodes}
    
#     for s in nodes:
#         for t in nodes:
#             if s != t:
#                 # Run Dijkstra to find shortest paths from s to t
#                 dist, path = dijkstra_algorithm(nodes, edges, s, t)
                
#                 for node in path[1:-1]:  
#                     centrality[node] += 1 / dist

#     return centrality

# def largest_connected_component(nodes, edges):
#     # Obtenemos las componentes conectadas utilizando djs_algorithm
#     components = djs_algorithm(nodes, edges)
    
#     # 'components' es ahora una lista de nodos, no un diccionario
#     return components  # Esta es la componente más grande, ya que max() lo garantizó