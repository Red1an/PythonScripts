import networkx as nx
import matplotlib.pyplot as plt

# Граф варианта 6
G = nx.Graph()
edges_w = [(1,2,3),(1,3,6),(1,4,5),(2,3,2),(2,5,4),(3,4,1),(4,5,7)]
G.add_weighted_edges_from(edges_w)

pos = nx.spring_layout(G, seed=42)
weights = nx.get_edge_attributes(G, 'weight')
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=600)
nx.draw_networkx_edge_labels(G, pos, edge_labels=weights)
plt.title("Граф вариант 6")
plt.show()