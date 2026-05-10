import streamlit as st
from utils import (
    get_pokemon_data, 
    get_pokemon_species_data, 
    get_ability_data,
    get_move_data,
    compare_pokemon_stats,
    get_type_effectiveness,
    search_pokemon_by_type
)
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
import requests
from io import BytesIO
import random

# Page config
st.set_page_config(page_title="Pokémon Explorer Pro", layout="wide", page_icon="⚡")

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4, #FFE66D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 20px;
    }
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    .type-badge {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        margin: 5px;
        font-weight: bold;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'team' not in st.session_state:
    st.session_state.team = []
if 'comparison_list' not in st.session_state:
    st.session_state.comparison_list = []

# Title
st.markdown('<div class="main-header">⚡ Pokémon Explorer Pro 🎮</div>', unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("🎯 Navigation")
page = st.sidebar.radio("Select Mode", [
    "🔍 Single Pokémon Explorer",
    "⚔️ Compare Pokémon",
    "👥 Team Builder",
    "🎲 Type Explorer",
    "📊 Advanced Statistics"
])

# Type colors for badges
TYPE_COLORS = {
    'normal': '#A8A878', 'fire': '#F08030', 'water': '#6890F0', 'electric': '#F8D030',
    'grass': '#78C850', 'ice': '#98D8D8', 'fighting': '#C03028', 'poison': '#A040A0',
    'ground': '#E0C068', 'flying': '#A890F0', 'psychic': '#F85888', 'bug': '#A8B820',
    'rock': '#B8A038', 'ghost': '#705898', 'dragon': '#7038F8', 'dark': '#705848',
    'steel': '#B8B8D0', 'fairy': '#EE99AC'
}

def display_type_badge(type_name):
    """Display a colored type badge"""
    color = TYPE_COLORS.get(type_name.lower(), '#777777')
    return f'<span class="type-badge" style="background-color: {color};">{type_name.upper()}</span>'

def display_pokemon_card(data, show_detailed=True):
    """Display a comprehensive Pokémon card"""
    col1, col2, col3 = st.columns([1, 2, 2])
    
    with col1:
        # Display official artwork
        artwork_url = data['sprites']['other']['official-artwork']['front_default']
        if artwork_url:
            response = requests.get(artwork_url)
            img = Image.open(BytesIO(response.content))
            st.image(img, use_column_width=True)
    
    with col2:
        st.subheader(f"{data['name'].title()}")
        st.markdown(f"**ID:** #{data['id']:03d}")
        
        # Types with colored badges
        types = [t['type']['name'] for t in data['types']]
        type_html = ''.join([display_type_badge(t) for t in types])
        st.markdown(type_html, unsafe_allow_html=True)
        
        # Physical attributes
        st.markdown(f"**Height:** {data['height'] / 10:.1f} m")
        st.markdown(f"**Weight:** {data['weight'] / 10:.1f} kg")
        st.markdown(f"**Base Experience:** {data['base_experience']}")
        
        # Abilities
        st.markdown("**Abilities:**")
        for ability in data['abilities']:
            ability_name = ability['ability']['name'].replace('-', ' ').title()
            is_hidden = " (Hidden)" if ability['is_hidden'] else ""
            st.markdown(f"• {ability_name}{is_hidden}")
    
    with col3:
        # Stats visualization
        stats = {stat['stat']['name'].replace('-', ' ').title(): stat['base_stat'] 
                 for stat in data['stats']}
        
        # Radar chart for stats
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=list(stats.values()),
            theta=list(stats.keys()),
            fill='toself',
            name=data['name'].title(),
            line_color='rgb(255, 107, 107)'
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 255])),
            showlegend=True,
            title="Base Stats Radar",
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Total base stats
        total_stats = sum(stats.values())
        st.metric("Total Base Stats", total_stats)
    
    if show_detailed:
        # Detailed sections
        tab1, tab2, tab3, tab4 = st.tabs(["📈 Stats Breakdown", "🎯 Moves", "🧬 Breeding", "🔄 Evolution"])
        
        with tab1:
            # Bar chart for individual stats
            fig_bar = go.Figure()
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#F7DC6F', '#BB8FCE', '#85C1E2']
            
            for i, (stat_name, stat_value) in enumerate(stats.items()):
                fig_bar.add_trace(go.Bar(
                    x=[stat_name],
                    y=[stat_value],
                    name=stat_name,
                    marker_color=colors[i % len(colors)],
                    text=[stat_value],
                    textposition='auto'
                ))
            
            fig_bar.update_layout(
                title="Individual Base Stats",
                yaxis_title="Value",
                xaxis_title="Stat",
                showlegend=False,
                height=400
            )
            st.plotly_chart(fig_bar, use_container_width=True)
            
            # Stat analysis
            col1, col2 = st.columns(2)
            with col1:
                highest_stat = max(stats, key=stats.get)
                st.success(f"💪 Highest Stat: {highest_stat} ({stats[highest_stat]})")
            with col2:
                lowest_stat = min(stats, key=stats.get)
                st.info(f"📉 Lowest Stat: {lowest_stat} ({stats[lowest_stat]})")
        
        with tab2:
            # Display learnable moves
            st.subheader("Learnable Moves")
            
            # Get moves by learning method
            level_up_moves = []
            machine_moves = []
            egg_moves = []
            
            for move in data['moves'][:50]:  # Limit to 50 moves for performance
                move_name = move['move']['name'].replace('-', ' ').title()
                for version_detail in move['version_group_details']:
                    learn_method = version_detail['move_learn_method']['name']
                    if learn_method == 'level-up':
                        level = version_detail['level_learned_at']
                        level_up_moves.append((level, move_name))
                    elif learn_method == 'machine':
                        machine_moves.append(move_name)
                    elif learn_method == 'egg':
                        egg_moves.append(move_name)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**Level Up Moves**")
                level_up_moves.sort()
                for level, move in level_up_moves[:15]:
                    st.markdown(f"Lv{level}: {move}")
            
            with col2:
                st.markdown("**TM/HM Moves**")
                for move in machine_moves[:15]:
                    st.markdown(f"• {move}")
            
            with col3:
                st.markdown("**Egg Moves**")
                for move in egg_moves[:15]:
                    st.markdown(f"• {move}")
        
        with tab3:
            # Breeding information
            species_data = get_pokemon_species_data(data['id'])
            if species_data:
                st.subheader("Breeding Information")
                
                col1, col2 = st.columns(2)
                with col1:
                    # Egg groups
                    egg_groups = species_data.get('egg_groups', [])
                    if egg_groups:
                        egg_group_names = [eg['name'].replace('-', ' ').title() for eg in egg_groups]
                        st.markdown(f"**Egg Groups:** {', '.join(egg_group_names)}")
                    
                    # Gender rate
                    gender_rate = species_data.get('gender_rate', -1)
                    if gender_rate == -1:
                        st.markdown("**Gender:** Genderless")
                    else:
                        female_rate = (gender_rate / 8) * 100
                        male_rate = 100 - female_rate
                        st.markdown(f"**Gender Ratio:** ♀{female_rate:.1f}% / ♂{male_rate:.1f}%")
                
                with col2:
                    # Hatch counter
                    hatch_counter = species_data.get('hatch_counter', 0)
                    st.markdown(f"**Hatch Counter:** {hatch_counter}")
                    st.markdown(f"**Steps to Hatch:** ~{(hatch_counter + 1) * 255} steps")
                    
                    # Capture rate
                    capture_rate = species_data.get('capture_rate', 0)
                    st.markdown(f"**Capture Rate:** {capture_rate}")
                    
                    # Growth rate
                    growth_rate = species_data.get('growth_rate', {}).get('name', 'unknown')
                    st.markdown(f"**Growth Rate:** {growth_rate.replace('-', ' ').title()}")
        
        with tab4:
            # Evolution chain
            evo_chain = species_data.get('evolution_chain', [])
            if evo_chain and len(evo_chain) > 1:
                st.subheader("Evolution Chain")
                st.markdown(" → ".join([f"**{p.title()}**" for p in evo_chain]))
                
                # Display evolution sprites
                cols = st.columns(len(evo_chain))
                for i, poke_name in enumerate(evo_chain):
                    try:
                        evo_data = get_pokemon_data(poke_name.lower())
                        if evo_data:
                            sprite_url = evo_data['sprites']['other']['official-artwork']['front_default']
                            if sprite_url:
                                response = requests.get(sprite_url)
                                img = Image.open(BytesIO(response.content))
                                cols[i].image(img, caption=poke_name.title(), use_column_width=True)
                    except:
                        pass
            else:
                st.info("This Pokémon does not evolve.")

