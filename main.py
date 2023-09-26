import json
import random
import matplotlib.pyplot as plt
import networkx as nx

# 1. Load the Graph Data
with open("graph.json", "r") as file:
    graph_data = json.load(file)

# Create a Pheromone Matrix
pheromone_matrix = {}
for node, neighbors in graph_data.items():
    pheromone_matrix[node] = {}
    for neighbor in neighbors:
        pheromone_matrix[node][neighbor] = {"pheromone": 0.01}
print(f"pheromone_matrix:\n{pheromone_matrix}")


# 2. Ant Movement
def simulate_ant_movement(graph):
    current_node = "0"
    end_node = "29"
    path = [current_node]
    while current_node != end_node:
        neighbors = list(graph[current_node].keys())
        next_node = random.choice(neighbors)
        path.append(next_node)
        current_node = next_node
    return path


# 3. Keep store of the ants path

num_ants = 10
ant_paths = [simulate_ant_movement(graph_data) for _ in range(num_ants)]
print(f"ant_paths:\n{ant_paths}")


# 4. Update Pheromone Matrix
def compute_path_cost(path, graph):
    cost = 0
    for i in range(len(path) - 1):
        cost += graph[path[i]][path[i + 1]]["weight"]
    return cost


def update_pheromone(pheromone_matrix, path, graph, constant_factor=1):
    path_cost = compute_path_cost(path, graph)
    for i in range(len(path) - 1):
        pheromone_value = pheromone_matrix[path[i]][path[i + 1]]["pheromone"]
        pheromone_matrix[path[i]][path[i + 1]]["pheromone"] = pheromone_value + (
            constant_factor / path_cost
        )


for path in ant_paths:
    update_pheromone(pheromone_matrix, path, graph_data)

print(
    f"first few entries of the updated pheromone matrix:\n{list(pheromone_matrix.items())[:5]}"
)


# 5. Visualization
G = nx.Graph()
for node, neighbors in graph_data.items():
    for neighbor, data in neighbors.items():
        G.add_edge(
            node,
            neighbor,
            weight=data["weight"],
            pheromone=pheromone_matrix[node][neighbor]["pheromone"],
        )

pos = nx.spring_layout(G)
edge_colors = [G[u][v]["pheromone"] for u, v in G.edges()]
plt.figure(figsize=(10, 8))
nx.draw(
    G,
    pos,
    with_labels=True,
    node_size=800,
    node_color="lightblue",
    edge_color=edge_colors,
    width=2.0,
    edge_cmap=plt.cm.Blues,
)
plt.title("Graph with Pheromone Values")
plt.colorbar(
    plt.cm.ScalarMappable(cmap=plt.cm.Blues),
    label="Pheromone Value",
    orientation="horizontal",
)
plt.show()

# 6. Compare with Shortest Path
shortest_path = nx.shortest_path(G, source="0", target="29", weight="weight")
shortest_path_cost = compute_path_cost(shortest_path, graph_data)

print(f"shortest_path, shortest_path_cost:\n{shortest_path}, {shortest_path_cost}")
