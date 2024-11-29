#!/usr/bin/env python
# coding: utf-8

# In[234]:


import os
print(os.getcwd())  # Prints the current working directory
import pandas as pd

path = '/Users/shatakshibhatnagar/Downloads/HexagonDSRS/synthetic_data (7) (1) (1).xlsx'
synthetic_df = pd.read_excel(path)

hex_map_data_path = '/Users/shatakshibhatnagar/Downloads/HexagonDSRS/Polygonic Hex Map New.xlsx'
hex_df = pd.read_excel(hex_map_data_path, sheet_name='Sheet1')


# In[236]:


EXTENDED_PALETTE = [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
    '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
    '#393b79', '#637939', '#8c6d31', '#843c39', '#7b4173',
    '#5254a3', '#9c9ede', '#637939', '#e7969c', '#e6550d',
    '#e7ba52', '#31a354', '#756bb1', '#636363', '#9e9ac8',
    '#5254a3', '#6b6ecf', '#bd9e39', '#9edae5', '#3182bd',
    '#6baed6', '#9ecae1', '#c6dbef', '#e6550d', '#fd8d3c',
    '#fdae6b', '#fdd0a2', '#31a354', '#74c476', '#a1d99b',
    '#c7e9c0', '#756bb1', '#9e9ac8', '#bcbddc', '#dadaeb',
    '#636363', '#969696', '#bdbdbd', '#d9d9d9'
]
from bokeh.palettes import Category20
EXTENDED_PALETTE = Category20[20]


# In[240]:


from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, TapTool
from bokeh.layouts import row
from bokeh.palettes import Category20c
from bokeh.transform import cumsum
import math
from math import pi, cos, sin
import pandas as pd
from bokeh.palettes import Viridis256
from bokeh.palettes import Pastel1


# Step 1: Aggregated data for pie chart
# Confirm that synthetic_df contains columns: 'state', 'subcategory', and a numeric column to aggregate.
agg_data = synthetic_df.groupby(['state', 'subcategory']).size().reset_index(name='Count')

# Add a column for percentages
agg_data['percentage'] = (agg_data['Count'] / agg_data.groupby('state')['Count'].transform('sum')) * 100

# Step 2: Generate Hexagon Coordinates
centroids = hex_df.groupby('State')[['X', 'Y']].mean().to_dict(orient='index')
hex_data = {
    'x': [],
    'y': [],
    'state': [],
    'abbreviation': [],
    'color': [],
    'centroid_x': [],  # Add centroid X coordinates
    'centroid_y': [] 
}

# Generate unique colors for states
unique_states = hex_df['State'].unique()
hex_colors = Category20c[len(unique_states)] if len(unique_states) <= 20 else Category20c[20]
state_colors = {state: hex_colors[i % len(hex_colors)] for i, state in enumerate(unique_states)}

# Generate hexagon coordinates for states
for state, coords in centroids.items():
    hex_coords = [(coords['X'] + 0.8 * math.cos(2 * pi * i / 6), coords['Y'] + 0.8 * math.sin(2 * pi * i / 6)) for i in range(6)]
    hex_x, hex_y = zip(*hex_coords)
    hex_data['x'].append(list(hex_x) + [hex_x[0]])
    hex_data['y'].append(list(hex_y) + [hex_y[0]])
    hex_data['state'].append(state)
    if state in hex_df['State'].values:
        hex_data['abbreviation'].append(hex_df[hex_df['State'] == state]['Abbreviation'].iloc[0])
    else:
        hex_data['abbreviation'].append('N/A')
    hex_data['color'].append(state_colors[state])
    hex_data['centroid_x'].append(coords['X'])  # Use X centroid for labels
    hex_data['centroid_y'].append(coords['Y'])  # Use Y centroid for labels

hex_source = ColumnDataSource(hex_data)

# Step 3: Initialize Pie Chart Data
pie_source = ColumnDataSource(data=dict(subcategory=[], angle=[], pie_color=[], percentage_label=[], x_label=[], y_label=[]))

# Step 4: Hexagon Plot
hex_plot = figure(title="Hexagon Plot with State Abbreviations", tools="tap", tooltips="@state", width=1200, height=900)
hex_plot.add_tools(TapTool())
hex_plot.patches('x', 'y', source=hex_source, fill_alpha=0.8, fill_color='color', line_color="white")

