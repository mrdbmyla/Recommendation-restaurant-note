import streamlit as st
import pandas as pd
import requests
import folium
from streamlit_folium import st_folium
from pathlib import Path

st.set_page_config(page_title="Carte des restaurants à proximité", layout="wide")
st.sidebar.caption("Sélectionnez une page")
st.markdown(
    """
    <h2 style="text-align: center;">Carte des restaurants à proximité</h2>
    <p style="text-align: center; font-size: 16px;">
        👉 Cette page permet de visualiser les restaurants du même type que le votre à proximité de votre position.
    </p>
    """,
    unsafe_allow_html=True
)

headers = {"User-Agent": "Mozilla/5.0 (Streamlit app)"}

def API_adresse(adresse_postale):
    link = (
        "https://nominatim.openstreetmap.org/search?q="
        + adresse_postale.replace(" ", "+")
        + "&format=json&limit=1"
    )
    try:
        r = requests.get(link, headers=headers, timeout=15)
        if r.status_code != 200:
            return None, None
        r = r.json()
    except (requests.RequestException, ValueError):
        return None, None
    if not r:
        return None, None
    return float(r[0]["lat"]), float(r[0]["lon"])

BASE_DIR = Path(__file__).resolve().parents[1]  # remonte de pages/ -> projet/
df = pd.read_csv(BASE_DIR / "P3_ML3v6.csv")

with st.form("search_form"):
 address = st.text_input("Entrez une adresse : ")
 user_cuisine = st.selectbox("Type de restaurant", df.columns[6:72])
 submit = st.form_submit_button("Rechercher")

 if not submit:
    st.stop()

if not address:
    st.stop()

lat, lon = API_adresse(address)

if lat is None:
    st.stop()

rayon = 250

query = f"""
[out:json][timeout:25];
(
  node["amenity"="restaurant"](around:{rayon},{lat},{lon});
  way["amenity"="restaurant"](around:{rayon},{lat},{lon});
);
out tags center;
"""

overpass_urls = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
]

data = None

for url in overpass_urls:
    try:
        r = requests.get(url, params={"data": query}, headers=headers, timeout=30)
        if r.status_code != 200:
            continue
        data = r.json()
        break
    except (requests.RequestException, ValueError):
        continue

if data is None:
    st.stop()

m = folium.Map(location=[lat, lon], zoom_start=17)

folium.Marker(
    [lat, lon],
    popup="Moi",
    tooltip="Ma position",
    icon=folium.Icon(color="green", icon="user", prefix="fa")
).add_to(m)

for element in data.get("elements", []):
    tags = element.get("tags", {})
    if "lat" in element:
        r_lat, r_lon = element["lat"], element["lon"]
    else:
        center = element.get("center")
        if not center:
            continue
        r_lat, r_lon = center["lat"], center["lon"]

    name = tags.get("name", "Restaurant inconnu")
    cuisine = tags.get("cuisine", "Cuisine inconnue")
    color = "red" if user_cuisine.lower() in cuisine.lower() else "blue"

    folium.Marker(
        [r_lat, r_lon],
        popup=f"{name}\nCuisine : {cuisine}",
        tooltip=name,
        icon=folium.Icon(color=color, icon="cutlery", prefix="fa")
    ).add_to(m)

col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st_folium(m, width=1250, returned_objects=[])
