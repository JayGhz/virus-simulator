## Simulación de Propagación de Virus en Grafos

Este proyecto tiene como objetivo simular la propagación de un virus a través de una red de nodos, donde cada nodo representa una persona y las aristas entre ellos representan la probabilidad de contagio. Utilizaremos distintos algoritmos y técnicas de búsqueda para modelar esta propagación.

### Características del Proyecto

- **Simulación de Propagación**: Se modela la propagación de un virus en una red social usando grafos.
- **Algoritmos Implementados**:
  - **Algoritmo de Kruskal**: Para encontrar árboles de expansión mínima y observar cómo afecta la conectividad a la propagación.
  - **Fuerza Bruta**: Para evaluar todas las posibles rutas de propagación y analizar las más críticas.
  - **Algoritmo A\***: Para encontrar la ruta óptima de contagio en términos de probabilidad y distancia entre nodos.
- **Visualización de Resultados**: Se utilizará una GUI desarrollada con DearPyGUI para interactuar con los resultados de la simulación.


### Requisitos

- **Python 3+**
- Librerías iniciales necesarias:
  - `DearPyGUI`
  - `pandas`
  - `networkx`

Para instalar las dependencias, ejecutar:
```bash
pip install -r requirements.txt