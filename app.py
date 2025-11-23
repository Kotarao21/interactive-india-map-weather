import folium
from geopy.geocoders import Nominatim
import requests

# -------------------------------
# 🔑 Replace with your OpenWeatherMap API Key
API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"
# -------------------------------

# Create a base map centered on India
india_map = folium.Map(location=[20.5937, 78.9629], zoom_start=5, tiles="OpenStreetMap")

# Function to get temperature using OpenWeatherMap API
def get_temperature(lat, lon):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        response = requests.get(url).json()
        if response.get("main"):
            return response["main"]["temp"]
        return None
    except:
        return None

# Function to get location details
def get_location(lat, lon):
    try:
        geolocator = Nominatim(user_agent="geoapi")
        location = geolocator.reverse((lat, lon), language="en")
        return location.address if location else "Unknown Location"
    except:
        return "Unknown Location"

# Add popup showing lat/lon when clicking
india_map.add_child(folium.LatLngPopup())

# Example: Add a marker at Delhi (to test functionality)
lat, lon = 28.6139, 77.2090
place = get_location(lat, lon)
temp = get_temperature(lat, lon)
temp_text = f"{temp} °C" if temp is not None else "Temperature not available"

folium.Marker(
    location=[lat, lon],
    popup=f"""
    📍 Location: {place}<br>
    🌍 Latitude: {lat}<br>
    🌍 Longitude: {lon}<br>
    🌡 Temperature: {temp_text}
    """,
    icon=folium.Icon(color="red", icon="info-sign")
).add_to(india_map)

# Save map as HTML
india_map.save("india_interactive_map.html")

print("✅ Map created! Open 'india_interactive_map.html' in your browser.")
