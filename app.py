import streamlit as st
from utils import get_pokemon_data, get_pokemon_species_data
import plotly.graph_objects as go
from PIL import Image
import requests
from io import BytesIO
import random

st.set_page_config(page_title="Pokémon Explorer", layout="wide")
st.title("⚡ Pokémon Explorer")

# Random Pokémon feature
if st.button("Surprise Me!"):
    pokemon_name = str(random.randint(1, 1010))  # Total Pokémon in API
else:
    pokemon_name = st.text_input("Enter Pokémon Name or ID")

if pokemon_name:
    data = get_pokemon_data(pokemon_name)
    if data:
        st.subheader(f"{data['name'].title()} (ID: {data['id']})")

        # Show Images
        images = [
            data['sprites']['front_default'],
            data['sprites']['back_default'],
            data['sprites']['other']['official-artwork']['front_default']
        ]
        cols = st.columns(len(images))
        for i, img_url in enumerate(images):
            if img_url:
                response = requests.get(img_url)
                img = Image.open(BytesIO(response.content))
                cols[i].image(img)

        # Show Types
        types = [t['type']['name'].title() for t in data['types']]
        st.markdown(f"**Type:** {' | '.join(types)}")

        # Show Stats using Plotly
        stats = {stat['stat']['name'].title(): stat['base_stat'] for stat in data['stats']}
        fig = go.Figure(go.Bar(x=list(stats.keys()), y=list(stats.values()), marker_color='orange'))
        fig.update_layout(title="Base Stats", yaxis_title="Value", xaxis_title="Stat")
        st.plotly_chart(fig, use_container_width=True)

        # Evolution Chain
        evo_chain = get_pokemon_species_data(data['id'])
        if evo_chain:
            st.markdown(f"**Evolution Chain:** {' → '.join([p.title() for p in evo_chain])}")
    else:
        st.error("Pokémon not found. Try another name or ID.")