hex_plot.text(
    x='centroid_x', y='centroid_y', text='abbreviation',
    source=hex_source, text_align="center", text_baseline="middle",
    text_color="black", text_font_size="10pt"
)

hex_plot.axis.visible = False
hex_plot.grid.grid_line_color = None

from bokeh.models import LabelSet
# Step 5: Pie Chart Plot
pie_chart = figure(title="Pie Chart", width=400, height=400, tools="")
pie_chart.wedge(
    x=0, y=0, radius=0.8,
    start_angle='start_angle',
    end_angle='end_angle',
    line_color="white",
    fill_color='pie_color',
    source=pie_source,
    legend_field='subcategory'
)

pie_chart.axis.visible = False
pie_chart.grid.grid_line_color = None

# Add labels for percentages
labels = LabelSet(
    x='x_label', y='y_label', text='percentage_label',
    source=pie_source,
    text_align='center', text_baseline='middle',
    text_font_size="10pt", text_color="black"
)

pie_chart.add_layout(labels)

def update_pie_chart(attr, old, new):
    selected = hex_source.selected.indices
    if not selected:
        # Clear pie chart if no hexagon is selected
        pie_source.data = dict(
            subcategory=[], start_angle=[], end_angle=[], pie_color=[], percentage_label=[], x_label=[], y_label=[]
        )
        pie_chart.title.text = "No State Selected"
        return

    selected_state = hex_source.data['state'][selected[0]]
    print(f"Selected State: {selected_state}")
    state_data = agg_data[agg_data['state'] == selected_state]

    if state_data.empty:
        # Handle missing data for the selected state
        print(f"No subcategories found for {selected_state}.")
        pie_source.data = dict(
            subcategory=[], start_angle=[], end_angle=[], pie_color=[], percentage_label=[], x_label=[], y_label=[]
        )
        pie_chart.title.text = f"No Data Available for {selected_state.capitalize()}"
        return

    # Calculate angles and cumulative sum for the pie chart
    state_data = state_data.copy()
    state_data['angle'] = state_data['percentage'] / 100 * 2 * pi
    state_data['start_angle'] = state_data['angle'].cumsum().shift(fill_value=0)
    state_data['end_angle'] = state_data['start_angle'] + state_data['angle']
    state_data['percentage_label'] = state_data['percentage'].round(1).astype(str) + '%'  # Format percentages


    # Dynamically assign lighter colors to each subcategory
    num_categories = len(state_data)
    palette = list(Pastel1[8])  # Use Pastel1 for lighter colors, max size is 8
    if num_categories > len(palette):  # Extend the palette if needed
        palette = (palette * (num_categories // len(palette) + 1))[:num_categories]
    state_data['pie_color'] = palette[:num_categories] 

    # Compute label positions
    state_data['x_label'] = [
        0.4 * math.cos(state_data['start_angle'].iloc[i] + state_data['angle'].iloc[i] / 2)
        for i in range(len(state_data))
    ]
    state_data['y_label'] = [
        0.4 * math.sin(state_data['start_angle'].iloc[i] + state_data['angle'].iloc[i] / 2)
        for i in range(len(state_data))
    ]

    # Convert pandas Series to lists for Bokeh compatibility
    pie_source.data = {
        'subcategory': state_data['subcategory'].tolist(),
        'start_angle': state_data['start_angle'].tolist(),
        'end_angle': state_data['end_angle'].tolist(),
        'pie_color': state_data['pie_color'].tolist(),  # Explicitly convert to list
        'percentage_label': state_data['percentage_label'].tolist(),
        'x_label': state_data['x_label'],  # Already computed as lists
        'y_label': state_data['y_label'],  # Already computed as lists
    }
    pie_chart.title.text = f"Subcategory Distribution for {selected_state.capitalize()}"
    print(f"Pie Source Data: {pie_source.data}")  # Debugging line


# Attach the callback
hex_source.selected.on_change('indices', update_pie_chart)
 
# Step 7: Layout and Show
curdoc().add_root(row(hex_plot, pie_chart))


# In[ ]:




