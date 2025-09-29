import folium

def create_map(locations, output_path="../output/ip_map.html"):
    map_ = folium.Map(location=[20, 0], zoom_start=2)

    for loc in locations:
        print(loc)  # Debug output
        if "latitude" in loc and "longitude" in loc:
            folium.Marker(
                location=[loc["latitude"], loc["longitude"]],
                popup=f'{loc["ip"]} ({loc.get("city", "Unknown")}, {loc.get("country", "Unknown")})'
            ).add_to(map_)

    for loc in locations:
        if "latitude" in loc and "longitude" in loc:
            folium.Marker(
                location=[loc["latitude"], loc["longitude"]],
                popup=f'{loc["ip"]} ({loc.get("city", "Unknown")}, {loc.get("country", "Unknown")})'
            ).add_to(map_)

    map_.save(output_path)
    print(f"Map saved to {output_path}")

