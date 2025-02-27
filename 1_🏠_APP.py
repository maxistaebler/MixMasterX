import streamlit as st
import math
import os

# Konfiguration der Hauptseite
st.set_page_config(
    page_title="Cocktail Mixer",
    page_icon="🍹",
    layout="wide"
)

st.sidebar.success("Wähle eine Seite aus dem Menü.")

# Get the absolute path to the assets directory
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")

# Standard Cocktails mit Bildpfaden
DEFAULT_COCKTAILS = {
    "Aperol Spritz": os.path.join(ASSETS_DIR, "aperol_spritz.jpg"),
    "Wildberry Lillet": os.path.join(ASSETS_DIR, "wildberry_lillet.jpg"),
    "Gin Tonic": os.path.join(ASSETS_DIR, "gin_tonic.jpg")
}

# Session State initialisieren, falls nicht vorhanden
if "cocktails" not in st.session_state:
    st.session_state["cocktails"] = DEFAULT_COCKTAILS

# Add custom CSS for clickable cards
st.markdown("""
    <style>
    .cocktail-card {
        cursor: pointer;
        transition: transform 0.3s;
        padding: 10px;
        border-radius: 10px;
        background: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .cocktail-card:hover {
        transform: scale(1.02);
    }
    .centered-title {
        text-align: center;
        padding: 2rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Zentrierter Titel
st.markdown("<h1 class='centered-title'>Cocktail / Long-Drink-Auswahl 🍸</h1>", unsafe_allow_html=True)

# Verwende die Rezepte aus dem Admin-Bereich
if "recipes" not in st.session_state:
    st.error("Bitte zuerst im Admin-Bereich Cocktails konfigurieren!")
else:
    # Bestimme die Anzahl der Cocktails pro Reihe
    total_cocktails = len(st.session_state["recipes"])
    cocktails_per_row = 3 if total_cocktails % 3 == 0 else 2

    # Berechne die Anzahl der benötigten Reihen
    num_rows = math.ceil(total_cocktails / cocktails_per_row)

    # Erstelle das Grid-Layout
    for row in range(num_rows):
        start_idx = row * cocktails_per_row
        end_idx = min(start_idx + cocktails_per_row, total_cocktails)
        
        cols = st.columns(cocktails_per_row)
        cocktails = list(st.session_state["recipes"].items())
        
        for col_idx, cocktail_idx in enumerate(range(start_idx, end_idx)):
            with cols[col_idx]:
                cocktail_name, recipe_data = cocktails[cocktail_idx]
                try:
                    st.image(recipe_data["image"], use_container_width=True)
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        if st.button(cocktail_name, key=f"btn_{cocktail_idx}"):
                            st.json(recipe_data["ingredients"])
                            st.success(f"Du hast {cocktail_name} ausgewählt! Prost! 🍹")
                except Exception as e:
                    st.error(f"Bild für {cocktail_name} konnte nicht geladen werden")