# ========================================
# PAGE 1: Single Pokémon Explorer
# ========================================
if page == "🔍 Single Pokémon Explorer":
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        pokemon_name = st.text_input("🔎 Enter Pokémon Name or ID", placeholder="e.g., Pikachu or 25")
    
    with col2:
        search_option = st.selectbox("Or choose a category", 
                                     ["", "Starter Pokémon", "Legendary", "Mythical", "Pseudo-Legendary"])
    
    with col3:
        if st.button("🎲 Random", use_container_width=True):
            pokemon_name = str(random.randint(1, 1010))
    
    # Predefined categories
    if search_option == "Starter Pokémon":
        starter_ids = [1, 4, 7, 152, 155, 158, 252, 255, 258, 387, 390, 393, 495, 498, 501]
        pokemon_name = str(random.choice(starter_ids))
    elif search_option == "Legendary":
        legendary_ids = [144, 145, 146, 150, 243, 244, 245, 249, 250, 377, 378, 379, 380, 381, 382, 383, 384]
        pokemon_name = str(random.choice(legendary_ids))
    elif search_option == "Mythical":
        mythical_ids = [151, 251, 385, 386, 489, 490, 491, 492, 493, 494]
        pokemon_name = str(random.choice(mythical_ids))
    elif search_option == "Pseudo-Legendary":
        pseudo_ids = [149, 248, 376, 398, 445, 635, 706, 784]
        pokemon_name = str(random.choice(pseudo_ids))
    
    if pokemon_name:
        with st.spinner("Loading Pokémon data..."):
            data = get_pokemon_data(pokemon_name)
            if data:
                display_pokemon_card(data, show_detailed=True)
                
                # Add to team button
                col1, col2 = st.columns([1, 4])
                with col1:
                    if st.button("➕ Add to Team"):
                        if len(st.session_state.team) < 6:
                            if data['id'] not in [p['id'] for p in st.session_state.team]:
                                st.session_state.team.append(data)
                                st.success(f"Added {data['name'].title()} to team!")
                            else:
                                st.warning("Already in team!")
                        else:
                            st.error("Team is full (max 6 Pokémon)")
                
                with col2:
                    if st.button("📊 Add to Comparison"):
                        if len(st.session_state.comparison_list) < 4:
                            if data['id'] not in [p['id'] for p in st.session_state.comparison_list]:
                                st.session_state.comparison_list.append(data)
                                st.success(f"Added {data['name'].title()} to comparison!")
                            else:
                                st.warning("Already in comparison!")
                        else:
                            st.error("Max 4 Pokémon for comparison")
            else:
                st.error("❌ Pokémon not found. Try another name or ID.")

