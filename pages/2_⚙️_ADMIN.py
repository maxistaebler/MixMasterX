import streamlit as st
import os
from PIL import Image
import io

# Get the absolute path to the assets directory
ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")

# Ensure assets directory exists
if not os.path.exists(ASSETS_DIR):
    os.makedirs(ASSETS_DIR)

# Function to resize image
def resize_image(image_bytes, target_size=(700, 933)):
    try:
        # Open the image
        img = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if necessary
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        
        # Resize the image
        img = img.resize(target_size, Image.Resampling.LANCZOS)
        
        # Save to bytes
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG', quality=95)
        img_byte_arr = img_byte_arr.getvalue()
        
        return img_byte_arr, None
    except Exception as e:
        return None, str(e)

# Standard Zutaten und deren Standardslots
DEFAULT_INGREDIENTS = {
    "Aperol": 1,
    "Lillet": 2,
    "Schweppes Raspberry": 3,
    "Secco": 4,
    "Mineralwasser": 5,
    "Gin": 6,
    "Tonic": 7
}

# Standard Cocktail-Rezepte
DEFAULT_RECIPES = {
    "Aperol Spritz": {
        "image": os.path.join(ASSETS_DIR, "aperol_spritz.jpg"),
        "ingredients": {
            "Aperol": 60,  # ml
            "Secco": 90,   # ml
            "Mineralwasser": 30  # ml
        }
    },
    "Wildberry Lillet": {
        "image": os.path.join(ASSETS_DIR, "wildberry_lillet.jpg"),
        "ingredients": {
            "Lillet": 80,  # ml
            "Schweppes Raspberry": 120  # ml
        }
    },
    "Gin Tonic": {
        "image": os.path.join(ASSETS_DIR, "gin_tonic.jpg"),
        "ingredients": {
            "Gin": 40,  # ml
            "Tonic": 160  # ml
        }
    }
}

# Session State initialisieren
if "ingredients" not in st.session_state:
    st.session_state["ingredients"] = DEFAULT_INGREDIENTS
if "recipes" not in st.session_state:
    st.session_state["recipes"] = DEFAULT_RECIPES
if "cocktails" not in st.session_state:
    st.session_state["cocktails"] = {name: recipe["image"] for name, recipe in DEFAULT_RECIPES.items()}

st.title("Adminbereich ⚙️")

# Sektion 1: Zutaten und Slots verwalten
st.header("1. Zutaten und Slots verwalten")
st.write("Hier können Sie die verfügbaren Zutaten und deren Slot-Positionen definieren.")

# Funktion zum Überprüfen der verfügbaren Slots
def get_available_slots(current_ingredient=None):
    used_slots = set()
    for ing, slot in st.session_state["ingredients"].items():
        if ing != current_ingredient and slot != "-":  # Ignoriere den aktuellen Slot
            used_slots.add(slot)
    available_slots = ["-"] + [str(i) for i in range(1, 11) if i not in used_slots]
    return available_slots

col1, col2 = st.columns(2)

with col1:
    st.subheader("Verfügbare Zutaten")
    updated_ingredients = {}
    for ingredient, current_slot in st.session_state["ingredients"].items():
        available_slots = get_available_slots(ingredient)
        current_slot_str = str(current_slot) if current_slot != "-" else "-"
        new_slot = st.selectbox(
            f"Slot für {ingredient}:",
            options=available_slots,
            index=available_slots.index(current_slot_str),
            key=f"slot_{ingredient}"
        )
        
        if new_slot != "-":
            updated_ingredients[ingredient] = int(new_slot)
        else:
            st.error(f"Bitte wählen Sie einen gültigen Slot für {ingredient}")
    
    # Update ingredients only if all slots are valid
    if all(ingredient in updated_ingredients for ingredient in st.session_state["ingredients"]):
        st.session_state["ingredients"] = updated_ingredients

with col2:
    st.subheader("Neue Zutat hinzufügen")
    new_ingredient = st.text_input("Name der neuen Zutat:")
    available_slots = get_available_slots()
    new_slot = st.selectbox("Slot:", options=available_slots, key="new_slot")
    
    if st.button("Zutat hinzufügen"):
        if new_ingredient and new_slot != "-":
            if new_ingredient not in st.session_state["ingredients"]:
                st.session_state["ingredients"][new_ingredient] = int(new_slot)
                st.success(f"{new_ingredient} wurde hinzugefügt!")
                st.rerun()
            else:
                st.error("Diese Zutat existiert bereits!")
        else:
            st.error("Bitte geben Sie einen Namen ein und wählen Sie einen gültigen Slot")

# Sektion 2: Cocktail-Rezepte verwalten
st.header("2. Cocktail-Rezepte verwalten")

# Existierende Rezepte bearbeiten
st.subheader("Existierende Rezepte")
for cocktail_name in st.session_state["recipes"].keys():
    with st.expander(f"Rezept: {cocktail_name}"):
        st.write("Zutaten und Mengen (in ml):")
        recipe = st.session_state["recipes"][cocktail_name]["ingredients"]
        
        updated_ingredients = {}
        for ing, amount in recipe.items():
            new_amount = st.number_input(
                f"{ing}:",
                min_value=0,
                max_value=500,
                value=amount,
                key=f"{cocktail_name}_{ing}"
            )
            updated_ingredients[ing] = new_amount
        
        st.session_state["recipes"][cocktail_name]["ingredients"] = updated_ingredients

# Neuen Cocktail hinzufügen
st.subheader("Neuen Cocktail hinzufügen")
new_cocktail = st.text_input("Name des neuen Cocktails:")
uploaded_file = st.file_uploader("Cocktail-Bild hochladen (optimal: 700x933 Pixel)", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    # Read the file
    image_bytes = uploaded_file.getvalue()
    
    # Resize the image
    resized_image, error = resize_image(image_bytes)
    
    if error:
        st.error(f"Fehler beim Verarbeiten des Bildes: {error}")
        st.error("Bitte laden Sie ein anderes Bild hoch.")
    else:
        # Save the resized image
        file_extension = os.path.splitext(uploaded_file.name)[1]
        file_name = f"{new_cocktail.lower().replace(' ', '_')}{file_extension}"
        image_path = os.path.join(ASSETS_DIR, file_name)
        
        with open(image_path, "wb") as f:
            f.write(resized_image)
        
        # Show preview of the resized image
        st.image(resized_image, caption="Vorschau des verarbeiteten Bildes", width=350)
        
        # Store the path for later use
        if "temp_image_path" not in st.session_state:
            st.session_state["temp_image_path"] = image_path

# Zutaten für neuen Cocktail auswählen
if new_cocktail:
    st.write("Zutaten auswählen:")
    new_ingredients = {}
    for ingredient in st.session_state["ingredients"].keys():
        amount = st.number_input(
            f"Menge {ingredient} (ml):",
            min_value=0,
            max_value=500,
            value=0,
            key=f"new_{ingredient}"
        )
        if amount > 0:
            new_ingredients[ingredient] = amount

    if st.button("Cocktail hinzufügen"):
        if "temp_image_path" in st.session_state and new_ingredients:
            image_path = st.session_state["temp_image_path"]
            st.session_state["recipes"][new_cocktail] = {
                "image": image_path,
                "ingredients": new_ingredients
            }
            st.session_state["cocktails"][new_cocktail] = image_path
            
            # Clear the temporary image path
            del st.session_state["temp_image_path"]
            
            st.success(f"{new_cocktail} wurde erfolgreich hinzugefügt!")
            st.rerun()
        else:
            st.error("Bitte laden Sie ein Bild hoch und fügen Sie mindestens eine Zutat hinzu!")

# Debug-Informationen (optional)
if st.checkbox("Debug-Informationen anzeigen"):
    st.write("Aktuelle Zutaten und Slots:", st.session_state["ingredients"])
    st.write("Aktuelle Rezepte:", st.session_state["recipes"])
