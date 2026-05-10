ide for users
markdown

# 🚀 Quick Start Guide

## Installation & Running

### Method 1: Simple Setup (Recommended)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### Method 2: Using Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## 🎯 Quick Feature Guide

### 1. Search for a Pokémon (30 seconds)

1. Open the app
2. Type "Charizard" in the search box
3. View complete stats, abilities, and evolution chain!

### 2. Build Your First Team (2 minutes)

1. Search for "Pikachu"
2. Click "➕ Add to Team"
3. Repeat for 5 more Pokémon
4. Go to "👥 Team Builder" tab
5. See your team's type coverage and stats!

### 3. Compare Pokémon (1 minute)

1. Search for "Blastoise"
2. Click "📊 Add to Comparison"
3. Search for "Charizard"
4. Click "📊 Add to Comparison"
5. Go to "⚔️ Compare Pokémon" tab
6. See the radar chart comparison!

### 4. Explore by Type (30 seconds)

1. Go to "🎲 Type Explorer"
2. Select "Fire" from dropdown
3. Click "🔄 Show Different Pokémon" to see random Fire types!

## 💡 Pro Tips

### Finding Specific Pokémon

- **By Name**: Just type the name (e.g., "Mewtwo")
- **By ID**: Use numbers (e.g., "150" for Mewtwo)
- **Random**: Click "🎲 Random" for surprises
- **Categories**: Use dropdowns for Starters, Legendaries, etc.

### Maximizing Team Builder

- Look for diverse type coverage
- Check average stats to balance your team
- Use the pie chart to spot type weaknesses
- Aim for complementary abilities

### Best Practices

- Clear comparison list when done (max 4 Pokémon)
- Team limit is 6 Pokémon (like the games!)
- Use radar charts for quick visual comparison
- Check evolution chains before choosing

## 🎮 Example Workflows

### Building a Balanced Team

1. Start with a strong starter (Charizard, Blastoise, Venusaur)
2. Add type coverage (Water + Fire + Grass is a good start)
3. Include a fast Pokémon (high Speed stat)
4. Add a tank (high Defense/Sp. Def)
5. Include a special attacker (high Sp. Atk)
6. Finish with a physical attacker (high Attack)

### Finding the Perfect Pokémon

1. Use Type Explorer to see options
2. Add interesting ones to comparison
3. Compare their stats side-by-side
4. Choose based on your team needs
5. Add to your team!

### Analyzing Legendary Pokémon

1. Select "Legendary" from category dropdown
2. Get random legendary Pokémon
3. Check base stats (usually 600+ total!)
4. View evolution chain (most don't evolve)
5. Compare with your team

## 🔥 Advanced Features

### Stat Analysis

- **Highest/Lowest Stats**: Automatically highlighted
- **Total Base Stats**: Quick power indicator
- **Radar Charts**: Visual stat distribution
- **Bar Charts**: Precise individual values

### Evolution Chains

- See all forms in one view
- Visual sprite display for each stage
- Click any evolution to view details

### Move Sets

- **Level-up Moves**: What they learn naturally
- **TM/HM Moves**: Teachable moves
- **Egg Moves**: Breeding-exclusive moves

### Breeding Info

- Egg groups for compatibility
- Gender ratios for probability
- Hatch rates in steps
- Growth rates for leveling

## 🐛 Common Questions

**Q: Why isn't my Pokémon loading?**
A: Check spelling or try the Pokémon's ID number instead.

**Q: Can I save my team?**
A: Teams persist during your session but reset when you close the app.

**Q: How many Pokémon are available?**
A: All 1010 Pokémon from Generations 1-8 are available!

**Q: Why do some images load slowly?**
A: First load fetches from the API. Subsequent loads are cached and faster!

**Q: Can I compare more than 4 Pokémon?**
A: Currently limited to 4 for optimal visualization.

## 📊 Understanding the Stats

### Base Stats Explained

- **HP**: Hit Points - determines total health
- **Attack**: Physical move damage
- **Defense**: Physical damage reduction
- **Sp. Atk**: Special move damage
- **Sp. Def**: Special damage reduction
- **Speed**: Turn order in battle

### Good Stat Totals

- **< 300**: Weak (early game Pokémon)
- **300-450**: Average (mid-game Pokémon)
- **450-550**: Strong (late game Pokémon)
- **550-600**: Very Strong (pseudo-legendaries)
- **600+**: Legendary tier

### Type Effectiveness Quick Reference

Remember: Some types are strong/weak against others

- Use Type Explorer to find coverage
- Build teams with diverse types
- Check evolution chains for type changes

## 🎨 Interface Tips

### Navigation

- Use sidebar for main sections
- Tabs within sections for detailed info
- Buttons for quick actions
- Search is case-insensitive

### Visual Indicators

- **Green badges**: Type indicators
- **Orange/Red charts**: Stat visualizations
- **Metric cards**: Quick stat views
- **Progress bars**: EV distributions (in calculator)

## 🚀 Next Steps

Ready to become a Pokémon Master? Try:

1. **Build a themed team** (all Fire types, all Starters, etc.)
2. **Find the strongest Pokémon** (sort by total stats)
3. **Discover new favorites** (random exploration)
4. **Compare legendary trios** (the legendary birds, beasts, etc.)
5. **Plan evolution strategies** (check evolution chains)

## 🔧 Bonus: Using the Calculator

If you run `calculator.py` separately:

```bash
streamlit run calculator.py
```

You get:

- **IV/EV Calculator**: Optimize competitive stats
- **Damage Calculator**: Plan battle strategies
- **Nature Effects**: Understand stat modifiers

---

**Happy exploring!** 🎮⚡
