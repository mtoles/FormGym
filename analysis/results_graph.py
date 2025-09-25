import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches

# Set style for beautiful plots
plt.style.use("default")
plt.rcParams["figure.facecolor"] = "white"
plt.rcParams["axes.facecolor"] = "white"
plt.rcParams["font.size"] = 10
plt.rcParams["axes.titlesize"] = 16
plt.rcParams["axes.labelsize"] = 28
plt.rcParams["xtick.labelsize"] = 24
plt.rcParams["ytick.labelsize"] = 24
plt.rcParams["legend.fontsize"] = 24

# Data preparation - reorganize by task
tasks = [
    "Auto Loans (Text) - One Shot",
    "Auto Loans (Text) - Iterative",
    "Auto Loans (Doc Transfer) - One Shot",
    "Auto Loans (Doc Transfer) - Iterative",
    "FUNSD - One Shot",
    "XFUND - One Shot",
    "Form-NLU - One Shot",
]

models = ["Aria 25B", "Claude 4", "GPT-5", "Llava 7B", "Molmo 7B"]

# Base model data
base_data = {
    "Auto Loans (Text) - One Shot": [0.0, 0.0, 1.0, 0.0, 0.0],
    "Auto Loans (Text) - Iterative": [0.0, 0.3, 2.0, 0.0, 0.0],
    "Auto Loans (Doc Transfer) - One Shot": [0.0, 0.3, 0.5, 0.0, 0.0],
    "Auto Loans (Doc Transfer) - Iterative": [
        0.0,
        0.0,
        1.0,
        0.00000001,
        0.0,
    ],  # .00000001 to avoid 0 and have a label
    "FUNSD - One Shot": [1.0, 21.0, 2.0, 1.0, 1.0],
    "XFUND - One Shot": [1.0, 1.0, 2.0, 1.0, 1.0],
    "Form-NLU - One Shot": [0.0, 0.0, 0.0, 0.0, 0.0],
}

# FF enhanced data
ff_data_needs_destack = {
    "Auto Loans (Text) - One Shot": [3.3, 8.3, 8.5, 1.0, 0.5],
    "Auto Loans (Text) - Iterative": [2.8, 7.8, 8.0, 0.3, 1.0],
    "Auto Loans (Doc Transfer) - One Shot": [1.5, 4.8, 3.0, 0.3, 0.0],
    "Auto Loans (Doc Transfer) - Iterative": [1.3, 2.8, 3.0, 0.0, 0.0],
    "FUNSD - One Shot": [20.0, 32.0, 29.0, 4.0, 9.0],
    "XFUND - One Shot": [9.0, 15.0, 14.0, 3.0, 3.0],
    "Form-NLU - One Shot": [29.0, 54.0, 50.0, 4.0, 7.0],
}

# subtract base_data from ff_data_needs_destack
ff_data = {
    k: [v[i] - base_data[k][i] for i in range(len(v))]
    for k, v in ff_data_needs_destack.items()
}
# Create the visualization
fig, ax = plt.subplots(figsize=(18, 10))

# Define colors for each model - base (much darker) and FF (current base colors) versions
model_colors = {
    "Aria 25B": {
        "base": "#7B241C",
        "ff": "#C0392B",
    },  # Very dark red / Previous base red
    "Claude 4": {
        "base": "#1B4F72",
        "ff": "#2980B9",
    },  # Very dark blue / Previous base blue
    "GPT-5": {
        "base": "#186A3B",
        "ff": "#27AE60",
    },  # Very dark green / Previous base green
    "Llava 7B": {
        "base": "#8B6914",
        "ff": "#D68910",
    },  # Very dark orange / Previous base orange
    "Molmo 7B": {
        "base": "#5B2C6F",
        "ff": "#8E44AD",
    },  # Very dark purple / Previous base purple
}

# Set up the plot - group by task
x = np.arange(len(tasks))
width = 0.15  # Increased width to reduce space between groups

# Create bars for each model within each task
for i, model in enumerate(models):
    base_values = [base_data[task][i] for task in tasks]
    ff_values = [ff_data[task][i] for task in tasks]

    # Get hardcoded colors for this model
    base_color = model_colors[model]["base"]
    ff_color = model_colors[model]["ff"]

    # Create stacked bars
    ax.bar(
        x + i * width,
        base_values,
        width,
        label=f"{model} (Base)" if i == 0 else "",
        color=base_color,
        alpha=0.9,
        edgecolor="white",
        linewidth=1,
    )

    ax.bar(
        x + i * width,
        ff_values,
        width,
        bottom=base_values,
        label=f"{model} (+ FF)" if i == 0 else "",
        color=ff_color,
        alpha=0.9,
        edgecolor="white",
        linewidth=1,
    )

# Customize the plot
ax.set_ylabel("Field Completion (%)", fontsize=28, fontweight="bold", color="black")

# Set x-axis labels
ax.set_xticks(x + width * 2)  # Center the labels
task_labels = [
    "Auto Loans\n(Text)\nOne Shot",
    "Auto Loans\n(Text)\nIterative",
    "Auto Loans\n(Doc)\nOne Shot",
    "Auto Loans\n(Doc)\nIterative",
    "FUNSD\nOne Shot",
    "XFUND\nOne Shot",
    "Form-NLU\nOne Shot",
]
ax.set_xticklabels(task_labels, rotation=45, ha="right", fontsize=24, color="black")

# Remove the base model +FF legend - we'll use the model legend instead

# Add grid for better readability
ax.grid(True, alpha=0.3, linestyle="--", axis="y")
ax.set_axisbelow(True)

# Add model labels above the bars
for i, model in enumerate(models):
    for j, task in enumerate(tasks):
        base_val = base_data[task][i]
        ff_val = ff_data[task][i]
        total_val = base_val + ff_val

        # Add percentage labels on every column
        if total_val > 0:  # Only show if there's a value
            ax.text(
                x[j] + i * width,
                total_val + 1,
                f"{total_val:.1f}",
                ha="center",
                va="bottom",
                fontsize=16,
                fontweight="bold",
                color="black",
            )

# Styling improvements
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#BDC3C7")
ax.spines["bottom"].set_color("#BDC3C7")

# Make y-axis tick labels black
ax.tick_params(axis="y", colors="black")

# Set y-axis limits to 55
ax.set_ylim(0, 55)

# Add subtle background color
ax.set_facecolor("white")
fig.patch.set_facecolor("white")

# Add model legend at the top left with both base and FF colors
# Create 5 rows of 2 columns: base model on left, FF on right
model_legend_elements = []
for model in models:
    # Add base color (left column)
    model_legend_elements.append(
        mpatches.Patch(
            color=model_colors[model]["base"], alpha=0.9, label=f"{model} (base)"
        )
    )
for model in models:
    # Add FF color (right column)
    model_legend_elements.append(
        mpatches.Patch(
            color=model_colors[model]["ff"], alpha=0.9, label=f"{model} (+FF)"
        )
    )


# Add model legend at top left
ax.legend(
    handles=model_legend_elements,
    loc="upper left",
    ncol=2,  # Two columns for base and FF
    fontsize=18,
    framealpha=0.9,
)

# Adjust layout to prevent label cutoff
plt.tight_layout()

# Save the plot
plt.savefig(
    "/local/data/mt/FormGym/analysis/model_performance_comparison.png",
    dpi=300,
    bbox_inches="tight",
    facecolor="white",
    edgecolor="none",
)

# Show the plot
plt.show()

print(
    "Beautiful stacked bar chart created and saved as 'model_performance_comparison.png'"
)
