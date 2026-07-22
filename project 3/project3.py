#install graphviz and python in colab
!apt-get install graphviz graphviz-dev
!pip install pygraphviz networkx pandas matplotlib

#Part (a)
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# 读取 phase1 ~ phase11 adjacency matrix
phases = {}
G = {}
for i in range(1, 12):
    var_name = "phase" + str(i)
    file_url = "https://raw.githubusercontent.com/ragini30/Networks-Homework/main/" + var_name + ".csv"
    # import CSV data
    df = pd.read_csv(file_url, index_col="players")
    # standardize node names to n1, n2 ...
    df.columns = "n" + df.columns.astype(str)
    df.index = df.columns
    # change into 0/1 adjacency matrix
    df[df > 0] = 1
    phases[i] = df
    # construct undirected network graph
    graph = nx.from_pandas_adjacency(df)
    G[i] = graph
    graph.name = var_name

# ========== output Phase 2 / 6 / 10 ==========
target_phases = [2, 6, 10]
print("=== Answer ===")
for p in target_phases:
    node_count = G[p].number_of_nodes()
    edge_count = G[p].number_of_edges()
    print(f"Phase {p} | Nodes: {node_count} | Edges: {edge_count}")

# draw the picture ofPhase3 (graphviz_layout）
plt.figure(figsize=(12, 8))
g3 = G[3]
pos = nx.drawing.nx_agraph.graphviz_layout(g3)
nx.draw(g3, pos=pos, with_labels=True, node_color="magenta", node_size=400, font_size=8)
plt.title("Phase 3 Network Graph", fontsize=15)
plt.show()

#Part(b) Q1
import networkx as nx
import pandas as pd

# Target nodes
target_nodes = ["n1", "n3", "n12", "n83"]
target_phases = [3, 9]

# store results
result = {}
for phase in target_phases:
    g = G[phase]
    # nx.degree_centrality exactly matches the definition ki/(n-1)
    deg_cent = nx.degree_centrality(g)
    result[phase] = {}
    for node in target_nodes:
        # retain three significant level
        val = deg_cent[node]
        result[phase][node] = round(val, 3)
        print(f"Phase {phase}, Node {node}: {val:.3g}")

# print table
print("\n=====All the results=====")
print("Node\tPhase3\tPhase9")
for nd in target_nodes:
    p3 = result[3][nd]
    p9 = result[9][nd]
    print(f"{nd}\t{p3:.3f}\t{p9:.3f}")

#Partb Q2
import networkx as nx

# target nodes and phases
target_nodes = ["n1", "n3", "n12", "n83"]
target_phases = [3, 9]
betweenness_result = {}

# Loop to calculate standardized betweenness centrality
for phase_num in target_phases:
    graph = G[phase_num]
    # normalized=True fit B_i
    bc_dict = nx.betweenness_centrality(graph, normalized=True)
    betweenness_result[phase_num] = {}
    for node in target_nodes:
        val = bc_dict[node]
        betweenness_result[phase_num][node] = val
        # print each result
        print(f"Phase {phase_num}, Player {node}: {val:.3g}")

# Print table
print("\n===== Table(3 significant figures)=====")
print("Player\tPhase3\t\tPhase9")
for nd in target_nodes:
    val3 = betweenness_result[3][nd]
    val9 = betweenness_result[9][nd]
    print(f"{nd}\t{val3:.3g}\t\t{val9:.3g}")

#Partb Q3
import networkx as nx

target_nodes = ["n1", "n3", "n12", "n83"]
target_phases = [3, 9]
eig_result = {}

for phase_num in target_phases:
    g = G[phase_num]
    # networkx.eigenvector_centrality default normalization
    ec = nx.eigenvector_centrality(g)
    eig_result[phase_num] = {}
    for node in target_nodes:
        val = ec[node]
        eig_result[phase_num][node] = val
        print(f"Phase {phase_num}, {node}: {val:.3g}")

# Print the table
print("\n===== Eigenvector Centrality (3 sig figs) =====")
print("Player\tPhase3\tPhase9")
for nd in target_nodes:
    p3 = eig_result[3][nd]
    p9 = eig_result[9][nd]
    print(f"{nd}\t{p3:.3g}\t{p9:.3g}")


#Partb Q5
import pandas as pd
import networkx as nx

# 1. import 11 phase
phases = {}
G = {}
for i in range(1, 12):
    url = f"https://raw.githubusercontent.com/ragini30/Networks-Homework/main/phase{i}.csv"
    df = pd.read_csv(url, index_col="players")
    df.columns = "n" + df.columns.astype(str)
    df.index = df.columns
    df[df>0] = 1
    G[i] = nx.from_pandas_adjacency(df)

# the list of 23 core people
core = ["n1","n3","n6","n11","n12","n17","n5","n8","n76","n77","n80","n82","n84","n85","n86","n87","n88","n89","n96","n106","n80","n81","n107"]

# Save each player's 11-phase betweenness centrality; missing values = 0.
btw_record = {node: [] for node in core}
for phase_id in range(1,12):
    g = G[phase_id]
    bc_dict = nx.betweenness_centrality(g, normalized=True)
    for nd in core:
        val = bc_dict.get(nd, 0.0)
        btw_record[nd].append(val)

# Compute 11-phase mean values
btw_mean = {nd: sum(vals)/11 for nd, vals in btw_record.items()}
# sort descending and output full ranking
ranked_btw = sorted(btw_mean.items(), key=lambda x:x[1], reverse=True)

# print the ranking
print("=== Betweenness Mean Full Ranking ===")
for idx, (node, mean_val) in enumerate(ranked_btw[:5], start=1):
    num = int(node.replace("n",""))
    print(f"Rank{idx}: Node {node}, number={num}, average={mean_val:.5f}")