# ========================================
# PAGE 2: Compare Pokémon
# ========================================
elif page == "⚔️ Compare Pokémon":
    st.header("Compare Pokémon Stats")
    
    if len(st.session_state.comparison_list) >= 2:
        # Display comparison
        pokemon_names = [p['name'].title() for p in st.session_state.comparison_list]
        st.subheader(f"Comparing: {' vs '.join(pokemon_names)}")
        
        # Create comparison visualization
        fig = go.Figure()
        
        stat_names = ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']
        
        for pokemon in st.session_state.comparison_list:
            stats_values = [stat['base_stat'] for stat in pokemon['stats']]
            fig.add_trace(go.Scatterpolar(
                r=stats_values,
                theta=stat_names,
                fill='toself',
                name=pokemon['name'].title()
            ))
        
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 255])),
            showlegend=True,
            title="Stats Comparison Radar",
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed comparison table
        st.subheader("Detailed Stats Comparison")
        
        comparison_data = {}
        for stat_name in stat_names:
            comparison_data[stat_name] = []
        
        comparison_data['Total'] = []
        comparison_data['Pokémon'] = pokemon_names
        
        for pokemon in st.session_state.comparison_list:
            total = 0
            for i, stat in enumerate(pokemon['stats']):
                value = stat['base_stat']
                comparison_data[stat_names[i]].append(value)
                total += value
            comparison_data['Total'].append(total)
        
        import pandas as pd
        df = pd.DataFrame(comparison_data)
        df = df[['Pokémon'] + stat_names + ['Total']]
        
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Type matchup comparison
        st.subheader("Type Matchup Analysis")
        cols = st.columns(len(st.session_state.comparison_list))
        
        for i, pokemon in enumerate(st.session_state.comparison_list):
            with cols[i]:
                st.markdown(f"**{pokemon['name'].title()}**")
                types = [t['type']['name'] for t in pokemon['types']]
                type_html = ''.join([display_type_badge(t) for t in types])
                st.markdown(type_html, unsafe_allow_html=True)
        
        # Clear comparison button
        if st.button("🗑️ Clear Comparison"):
            st.session_state.comparison_list = []
            st.rerun()
    else:
        st.info("Add at least 2 Pokémon to compare. Go to 'Single Pokémon Explorer' and click 'Add to Comparison'")
        
        # Show current comparison list
        if st.session_state.comparison_list:
            st.write(f"Current list ({len(st.session_state.comparison_list)}/4):")
            for p in st.session_state.comparison_list:
                st.write(f"• {p['name'].title()}")

