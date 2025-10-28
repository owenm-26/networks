import matplotlib.pyplot as plt
import numpy as np

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
    
