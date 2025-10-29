import matplotlib.pyplot as plt
import numpy as np
import os
import pickle
import seaborn as sns

def create_scatter_plot(x, y, x_label, y_label, title, labels=None, paradox_line=False):
    """
    x, y: lists or arrays of numeric values
    labels: optional list of strings, one per point, to label the scatter points
    paradox_line: if True, draw y=x line to indicate friendship paradox regime
    """
    plt.figure(figsize=(10, 7))
    
    # Scatter points
    plt.scatter(x, y, color='blue', s=50, alpha=0.7)

    # Draw friendship paradox line y=x
    if paradox_line:
        min_val = min(min(x), min(y))
        max_val = max(max(x), max(y))
        plt.plot([min_val, max_val], [min_val, max_val], color='red', linestyle='--', label='y = x')

    # Label points if labels are provided
    if labels:
        for xi, yi, label in zip(x, y, labels):
            plt.text(xi + 0.02, yi + 0.02, label, fontsize=9, alpha=0.8)

    # Axes labels and title
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    if paradox_line:
        plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{title}.png")
    plt.show()


def create_modularity_charts():
    # ---------------------------------------------------------
    # CONFIG
    # ---------------------------------------------------------
    # path to your pickle from metric-scripts/modularity.py
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    modularity_path = os.path.join(project_root, "modularities.pkl")

    # optional: if you stored graph sizes (node counts) somewhere
    sizes_path = os.path.join(project_root, "network_sizes.pkl")  # optional
    # if you don't have this, you can mock or skip x-axis sizes

    # names of the four comparisons (order matches your modularities list)
    comparisons = ["Gender", "Major", "Student Status", "Degree"]

    # ---------------------------------------------------------
    # LOAD DATA
    # ---------------------------------------------------------
    with open(modularity_path, "rb") as f:
        modularities = pickle.load(f)   # list of 4 lists of Q values

    # if you saved sizes in another file
    if os.path.exists(sizes_path):
        with open(sizes_path, "rb") as f:
            network_sizes = pickle.load(f)  # list of n values (same order)
    else:
        # fallback mock: just 1..len
        raise ValueError("NO NETWORK SIZE PICKLE FOUND")

    # ---------------------------------------------------------
    # PLOTTING
    # ---------------------------------------------------------
    sns.set_theme(style="whitegrid", font_scale=1.2)

    output_dir = os.path.join(project_root, "figures")
    os.makedirs(output_dir, exist_ok=True)

    for comp, Q_values in zip(comparisons, modularities):
        Q_values = np.array(Q_values)
        n_values = np.array(network_sizes)

        # ---------- SCATTER PLOT ----------
        plt.figure(figsize=(7,5))
        plt.scatter(n_values, Q_values, alpha=0.7)
        plt.xscale("log")
        plt.axhline(0, color="red", linestyle="--", label="No assortativity (Q=0)")
        plt.title(f"Modularity vs Network Size — {comp}")
        plt.xlabel("Network size n (log scale)")
        plt.ylabel("Modularity Q")
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"{comp.lower()}_scatter.png"), dpi=300)
        plt.close()

        # ---------- HISTOGRAM / DENSITY PLOT ----------
        plt.figure(figsize=(7,5))
        sns.histplot(Q_values, bins=20, kde=True, color="skyblue", edgecolor="black")
        plt.axvline(0, color="red", linestyle="--", label="No assortativity (Q=0)")
        plt.title(f"Distribution of Modularity — {comp}")
        plt.xlabel("Modularity Q")
        plt.ylabel("Frequency")
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"{comp.lower()}_hist.png"), dpi=300)
        plt.close()

    print(f"✅ Plots saved in: {output_dir}")

        
