import os
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import rasterio

from envoi import extract, init_gee

# Set the output directory
OUTPUT_DIR = Path("walkthrough_output")
os.getcwd()
os.chdir("/Users/migre740/Desktop/NBIS_projects/andermann_sdm/envoi/examples")

init_gee()
gbif_points = pd.read_csv("walkthrough_input/sample_points.csv", delimiter="\t")


points = gbif_points[["occurrenceID", "decimalLatitude", "decimalLongitude", "eventDate"]]


extract(
    points,
    {
        "batch_id": "terrain_stats",
        "datasets": ["dem_copernicus_glo30"],
        "settings": {
            "output_type": "tabular",
            "statistics": ["mean", "std"],
            "window_size_m": 500,
        },
    },
    output_dir=OUTPUT_DIR,
)

pd.read_csv(OUTPUT_DIR / "terrain_stats.csv")


extract(
    points,
    {
        "batch_id": "terrain_tiles",
        "datasets": ["dem_copernicus_glo30"],
        "settings": {
            "output_type": "raster",
            "window_size_m": 500,
            "resample_m": 10,
        },
    },
    output_dir=OUTPUT_DIR,
)

tiles = sorted((OUTPUT_DIR / "terrain_tiles" / "dem_copernicus_glo30").glob("*.tif"))


fig, ax = plt.subplots(figsize=(4, 4))
with rasterio.open(tiles[0]) as src:
    im = ax.imshow(src.read(1), cmap="Greys")
ax.set_title(tiles[0].stem.split("-")[0], fontsize=9)
ax.set_axis_off()
fig.colorbar(im, ax=ax, label="Elevation (m)", shrink=0.8)
fig.suptitle("dem_copernicus_glo30")
plt.tight_layout()
plt.show()


sample_points = pd.DataFrame(
    {
        "occurrenceID": ["a", "b", "c"],
        "decimalLatitude": [59.85, 59.86, 59.87],
        "decimalLongitude": [17.63, 17.64, 17.65],
        "decimalLatitudesweref99": [6580000, 6581000, 6582000],
        "decimalLongitudesweref99": [162000, 163000, 164000],
    }
)

outputs = extract(
    sample_points,
    {
        "batch_id": "terrain",
        "datasets": ["dem_copernicus_glo30"],
        "settings": {
            "output_type": "tabular",
            "statistics": ["mean", "std"],
            "window_size_m": 200,
        },
    },
)

sample_points_sweref = pd.read_csv(
    "/Users/migre740/Desktop/NBIS_projects/andermann_sdm/envoi/examples/sample_example_MR_correct_sweref.csv"
)

outputs = extract(
    sample_points_sweref,
    {
        "batch_id": "terrain",
        "datasets": ["dem_copernicus_glo30"],
        "settings": {
            "output_type": "tabular",
            "statistics": ["mean", "std"],
            "window_size_m": 200,
        },
    },
    input_crs="EPSG:3006",
    output_dir="/Users/migre740/Desktop/NBIS_projects/andermann_sdm/envoi/examples",
)
