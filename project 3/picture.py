import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# ========== 1. Facebook network ==========
G_fb = nx.read_edgelist("facebook_combined.txt", nodetype=int)
N = G_fb.number_of_nodes()
M = G_fb.number_of_edges()
print(f"Facebook N={N}, M={M}")

# ========== 2. Create three comparative models ==========
# ER p = 2M/(N(N-1))
p = 2*M / (N*(N-1))
G_er = nx.erdos_renyi_graph(N, p, seed=42)
# WS k=44, p=0.05
G_ws = nx.watts_strogatz_graph(N, k=44, p=0.05, seed=42)
# BA m=22
G_ba = nx.barabasi_albert_graph(N, m=22, seed=42)

def get_degree_dist(G):
    degrees = [d for n,d in G.degree()]
    hist, bins = np.histogram(degrees, bins=np.logspace(np.log10(1), np.log10(max(degrees)), 40))
    prob = hist / sum(hist)
    centers = (bins[1:] + bins[:-1])/2
    # filter zero-probability points to avoid log runtime errors
    mask = prob > 0
    return centers[mask], prob[mask]

# Obtain the degree distribution of each group
k_fb, pk_fb = get_degree_dist(G_fb)
k_ws, pk_ws = get_degree_dist(G_ws)
k_ba, pk_ba = get_degree_dist(G_ba)

# ========== draw  ==========
plt.figure(figsize=(12,8), dpi=150)
plt.loglog(k_fb, pk_fb, 'o', c="#2266bb", markersize=3, label="Empirical Facebook")
plt.loglog(k_ws, pk_ws, 'o', c="#3399dd", markersize=4, label="Watts-Strogatz (WS)")
plt.loglog(k_ba, pk_ba, 'o', c="#ee8833", markersize=4, label="Barabási-Albert (BA)")

plt.xlabel("Node Degree $k$ (Log Scale)")
plt.ylabel("Probability $P(k)$ (Log Scale)")
plt.title("Degree Distribution Comparison (Log-Log Scale)")
plt.legend()
plt.grid(True, alpha=0.3, which="both")
plt.savefig("degree_distribution_all.png", bbox_inches="tight")
plt.show()