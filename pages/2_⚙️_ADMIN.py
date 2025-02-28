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

# Standard Cocktail-Rezepte mit Prozentangaben
DEFAULT_RECIPES = {
    "Aperol Spritz": {
        "image": os.path.join(ASSETS_DIR, "aperol_spritz.jpg"),
        "glass_size": 400,  # ml
        "ingredients": {
            "Aperol": 33,  # %
            "Secco": 50,   # %
            "Mineralwasser": 17  # %
        }
    },
    "Wildberry Lillet": {
        "image": os.path.join(ASSETS_DIR, "wildberry_lillet.jpg"),
        "glass_size": 400,  # ml
        "ingredients": {
            "Lillet": 40,  # %
            "Schweppes Raspberry": 60  # %
        }
    },
    "Gin Tonic": {
        "image": os.path.join(ASSETS_DIR, "gin_tonic.jpg"),
        "glass_size": 400,  # ml
        "ingredients": {
            "Gin": 20,  # %
            "Tonic": 80  # %
        }
    }
}

# Set of default cocktail names for deletion protection
DEFAULT_COCKTAIL_NAMES = set(DEFAULT_RECIPES.keys())

# Session State initialisieren
if "ingredients" not in st.session_state:
    st.session_state["ingredients"] = DEFAULT_INGREDIENTS
if "recipes" not in st.session_state:
    st.session_state["recipes"] = DEFAULT_RECIPES
if "cocktails" not in st.session_state:
    st.session_state["cocktails"] = {name: recipe["image"] for name, recipe in DEFAULT_RECIPES.items()}

# Add glass size to session state if not present
if "glass_size" not in st.session_state:
    st.session_state["glass_size"] = 400  # Default glass size in ml

st.title("Adminbereich ⚙️")

# Global glass size setting
st.header("Glasgröße einstellen")
st.session_state["glass_size"] = st.slider(
    "Standard Glasgröße (ml):",
    min_value=100,
    max_value=1000,
    value=st.session_state["glass_size"],
    step=50,
)
st.write(f"Aktuelle Glasgröße: {st.session_state['glass_size']}ml")

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

# Funktion zur Überprüfung der Prozentsumme
def validate_percentages(ingredients):
    total = sum(ingredients.values())
    return abs(total - 100) < 0.1  # Erlaubt kleine Rundungsfehler

# Sektion 2: Cocktail-Rezepte verwalten
st.header("2. Cocktail-Rezepte verwalten")

# Existierende Rezepte bearbeiten
st.subheader("Existierende Rezepte")
cocktails_to_delete = []  # Liste für zu löschende Cocktails

for cocktail_name in st.session_state["recipes"].keys():
    with st.expander(f"Rezept: {cocktail_name}"):
        # Delete button in the top right corner
        col1, col2 = st.columns([6, 1])
        with col2:
            if cocktail_name in DEFAULT_COCKTAIL_NAMES:
                st.write("🔒")  # Lock emoji for default cocktails
            else:
                if st.button("🗑️", key=f"delete_{cocktail_name}"):
                    cocktails_to_delete.append(cocktail_name)
                    st.warning(f"Cocktail {cocktail_name} wird gelöscht...")
        
        with col1:
            st.write("Zutaten (in %):")
            recipe = st.session_state["recipes"][cocktail_name]
            
            updated_ingredients = {}
            for ing, percentage in recipe["ingredients"].items():
                new_percentage = st.number_input(
                    f"{ing} (%):",
                    min_value=0.0,
                    max_value=100.0,
                    value=float(percentage),
                    step=0.1,
                    key=f"{cocktail_name}_{ing}"
                )
                updated_ingredients[ing] = new_percentage
            
            # Überprüfe ob die Summe 100% ergibt
            if not validate_percentages(updated_ingredients):
                st.error("Die Summe der Prozente muss 100% ergeben!")
                st.write(f"Aktuelle Summe: {sum(updated_ingredients.values()):.1f}%")
            else:
                recipe["ingredients"] = updated_ingredients
                
            # Zeige die ml-Werte an
            st.write("\nMengen in ml (basierend auf Glasgröße):")
            for ing, percentage in updated_ingredients.items():
                ml_amount = (percentage / 100) * st.session_state["glass_size"]
                st.write(f"{ing}: {ml_amount:.1f}ml")

# Lösche die markierten Cocktails
for cocktail_name in cocktails_to_delete:
    if cocktail_name not in DEFAULT_COCKTAIL_NAMES:  # Extra safety check
        # Remove the cocktail's image file if it exists
        image_path = st.session_state["recipes"][cocktail_name]["image"]
        try:
            if os.path.exists(image_path):
                os.remove(image_path)
        except Exception as e:
            st.error(f"Fehler beim Löschen des Bildes für {cocktail_name}: {e}")
        
        # Remove the cocktail from both recipes and cocktails
        del st.session_state["recipes"][cocktail_name]
        del st.session_state["cocktails"][cocktail_name]
        
        # Rerun the app to update the display
        if cocktails_to_delete:
            st.rerun()

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
    st.write("Zutaten (in %):")
    
    new_ingredients = {}
    for ingredient in st.session_state["ingredients"].keys():
        percentage = st.number_input(
            f"{ingredient} (%):",
            min_value=0.0,
            max_value=100.0,
            value=0.0,
            step=0.1,
            key=f"new_{ingredient}"
        )
        if percentage > 0:
            new_ingredients[ingredient] = percentage
    
    # Überprüfe die Prozentsumme
    if new_ingredients:
        total_percentage = sum(new_ingredients.values())
        st.write(f"Gesamtsumme: {total_percentage:.1f}%")
        
        if not validate_percentages(new_ingredients):
            st.error("Die Summe der Prozente muss 100% ergeben!")
        else:
            st.success("Die Prozente ergeben 100%!")
            
            # Zeige die ml-Werte an
            st.write("\nMengen in ml (basierend auf Glasgröße):")
            for ing, percentage in new_ingredients.items():
                ml_amount = (percentage / 100) * st.session_state["glass_size"]
                st.write(f"{ing}: {ml_amount:.1f}ml")

    if st.button("Cocktail hinzufügen"):
        if "temp_image_path" in st.session_state and new_ingredients:
            if validate_percentages(new_ingredients):
                image_path = st.session_state["temp_image_path"]
                st.session_state["recipes"][new_cocktail] = {
                    "image": image_path,
                    "ingredients": new_ingredients
                }
                st.session_state["cocktails"][new_cocktail] = image_path
                
                del st.session_state["temp_image_path"]
                
                st.success(f"{new_cocktail} wurde erfolgreich hinzugefügt!")
                st.rerun()
            else:
                st.error("Die Summe der Prozente muss 100% ergeben!")
        else:
            st.error("Bitte laden Sie ein Bild hoch und fügen Sie mindestens eine Zutat hinzu!")

# Debug-Informationen (optional)
if st.checkbox("Debug-Informationen anzeigen"):
    st.write("Aktuelle Zutaten und Slots:", st.session_state["ingredients"])
    st.write("Aktuelle Rezepte:", st.session_state["recipes"])
    st.write("Aktuelle Glasgröße:", st.session_state["glass_size"])
