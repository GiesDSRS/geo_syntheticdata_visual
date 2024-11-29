# Hexagon and Pie Chart Visualization with Bokeh

## Overview
This project visualizes state-wise data using an **interactive hexagon plot** and a corresponding **dynamic pie chart**. The visualization updates in real-time based on user interaction. Selecting a state from the hexagon plot triggers a pie chart update to show the distribution of subcategories for the selected state.

---

## Features
- **Hexagon Plot**:
  - Interactive hexagons representing states.
  - State abbreviations displayed at hexagon centroids.
  - Dynamic tooltip displaying state names.

- **Dynamic Pie Chart**:
  - Displays the subcategory distribution for a selected state.
  - Color-coded segments using the `Pastel1` palette.
  - Percentage labels dynamically calculated and displayed for each segment.

---

## Data Sources

### 1. **Synthetic Data (`synthetic_df`)**
The synthetic dataset represents state-wise subcategories and counts:
- **Columns**:
  - `state`: Names of states.
  - `subcategory`: Categories (e.g., "Education", "Health").
  - `Count`: Numerical value indicating the count for each subcategory in a state.

### 2. **Geographic Data (`hex_df`)**
The geographic dataset includes state-wise coordinates:
- **Columns**:
  - `State`: Names of states.
  - `X`: X-coordinates for hexagon centroids.
  - `Y`: Y-coordinates for hexagon centroids.
  - `Abbreviation`: Two-letter state abbreviations.

These datasets are merged in the visualization logic to link subcategory data with geographic coordinates for hexagon plotting.

---

## Installation

### Prerequisites
- Python 3.7 or later
- Required libraries: [Bokeh](https://bokeh.pydata.org/), Pandas

### Installation Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/hexagon-pie-chart.git
   cd hexagon-pie-chart
