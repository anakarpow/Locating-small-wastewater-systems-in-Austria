#!/usr/bin/env python3
"""
Script to regenerate plots with white text for better GitHub visibility.
This script provides examples of how to modify matplotlib plots to use white text.
"""

import matplotlib.pyplot as plt
import matplotlib as mpl

# Set global matplotlib parameters for white text
def setup_white_text_theme():
    """Configure matplotlib to use white text for better GitHub visibility."""
    
    # Set the default text color to white
    mpl.rcParams['text.color'] = 'white'
    mpl.rcParams['axes.labelcolor'] = 'white'
    mpl.rcParams['xtick.color'] = 'white'
    mpl.rcParams['ytick.color'] = 'white'
    mpl.rcParams['axes.edgecolor'] = 'white'
    mpl.rcParams['figure.facecolor'] = 'black'  # Set figure background to black
    mpl.rcParams['axes.facecolor'] = 'black'    # Set axes background to black
    
    # For plot titles and labels
    mpl.rcParams['axes.titlecolor'] = 'white'
    
    # For legend
    mpl.rcParams['legend.facecolor'] = 'black'
    mpl.rcParams['legend.edgecolor'] = 'white'
    
    print("✓ White text theme configured for matplotlib")

def example_plot_modification():
    """Example of how to modify individual plots for white text."""
    
    # Example 1: For a simple plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Your plotting code here...
    # ax.plot(x, y)
    # ax.bar(categories, values)
    # etc.
    
    # Set colors explicitly for this plot
    ax.tick_params(colors='white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.title.set_color('white')
    
    # Set background colors
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    
    # For spines (plot borders)
    for spine in ax.spines.values():
        spine.set_color('white')
    
    # Save with transparent background or black background
    plt.savefig('example_plot_white_text.png', 
                facecolor='black',  # or 'transparent'
                bbox_inches='tight')
    plt.close()

def geopandas_plot_modification():
    """Example for GeoPandas plots (which seem to be used in your project)."""
    
    # For GeoPandas plots, you need to modify the matplotlib figure after plotting
    # Example:
    # fig, ax = plt.subplots(figsize=(15, 10))
    # gdf.plot(ax=ax, color='blue', alpha=0.7)
    
    # Then apply white text settings:
    # ax.tick_params(colors='white')
    # ax.set_title('Your Title', color='white', fontsize=16)
    # fig.patch.set_facecolor('black')
    # ax.set_facecolor('black')
    
    print("✓ See geopandas_plot_modification() function for GeoPandas examples")

if __name__ == "__main__":
    print("=== Plot Update Script for White Text ===")
    print()
    
    # Setup the global theme
    setup_white_text_theme()
    
    print("\nTo update your existing plots:")
    print("1. Run setup_white_text_theme() at the beginning of your notebook/script")
    print("2. Re-run your plotting code")
    print("3. The plots will automatically use white text")
    print()
    print("For individual plot control, see the example functions in this script.")
    print()
    print("Key files to update:")
    print("- oebo_plots.ipynb (generates age_1.png)")
    print("- Other workflow notebooks that generate the PNG files")
    print()
    print("Alternative: Use plt.style.use('dark_background') for a pre-made dark theme")
