# Python Notebook - US Orders Heatmap

"""
# New Notebook
"""

import folium
from folium.plugins import HeatMap, HeatMapWithTime
from folium import Icon
import pandas as pd
import numpy as np

df = datasets[0]

df1= df[['BUYER_CITY', 'LATITUDE', 'LONGITUDE', 'ORDERS']]

df2 = df1.dropna(subset=['LATITUDE', 'LONGITUDE', 'ORDERS'])

# Add a new column for log-transformed order volume
df2['LogOrders'] = np.log10(df2['ORDERS'] + 1)

# Optional: scale to 0–1 if needed
df2['NormalizedOrders'] = df2['LogOrders'] / df2['LogOrders'].max()
print(df2.sample)

print(df2.isna().sum())

# Create map
m = folium.Map(location=[39.8283, -98.5795], zoom_start=5)

# Add heatmap
heat_data = [[row['LATITUDE'], row['LONGITUDE'], row['NormalizedOrders']] for index, row in df2.iterrows()]
HeatMap(
  heat_data,
  min_opacity=0.2,
  radius=20,     # ↑ = larger "glow"
  blur=15,       # ↑ = smoother transitions
  max_zoom=5,
  gradient={0.2: 'blue', 0.4: 'lime', 0.6: 'orange', 0.8: 'red'}  # Custom color gradient
).add_to(m)

top20 = df2.nlargest(20, 'ORDERS')

for index, row in top20.iterrows():
    folium.Marker(
        location=[row['LATITUDE'], row['LONGITUDE']],
        popup=folium.Popup(f"Total Orders: {row['ORDERS']}", max_width=250),
        tooltip=f"Total Orders: {row['ORDERS']}",
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
<b>Order Volume</b><br>
<span style="background:blue; width:15px; height:10px; display:inline-block;"></span> 1–1,000<br>
<span style="background:lime; width:15px; height:10px; display:inline-block;"></span> 1,001–10,000<br>
<span style="background:orange; width:15px; height:10px; display:inline-block;"></span> 10,001–100,000<br>
<span style="background:red; width:15px; height:10px; display:inline-block;"></span> 100,001–1,000,000+
</div>
'''

m.get_root().html.add_child(folium.Element(legend_html))

display(m)


# Add small circle markers with order labels
# for _, row in df2.iterrows():
#     label = f"{row['BUYER_CITY']}: {int(row['ORDERS'])} orders"
#     folium.CircleMarker(
#         location=[row['LATITUDE'], row['LONGITUDE']],
#         radius=1,  # Size of the marker
#         color='white',
#         fill=False,
#         # fill_color='blue',
#         fill_opacity=0.7,
#         popup=folium.Popup(label, max_width=150)
#     ).add_to(m)

# Add always-visible labels (no icon, just label)
# for _, row in df2.iterrows():
#     folium.Marker(
#         location=[row['LATITUDE'], row['LONGITUDE']],
#         icon=folium.DivIcon(html=""),  # empty icon to hide default marker
#         tooltip=folium.Tooltip(
#             f"{row['BUYER_CITY']}: {int(row['ORDERS'])} orders",
#             permanent=True,
#             direction='top',
#             offset=(0, -10),
#             sticky=True
#         )
#     ).add_to(m)
    

