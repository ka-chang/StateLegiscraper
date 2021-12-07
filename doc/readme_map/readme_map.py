"""
Generate US map for readme that denotes state coverage 
"""

import geopandas as gpd
import matplotlib.pyplot as plt

#shp from https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html

fig = gpd.read_file("cb_2018_us_state_500k.shp")
fig = fig.assign(COVERAGE=0)

fig.loc[11, "COVERAGE"] = 1 #Washington
fig.loc[28, "COVERAGE"] = 1 #Nevada

map_states = fig.plot(figsize=(30, 15), column="COVERAGE", cmap="Set3", edgecolor='black')
map_states.set_ylim([25, 50])
map_states.set_xlim([-128, -66])
map_states.axis('off')

final = map_states.get_figure()
final.tight_layout()
final.savefig("readme_map.png")
