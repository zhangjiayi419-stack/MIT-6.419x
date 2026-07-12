# ==============================================
# Full CAVIAR Time-Varying Criminal Network Analysis
# Covers all homework parts: Part(a) ~ Part(b) Q5
# Dependencies: pandas, networkx, matplotlib, pygraphviz
# ==============================================

# --------------------------
# Step 1: Install Dependencies (only run once in Colab)
# --------------------------
import sys
import subprocess

def install_dependencies():
    # Colab system graphviz install
    subprocess.run(["apt-get", "install", "-y", "graphviz", "graphviz-dev"])
    subprocess.run([sys.executable, "-m", "pip", "install", "pygraphviz", "networkx", "pandas", "matplotlib"])

# Uncomment below line if running on Google Colab
# install_dependencies()

# --------------------------
# Step 2: Import Core Libraries
# --------------------------
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# --------------------------
# Step 3: Load all 11 Phase Adjacency Matrices from GitHub Dataset
# --------------------------
phases_data = {}
graph_collection = {}

for phase_num in range(1, 12):
    phase_name = f"phase{phase_num}"
    data_url = f"https://raw.githubusercontent.com/ragini30/Networks-Homework/main/{phase_name}.csv"
    
    # Read CSV adjacency matrix
    df = pd.read_csv(data_url, index_col="players")
    # Rename nodes to n1, n2 format to match homework notation
    df.columns = "n" + df.columns.astype(str)
    df.index = df.columns
    # Binarize matrix (all non-zero edges set to 1)
    df[df > 0] = 1
    phases_data[phase_num] = df
    
    # Create undirected networkX graph
    g = nx.from_pandas_adjacency(df)
    g.name = phase_name
    graph_collection[phase_num] = g

print("✅ All 11 phase networks loaded successfully.")

# --------------------------
# Part (a) Q1: Count Nodes & Edges for Phase 2,6,10
# --------------------------
print("\n========== Part (a) Q1 Network Size Stats ==========")
target_a_phases = [2, 6, 10]
for p in target_a_phases:
    g = graph_collection[p]
    node_count = g.number_of_nodes()
    edge_count = g.number_of_edges()
    print(f"Phase {p} | Nodes: {node_count} | Edges: {edge_count}")

# --------------------------
# Part (a) Q2: Draw Phase 3 Graph (Graphviz Layout for visual matching)
# --------------------------
def draw_phase_graph(phase_id, figsize=(12,8)):
    g = graph_collection[phase_id]
    plt.figure(figsize=figsize)
    pos = nx.drawing.nx_agraph.graphviz_layout(g)
    nx.draw(
        g, pos=pos, with_labels=True,
        node_color="magenta", node_size=400, font_size=8
    )
    plt.title(f"Phase {phase_id} Network Graph", fontsize=15)
    plt.show()

print("\n========== Part (a) Q2 Render Phase 3 Graph ==========")
draw_phase_graph(3)

# --------------------------
# Part (b) Q1: Normalized Degree Centrality (Phase3 & Phase9)
# --------------------------
print("\n========== Part (b) Q1 Normalized Degree Centrality ==========")
target_nodes_b = ["n1", "n3", "n12", "n83"]
target_phases_b = [3, 9]
degree_result = {}

for p in target_phases_b:
    g = graph_collection[p]
    deg_cent = nx.degree_centrality(g)
    degree_result[p] = {}
    for nd in target_nodes_b:
        val = deg_cent[nd]
        degree_result[p][nd] = val
        print(f"Phase {p}, Player {nd}: {val:.3g}")

# Tabulated output for homework fill-in
print("\nPlayer\tPhase3\tPhase9")
for nd in target_nodes_b:
    print(f"{nd}\t{degree_result[3][nd]:.3g}\t{degree_result[9][nd]:.3g}")

# --------------------------
# Part (b) Q2: Normalized Betweenness Centrality (Phase3 & Phase9)
# --------------------------
print("\n========== Part (b) Q2 Normalized Betweenness Centrality ==========")
betweenness_result = {}
for p in target_phases_b:
    g = graph_collection[p]
    btw_cent = nx.betweenness_centrality(g, normalized=True)
    betweenness_result[p] = {}
    for nd in target_nodes_b:
        val = btw_cent[nd]
        betweenness_result[p][nd] = val
        print(f"Phase {p}, Player {nd}: {val:.3g}")

print("\nPlayer\tPhase3\tPhase9")
for nd in target_nodes_b:
    print(f"{nd}\t{betweenness_result[3][nd]:.3g}\t{betweenness_result[9][nd]:.3g}")

# --------------------------
# Part (b) Q3: Eigenvector Centrality (Phase3 & Phase9)
# --------------------------
print("\n========== Part (b) Q3 Eigenvector Centrality ==========")
eigen_result = {}
for p in target_phases_b:
    g = graph_collection[p]
    eig_cent = nx.eigenvector_centrality(g)
    eigen_result[p] = {}
    for nd in target_nodes_b:
        val = eig_cent[nd]
        eigen_result[p][nd] = val
        print(f"Phase {p}, Player {nd}: {val:.3g}")

print("\nPlayer\tPhase3\tPhase9")
for nd in target_nodes_b:
    print(f"{nd}\t{eigen_result[3][nd]:.3g}\t{eigen_result[9][nd]:.3g}")

# --------------------------
# Part (b) Q5: Compute 11-phase average centrality
# Rule: Assign centrality = 0 if node missing in a phase
# Core 23 players defined from homework reading
# --------------------------
print("\n========== Part (b) Q5 Temporal Average Centrality Ranking ==========")
core_23_players = [
    "n1","n3","n6","n11","n12","n17","n5","n8","n76","n77","n80","n82",
    "n84","n85","n86","n87","n88","n89","n96","n106","n81","n107","n76"
]

# Storage for all 11 phase values for each core player
btw_timeline = {node: [] for node in core_23_players}
eig_timeline = {node: [] for node in core_23_players}

# Loop over every phase 1~11
for phase_id in range(1, 12):
    g = graph_collection[phase_id]
    bc = nx.betweenness_centrality(g, normalized=True)
    ec = nx.eigenvector_centrality(g)
    for player in core_23_players:
        # Fill zero if node does not exist in this phase
        btw_timeline[player].append(bc.get(player, 0.0))
        eig_timeline[player].append(ec.get(player, 0.0))

# Calculate average across all 11 phases
avg_betweenness = {p: sum(vals)/11 for p, vals in btw_timeline.items()}
avg_eigenvector = {p: sum(vals)/11 for p, vals in eig_timeline.items()}

# Sort descending by average value for ranking
ranked_btw = sorted(avg_betweenness.items(), key=lambda x: x[1], reverse=True)
ranked_eig = sorted(avg_eigenvector.items(), key=lambda x: x[1], reverse=True)

# Print Betweenness Top 5 Ranking (extract numeric ID for homework input)
print("=== Betweenness Centrality Global Average Ranking ===")
for rank, (node, mean_val) in enumerate(ranked_btw[:5], start=1):
    node_number = int(node.replace("n", ""))
    print(f"Rank {rank}: Node {node} | Input Number: {node_number} | Mean Value: {mean_val:.5f}")

# Print Eigenvector Top 5 Ranking
print("\n=== Eigenvector Centrality Global Average Ranking ===")
for rank, (node, mean_val) in enumerate(ranked_eig[:5], start=1):
    node_number = int(node.replace("n", ""))
    print(f"Rank {rank}: Node {node} | Input Number: {node_number} | Mean Value: {mean_val:.5f}")

# --------------------------
# End of Full Analysis Script
# --------------------------
