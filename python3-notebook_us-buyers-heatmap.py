# Python Notebook - US Buyers Heatmap

"""
# New Notebook
"""

import folium
from folium.plugins import HeatMap, HeatMapWithTime
from folium import Icon
import pandas as pd
import numpy as np

df = datasets[0]

df1= df[['BUYER_CITY', 'LATITUDE', 'LONGITUDE', 'BUYER_COUNT']]

df2 = df1.dropna(subset=['LATITUDE', 'LONGITUDE', 'BUYER_COUNT'])

# Add a new column for log-transformed order volume
df2['LogBuyers'] = np.log10(df2['BUYER_COUNT'] + 1)

# Optional: scale to 0–1 if needed
df2['NormalizedBuyers'] = df2['LogBuyers'] / df2['LogBuyers'].max()
print(df2.sample)

print(df2.isna().sum())

# Create map
m = folium.Map(location=[39.8283, -98.5795], zoom_start=5)

# Add heatmap
heat_data = [[row['LATITUDE'], row['LONGITUDE'], row['NormalizedBuyers']] for index, row in df2.iterrows()]

# Add heatmap layer
HeatMap(
  heat_data,
  min_opacity=0.2,
  radius=20,     # ↑ = larger "glow"
  blur=15,       # ↑ = smoother transitions
  max_zoom=5,
  gradient={0.2: 'blue', 0.4: 'lime', 0.6: 'orange', 0.8: 'red'}  # Custom color gradient
).add_to(m)

# Add top 10 lables
top10 = df2.nlargest(20, 'BUYER_COUNT')

for index, row in top10.iterrows():
    folium.Marker(
        location=[row['LATITUDE'], row['LONGITUDE']],
        popup=folium.Popup(f"buyer count: {row['BUYER_COUNT']}", max_width=250),
        tooltip=f"buyer count: {row['BUYER_COUNT']}",
        icon=Icon(
            color='red',        # Marker color (red, green, blue, purple, orange, darkred, etc.)
            icon='star',        # Icon type (use 'star', 'trophy', 'fire', 'shopping-cart', etc.)
            prefix='fa'         # Use Font Awesome icons ('fa')
        )
    ).add_to(m)

legend_html = '''
<div style="
    position: fixed; 
    bottom: 50px; left: 50px; width: 200px; height: 100px; 
    background-color: transparent; 
    border:0px solid grey; 
    z-index:9999; 
    font-size:10px;
    padding: 8px;
">
<b>Buyers Count</b><br>
<i style="background: rgba(0, 0, 255, 0.8); width: 18px; height: 10px; display: inline-block;"></i>&nbsp; 1–5,000<br>
<i style="background: rgba(0, 255, 255, 0.8); width: 18px; height: 10px; display: inline-block;"></i>&nbsp; 5,000–20,000<br>
<i style="background: rgba(0, 255, 0, 0.8); width: 18px; height: 10px; display: inline-block;"></i>&nbsp; 20,000–50,000<br>
<i style="background: rgba(255, 255, 0, 0.8); width: 18px; height: 10px; display: inline-block;"></i>&nbsp; 50,000–75,000<br>
<i style="background: rgba(255, 0, 0, 0.8); width: 18px; height: 10px; display: inline-block;"></i>&nbsp; 75,000–<br>
</div>
'''

m.get_root().html.add_child(folium.Element(legend_html))

display(m)