# ========================================
# PAGE 3: Team Builder
# ========================================
elif page == "👥 Team Builder":
    st.header("Build Your Pokémon Team")
    
    if st.session_state.team:
        st.subheader(f"Your Team ({len(st.session_state.team)}/6)")
        
        # Display team members
        cols = st.columns(min(len(st.session_state.team), 3))
        
        for i, pokemon in enumerate(st.session_state.team):
            with cols[i % 3]:
                # Sprite
                sprite_url = pokemon['sprites']['other']['official-artwork']['front_default']
                if sprite_url:
                    response = requests.get(sprite_url)
                    img = Image.open(BytesIO(response.content))
                    st.image(img, use_column_width=True)
                
                st.markdown(f"**{pokemon['name'].title()}**")
                types = [t['type']['name'] for t in pokemon['types']]
                type_html = ''.join([display_type_badge(t) for t in types])
                st.markdown(type_html, unsafe_allow_html=True)
                
                if st.button(f"Remove", key=f"remove_{pokemon['id']}"):
                    st.session_state.team.remove(pokemon)
                    st.rerun()
        
        st.divider()
        
        # Team analysis
        st.subheader("📊 Team Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Type coverage
            st.markdown("**Type Coverage**")
            all_types = []
            for pokemon in st.session_state.team:
                for type_info in pokemon['types']:
                    all_types.append(type_info['type']['name'])
            
            type_counts = {}
            for t in all_types:
                type_counts[t] = type_counts.get(t, 0) + 1
            
            fig = go.Figure(data=[go.Pie(
                labels=list(type_counts.keys()),
                values=list(type_counts.values()),
                hole=.3
            )])
            fig.update_layout(title="Type Distribution", height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Average stats
            st.markdown("**Team Average Stats**")
            avg_stats = {
                'HP': 0, 'Attack': 0, 'Defense': 0,
                'Sp. Atk': 0, 'Sp. Def': 0, 'Speed': 0
            }
            
            for pokemon in st.session_state.team:
                for stat in pokemon['stats']:
                    stat_name = stat['stat']['name'].replace('special-', 'Sp. ').replace('-', ' ').title()
                    if 'Hp' in stat_name:
                        stat_name = 'HP'
                    avg_stats[stat_name] += stat['base_stat']
            
            team_size = len(st.session_state.team)
            for key in avg_stats:
                avg_stats[key] = avg_stats[key] / team_size
            
            fig = go.Figure(data=[go.Bar(
                x=list(avg_stats.keys()),
                y=list(avg_stats.values()),
                marker_color='lightblue'
            )])
            fig.update_layout(
                title="Average Base Stats",
                yaxis_title="Value",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Clear team button
        if st.button("🗑️ Clear Team"):
            st.session_state.team = []
            st.rerun()
    else:
        st.info("Your team is empty. Go to 'Single Pokémon Explorer' and click 'Add to Team' to build your team!")

# ========================================
# PAGE 4: Type Explorer
# ========================================
elif page == "🎲 Type Explorer":
    st.header("Explore Pokémon by Type")
    
    all_types = list(TYPE_COLORS.keys())
    
    col1, col2 = st.columns(2)
    with col1:
        selected_type = st.selectbox("Select Primary Type", [""] + [t.title() for t in all_types])
    with col2:
        selected_type2 = st.selectbox("Select Secondary Type (Optional)", ["None"] + [t.title() for t in all_types])
    
    if selected_type:
        st.subheader(f"Pokémon with {selected_type} type")
        
        # Search for random Pokemon of this type
        type_pokemon = search_pokemon_by_type(selected_type.lower())
        
        if type_pokemon:
            # Display random samples
            sample_size = min(6, len(type_pokemon))
            samples = random.sample(type_pokemon, sample_size)
            
            cols = st.columns(3)
            for i, poke_name in enumerate(samples):
                with cols[i % 3]:
                    try:
                        data = get_pokemon_data(poke_name)
                        if data:
                            sprite_url = data['sprites']['other']['official-artwork']['front_default']
                            if sprite_url:
                                response = requests.get(sprite_url)
                                img = Image.open(BytesIO(response.content))
                                st.image(img, use_column_width=True)
                            
                            st.markdown(f"**{data['name'].title()}**")
                            types = [t['type']['name'] for t in data['types']]
                            type_html = ''.join([display_type_badge(t) for t in types])
                            st.markdown(type_html, unsafe_allow_html=True)
                    except:
                        pass
            
            if st.button("🔄 Show Different Pokémon"):
                st.rerun()

# ========================================
# PAGE 5: Advanced Statistics
# ========================================
elif page == "📊 Advanced Statistics":
    st.header("Advanced Pokémon Statistics")
    
    st.subheader("Generation Analysis")
    
    # Sample data from different generations
    gen_data = {
        'Gen I (1-151)': list(range(1, 152)),
        'Gen II (152-251)': list(range(152, 252)),
        'Gen III (252-386)': list(range(252, 387)),
        'Gen IV (387-493)': list(range(387, 494)),
        'Gen V (494-649)': list(range(494, 650))
    }
    
    selected_gen = st.selectbox("Select Generation", list(gen_data.keys()))
    
    if st.button("Analyze Generation"):
        with st.spinner("Analyzing generation data..."):
            gen_stats = {'HP': [], 'Attack': [], 'Defense': [], 'Speed': []}
            
            # Sample 20 random Pokémon from generation
            sample_ids = random.sample(gen_data[selected_gen], min(20, len(gen_data[selected_gen])))
            
            for poke_id in sample_ids:
                try:
                    data = get_pokemon_data(poke_id)
                    if data:
                        for stat in data['stats']:
                            stat_name = stat['stat']['name'].title()
                            if stat_name in gen_stats:
                                gen_stats[stat_name].append(stat['base_stat'])
                except:
                    pass
            
            # Calculate averages
            avg_stats = {k: sum(v)/len(v) if v else 0 for k, v in gen_stats.items()}
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = go.Figure(data=[go.Bar(
                    x=list(avg_stats.keys()),
                    y=list(avg_stats.values()),
                    marker_color='coral'
                )])
                fig.update_layout(
                    title=f"{selected_gen} Average Stats",
                    yaxis_title="Average Value"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                for stat_name, values in gen_stats.items():
                    if values:
                        st.metric(
                            f"{stat_name}",
                            f"{sum(values)/len(values):.1f}",
                            f"Range: {min(values)}-{max(values)}"
                        )

# Footer
st.divider()
st.markdown("""
    <div style='text-align: center; color: gray; padding: 20px;'>
        <p>Pokémon Explorer Pro | Data from PokéAPI | Made with ❤️ using Streamlit</p>
    </div>
""", unsafe_allow_html=True)