# White Text Plot Examples

This notebook shows how to modify your existing plotting code to use white text for better GitHub visibility.

## Option 1: Global matplotlib settings (Easiest)

```python
import matplotlib.pyplot as plt
import matplotlib as mpl

# Apply this at the beginning of your notebook
def setup_white_text_theme():
    """Configure matplotlib to use white text for better GitHub visibility."""
    
    # Set the default text color to white
    mpl.rcParams['text.color'] = 'white'
    mpl.rcParams['axes.labelcolor'] = 'white'
    mpl.rcParams['xtick.color'] = 'white'
    mpl.rcParams['ytick.color'] = 'white'
    mpl.rcParams['axes.edgecolor'] = 'white'
    mpl.rcParams['figure.facecolor'] = 'black'
    mpl.rcParams['axes.facecolor'] = 'black'
    mpl.rcParams['axes.titlecolor'] = 'white'
    mpl.rcParams['legend.facecolor'] = 'black'
    mpl.rcParams['legend.edgecolor'] = 'white'

# Call this once at the start
setup_white_text_theme()

# Now all your existing plots will use white text!
```

## Option 2: Use built-in dark style

```python
import matplotlib.pyplot as plt

# Use matplotlib's built-in dark background style
plt.style.use('dark_background')

# Now all your plots will have white text on dark background
```

## Option 3: Modify individual plots

```python
# For your existing geopandas plots, add these lines after plotting:
fig, ax = plt.subplots(figsize=(15, 10))

# Your existing plotting code here...
# gdf.plot(ax=ax, column='some_column', cmap='viridis', legend=True)

# Add white text modifications:
ax.tick_params(colors='white')
ax.set_title('Your Plot Title', color='white', fontsize=16)
fig.patch.set_facecolor('black')
ax.set_facecolor('black')

# For spines (plot borders)
for spine in ax.spines.values():
    spine.set_color('white')

# Save with black background
plt.savefig('your_plot.png', facecolor='black', bbox_inches='tight')
```

## Quick Fix Instructions

1. **Easiest approach**: Add this line at the top of your plotting notebooks:
   ```python
   plt.style.use('dark_background')
   ```

2. **Then re-run the cells** that generate:
   - age_1.png
   - all_nonitri%.png  
   - PE_1000_people.png
   - topo_points_tech.png
   - WWTPS_1000_people.png

3. **The files will be regenerated** with white text automatically!

## Files to Update

Based on your search results, you need to update these notebooks:
- `oebo_plots.ipynb` (generates age_1.png)
- Check other workflow files for the remaining PNG files

## Alternative: Manual Tools

If you prefer not to regenerate, you could use image editing tools like:
- GIMP (free)
- Photoshop  
- Online tools like Canva or Figma
- Python PIL/Pillow for programmatic editing

But regenerating the plots is the cleanest approach!
