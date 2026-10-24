"""
Project: geoIP-log-mapper

File: visualize.py

Description: Generates an interactive, self-contained HTML
             map using Plotly to visualize the approximate
             geographic locations of extracted IP addresses.

Created by: Gavin Main

Date Finalized: 10/23/26
"""

from pathlib import Path
import plotly.graph_objects as go


def create_map(locations, output_path="../output/ip_map.html"):
    
    # Ensure the output directory exists.
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Filter locations with valid coordinates.
    valid_locations = []

    for loc in locations:
        try:
            lat = float(loc["latitude"])
            lon = float(loc["longitude"])

            if not (-90 <= lat <= 90 and -180 <= lon <= 180):
                continue

            valid_locations.append({
                "latitude": lat,
                "longitude": lon,
                "ip": loc.get("ip", "Unknown"),
                "city": loc.get("city", "Unknown"),
                "country": loc.get("country", "Unknown")
            })

        except (KeyError, TypeError, ValueError):
            continue

    # Build labels for each IP address.
    labels = [
        f"IP: {loc['ip']}<br>"
        f"City: {loc['city']}<br>"
        f"Country: {loc['country']}"
        for loc in valid_locations
    ]

    # Create an interactive geographic visualization.
    fig = go.Figure()

    fig.add_trace(go.Scattergeo(
        lat=[loc["latitude"] for loc in valid_locations],
        lon=[loc["longitude"] for loc in valid_locations],
        text=labels,
        mode="markers",
        hoverinfo="text",
        marker=dict(
            size=9,
            color="red",
            opacity=0.8,
            line=dict(width=1, color="white")
        )
    ))

    fig.update_layout(
        title="GeoIP Log Mapper",
        geo=dict(
            scope="world",
            projection_type="natural earth",
            showland=True,
            landcolor="rgb(220, 225, 230)",
            showocean=True,
            oceancolor="rgb(190, 215, 235)",
            showcoastlines=True,
            coastlinecolor="rgb(100, 100, 100)",
            showcountries=True,
            countrycolor="rgb(120, 120, 120)",
            showframe=False
        ),
        margin=dict(l=10, r=10, t=50, b=10)
    )

    # Embed Plotly JavaScript into the HTML file.
    # This avoids dependence on external CDNs.
    fig.write_html(
        str(output_file),
        include_plotlyjs=True,
        full_html=True
    )

    print(f"Map saved to {output_file}")
    print(f"Plotted {len(valid_locations)} IP locations.")
