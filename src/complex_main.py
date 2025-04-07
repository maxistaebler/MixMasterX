import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import json
import math
from PIL import Image, ImageTk
import io

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Cocktail Mixer")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Set up assets directory
        self.assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
        if not os.path.exists(self.assets_dir):
            os.makedirs(self.assets_dir)
        
        # Default data
        self.default_ingredients = {
            "Aperol": 1,
            "Lillet": 2,
            "Schweppes Raspberry": 3,
            "Secco": 4,
            "Mineralwasser": 5,
            "Gin": 6,
            "Tonic": 7
        }
        
        self.default_recipes = {
            "Aperol Spritz": {
                "image": os.path.join(self.assets_dir, "aperol_spritz.jpg"),
                "glass_size": 400,
                "ingredients": {
                    "Aperol": 33,
                    "Secco": 50,
                    "Mineralwasser": 17
                }
            },
            "Wildberry Lillet": {
                "image": os.path.join(self.assets_dir, "wildberry_lillet.jpg"),
                "glass_size": 400,
                "ingredients": {
                    "Lillet": 40,
                    "Schweppes Raspberry": 60
                }
            },
            "Gin Tonic": {
                "image": os.path.join(self.assets_dir, "gin_tonic.jpg"),
                "glass_size": 400,
                "ingredients": {
                    "Gin": 20,
                    "Tonic": 80
                }
            }
        }
        
        # Default cocktail names for deletion protection
        self.default_cocktail_names = set(self.default_recipes.keys())
        
        # Load data from file or use defaults
        self.load_data()
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create main tab
        self.main_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.main_frame, text="Cocktail Auswahl")
        
        # Create admin tab
        self.admin_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.admin_frame, text="Admin")
        
        # Initialize tabs
        self.setup_main_tab()
        self.setup_admin_tab()
        
        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def load_data(self):
        """Load data from JSON files or use defaults"""
        data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        # Load ingredients
        ingredients_file = os.path.join(data_dir, "ingredients.json")
        if os.path.exists(ingredients_file):
            try:
                with open(ingredients_file, 'r') as f:
                    self.ingredients = json.load(f)
            except:
                self.ingredients = self.default_ingredients.copy()
        else:
            self.ingredients = self.default_ingredients.copy()
        
        # Load recipes
        recipes_file = os.path.join(data_dir, "recipes.json")
        if os.path.exists(recipes_file):
            try:
                with open(recipes_file, 'r') as f:
                    self.recipes = json.load(f)
            except:
                self.recipes = self.default_recipes.copy()
        else:
            self.recipes = self.default_recipes.copy()
        
        # Load glass size
        glass_size_file = os.path.join(data_dir, "glass_size.json")
        if os.path.exists(glass_size_file):
            try:
                with open(glass_size_file, 'r') as f:
                    self.glass_size = json.load(f)["glass_size"]
            except:
                self.glass_size = 400
        else:
            self.glass_size = 400
    
    def save_data(self):
        """Save data to JSON files"""
        data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        # Save ingredients
        with open(os.path.join(data_dir, "ingredients.json"), 'w') as f:
            json.dump(self.ingredients, f, indent=4)
        
        # Save recipes
        with open(os.path.join(data_dir, "recipes.json"), 'w') as f:
            json.dump(self.recipes, f, indent=4)
        
        # Save glass size
        with open(os.path.join(data_dir, "glass_size.json"), 'w') as f:
            json.dump({"glass_size": self.glass_size}, f, indent=4)
    
    def setup_main_tab(self):
        """Set up the main tab for cocktail selection"""
        # Title
        title_frame = ttk.Frame(self.main_frame)
        title_frame.pack(fill=tk.X, padx=10, pady=10)
        
        title_label = ttk.Label(title_frame, text="Cocktail / Long-Drink-Auswahl 🍸", font=("Arial", 24, "bold"))
        title_label.pack()
        
        # Glass size display
        glass_frame = ttk.Frame(self.main_frame)
        glass_frame.pack(fill=tk.X, padx=10, pady=5)
        
        glass_label = ttk.Label(glass_frame, text=f"Glasgröße: {self.glass_size}ml", font=("Arial", 12))
        glass_label.pack(side=tk.LEFT)
        
        # Cocktail grid
        self.cocktail_frame = ttk.Frame(self.main_frame)
        self.cocktail_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Recipe details frame
        self.recipe_details_frame = ttk.Frame(self.main_frame)
        self.recipe_details_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Update cocktail grid
        self.update_cocktail_grid()
    
    def update_cocktail_grid(self):
        """Update the cocktail grid in the main tab"""
        # Clear existing widgets
        for widget in self.cocktail_frame.winfo_children():
            widget.destroy()
        
        # Clear recipe details
        for widget in self.recipe_details_frame.winfo_children():
            widget.destroy()
        
        # Calculate grid dimensions
        total_cocktails = len(self.recipes)
        cocktails_per_row = 3 if total_cocktails % 3 == 0 else 2
        num_rows = math.ceil(total_cocktails / cocktails_per_row)
        
        # Create grid
        for row in range(num_rows):
            for col in range(cocktails_per_row):
                cocktail_idx = row * cocktails_per_row + col
                if cocktail_idx < total_cocktails:
                    cocktail_name = list(self.recipes.keys())[cocktail_idx]
                    recipe_data = self.recipes[cocktail_name]
                    
                    # Create frame for cocktail
                    cocktail_frame = ttk.Frame(self.cocktail_frame, relief=tk.RAISED, borderwidth=1)
                    cocktail_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
                    
                    # Load and display image
                    try:
                        img = Image.open(recipe_data["image"])
                        img = img.resize((200, 266), Image.Resampling.LANCZOS)
                        photo = ImageTk.PhotoImage(img)
                        
                        img_label = ttk.Label(cocktail_frame, image=photo)
                        img_label.image = photo  # Keep a reference
                        img_label.pack(padx=5, pady=5)
                    except Exception as e:
                        error_label = ttk.Label(cocktail_frame, text=f"Bild konnte nicht geladen werden: {e}")
                        error_label.pack(padx=5, pady=5)
                    
                    # Cocktail name button
                    btn = ttk.Button(cocktail_frame, text=cocktail_name, 
                                    command=lambda name=cocktail_name: self.show_recipe_details(name))
                    btn.pack(padx=5, pady=5, fill=tk.X)
        
        # Configure grid weights
        for i in range(num_rows):
            self.cocktail_frame.grid_rowconfigure(i, weight=1)
        for i in range(cocktails_per_row):
            self.cocktail_frame.grid_columnconfigure(i, weight=1)
    
    def show_recipe_details(self, cocktail_name):
        """Show recipe details for the selected cocktail"""
        # Clear existing widgets
        for widget in self.recipe_details_frame.winfo_children():
            widget.destroy()
        
        recipe_data = self.recipes[cocktail_name]
        
        # Title
        title_label = ttk.Label(self.recipe_details_frame, text=f"Rezept: {cocktail_name}", font=("Arial", 16, "bold"))
        title_label.pack(pady=5)
        
        # Glass size
        glass_label = ttk.Label(self.recipe_details_frame, text=f"Glasgröße: {self.glass_size}ml")
        glass_label.pack(pady=5)
        
        # Ingredients
        ingredients_frame = ttk.Frame(self.recipe_details_frame)
        ingredients_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(ingredients_frame, text="Zutat", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Label(ingredients_frame, text="Prozent", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        ttk.Label(ingredients_frame, text="Menge (ml)", font=("Arial", 12, "bold")).grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        
        for i, (ing, percentage) in enumerate(recipe_data["ingredients"].items()):
            ml_amount = (percentage / 100) * self.glass_size
            
            ttk.Label(ingredients_frame, text=ing).grid(row=i+1, column=0, padx=5, pady=2, sticky=tk.W)
            ttk.Label(ingredients_frame, text=f"{percentage:.1f}%").grid(row=i+1, column=1, padx=5, pady=2, sticky=tk.W)
            ttk.Label(ingredients_frame, text=f"{ml_amount:.1f}ml").grid(row=i+1, column=2, padx=5, pady=2, sticky=tk.W)
        
        # Success message
        success_label = ttk.Label(self.recipe_details_frame, text=f"Du hast {cocktail_name} ausgewählt! Prost! 🍹", font=("Arial", 12))
        success_label.pack(pady=10)
    
    def setup_admin_tab(self):
        """Set up the admin tab for managing ingredients and recipes"""
        # Create notebook for admin sections
        admin_notebook = ttk.Notebook(self.admin_frame)
        admin_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Glass size tab
        glass_frame = ttk.Frame(admin_notebook)
        admin_notebook.add(glass_frame, text="Glasgröße")
        
        # Ingredients tab
        ingredients_frame = ttk.Frame(admin_notebook)
        admin_notebook.add(ingredients_frame, text="Zutaten")
        
        # Recipes tab
        recipes_frame = ttk.Frame(admin_notebook)
        admin_notebook.add(recipes_frame, text="Rezepte")
        
        # Setup each tab
        self.setup_glass_size_tab(glass_frame)
        self.setup_ingredients_tab(ingredients_frame)
        self.setup_recipes_tab(recipes_frame)
    
    def setup_glass_size_tab(self, parent):
        """Set up the glass size tab"""
        # Title
        title_label = ttk.Label(parent, text="Glasgröße einstellen", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Glass size slider
        glass_frame = ttk.Frame(parent)
        glass_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(glass_frame, text="Standard Glasgröße (ml):").pack(side=tk.LEFT, padx=5)
        
        glass_var = tk.IntVar(value=self.glass_size)
        glass_slider = ttk.Scale(glass_frame, from_=100, to=1000, variable=glass_var, 
                                orient=tk.HORIZONTAL, length=300, command=self.update_glass_size)
        glass_slider.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        glass_label = ttk.Label(glass_frame, text=f"{self.glass_size}ml")
        glass_label.pack(side=tk.LEFT, padx=5)
        
        # Store references
        self.glass_var = glass_var
        self.glass_label = glass_label
    
    def update_glass_size(self, *args):
        """Update glass size when slider changes"""
        self.glass_size = self.glass_var.get()
        self.glass_label.config(text=f"{self.glass_size}ml")
        self.save_data()
    
    def setup_ingredients_tab(self, parent):
        """Set up the ingredients tab"""
        # Title
        title_label = ttk.Label(parent, text="Zutaten und Slots verwalten", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Description
        desc_label = ttk.Label(parent, text="Hier können Sie die verfügbaren Zutaten und deren Slot-Positionen definieren.")
        desc_label.pack(pady=5)
        
        # Create frames for existing ingredients and new ingredient
        ingredients_frame = ttk.Frame(parent)
        ingredients_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left frame for existing ingredients
        left_frame = ttk.LabelFrame(ingredients_frame, text="Verfügbare Zutaten")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Right frame for new ingredient
        right_frame = ttk.LabelFrame(ingredients_frame, text="Neue Zutat hinzufügen")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Setup existing ingredients
        self.setup_existing_ingredients(left_frame)
        
        # Setup new ingredient form
        self.setup_new_ingredient_form(right_frame)
    
    def setup_existing_ingredients(self, parent):
        """Set up the existing ingredients section"""
        # Create a canvas with scrollbar for ingredients
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Function to get available slots
        def get_available_slots(current_ingredient=None):
            used_slots = set()
            for ing, slot in self.ingredients.items():
                if ing != current_ingredient and slot != "-":
                    used_slots.add(slot)
            available_slots = ["-"] + [str(i) for i in range(1, 11) if i not in used_slots]
            return available_slots
        
        # Create widgets for each ingredient
        self.ingredient_vars = {}
        for ingredient, current_slot in self.ingredients.items():
            frame = ttk.Frame(scrollable_frame)
            frame.pack(fill=tk.X, padx=5, pady=2)
            
            ttk.Label(frame, text=f"{ingredient}:").pack(side=tk.LEFT, padx=5)
            
            available_slots = get_available_slots(ingredient)
            current_slot_str = str(current_slot) if current_slot != "-" else "-"
            
            var = tk.StringVar(value=current_slot_str)
            self.ingredient_vars[ingredient] = var
            
            combo = ttk.Combobox(frame, textvariable=var, values=available_slots, state="readonly", width=5)
            combo.pack(side=tk.LEFT, padx=5)
            
            # Add update function
            combo.bind("<<ComboboxSelected>>", lambda e, ing=ingredient: self.update_ingredient_slot(ing))
        
        # Add save button
        save_btn = ttk.Button(scrollable_frame, text="Änderungen speichern", command=self.save_ingredients)
        save_btn.pack(pady=10)
    
    def update_ingredient_slot(self, ingredient):
        """Update ingredient slot when changed"""
        slot = self.ingredient_vars[ingredient].get()
        if slot != "-":
            self.ingredients[ingredient] = int(slot)
        else:
            self.ingredients[ingredient] = "-"
        self.save_data()
    
    def save_ingredients(self):
        """Save ingredient changes"""
        self.save_data()
        messagebox.showinfo("Erfolg", "Zutaten wurden gespeichert!")
    
    def setup_new_ingredient_form(self, parent):
        """Set up the new ingredient form"""
        # Name input
        name_frame = ttk.Frame(parent)
        name_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(name_frame, text="Name der neuen Zutat:").pack(side=tk.LEFT, padx=5)
        
        name_var = tk.StringVar()
        name_entry = ttk.Entry(name_frame, textvariable=name_var)
        name_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Slot selection
        slot_frame = ttk.Frame(parent)
        slot_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(slot_frame, text="Slot:").pack(side=tk.LEFT, padx=5)
        
        # Get available slots
        used_slots = set()
        for slot in self.ingredients.values():
            if slot != "-":
                used_slots.add(slot)
        available_slots = [str(i) for i in range(1, 11) if i not in used_slots]
        
        slot_var = tk.StringVar()
        slot_combo = ttk.Combobox(slot_frame, textvariable=slot_var, values=available_slots, state="readonly", width=5)
        slot_combo.pack(side=tk.LEFT, padx=5)
        
        # Add button
        add_btn = ttk.Button(parent, text="Zutat hinzufügen", 
                            command=lambda: self.add_new_ingredient(name_var.get(), slot_var.get()))
        add_btn.pack(pady=10)
    
    def add_new_ingredient(self, name, slot):
        """Add a new ingredient"""
        if not name:
            messagebox.showerror("Fehler", "Bitte geben Sie einen Namen ein!")
            return
        
        if not slot:
            messagebox.showerror("Fehler", "Bitte wählen Sie einen gültigen Slot!")
            return
        
        if name in self.ingredients:
            messagebox.showerror("Fehler", "Diese Zutat existiert bereits!")
            return
        
        self.ingredients[name] = int(slot)
        self.save_data()
        
        # Refresh the ingredients tab
        self.setup_ingredients_tab(self.admin_frame.winfo_children()[0].select(1))
        messagebox.showinfo("Erfolg", f"{name} wurde hinzugefügt!")
    
    def setup_recipes_tab(self, parent):
        """Set up the recipes tab"""
        # Title
        title_label = ttk.Label(parent, text="Cocktail-Rezepte verwalten", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Create notebook for existing recipes and new recipe
        recipes_notebook = ttk.Notebook(parent)
        recipes_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Existing recipes tab
        existing_frame = ttk.Frame(recipes_notebook)
        recipes_notebook.add(existing_frame, text="Existierende Rezepte")
        
        # New recipe tab
        new_frame = ttk.Frame(recipes_notebook)
        recipes_notebook.add(new_frame, text="Neuen Cocktail hinzufügen")
        
        # Setup each tab
        self.setup_existing_recipes_tab(existing_frame)
        self.setup_new_recipe_tab(new_frame)
    
    def setup_existing_recipes_tab(self, parent):
        """Set up the existing recipes tab"""
        # Create a canvas with scrollbar for recipes
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Function to validate percentages
        def validate_percentages(ingredients):
            total = sum(ingredients.values())
            return abs(total - 100) < 0.1  # Allow small rounding errors
        
        # Create widgets for each recipe
        self.recipe_vars = {}
        for cocktail_name, recipe_data in self.recipes.items():
            # Create frame for recipe
            recipe_frame = ttk.LabelFrame(scrollable_frame, text=f"Rezept: {cocktail_name}")
            recipe_frame.pack(fill=tk.X, padx=5, pady=5)
            
            # Delete button (if not default)
            if cocktail_name not in self.default_cocktail_names:
                delete_btn = ttk.Button(recipe_frame, text="🗑️", width=3,
                                       command=lambda name=cocktail_name: self.delete_recipe(name))
                delete_btn.pack(side=tk.RIGHT, padx=5, pady=5)
            
            # Ingredients section
            ingredients_frame = ttk.Frame(recipe_frame)
            ingredients_frame.pack(fill=tk.X, padx=5, pady=5)
            
            ttk.Label(ingredients_frame, text="Zutaten (in %):").pack(anchor=tk.W, padx=5, pady=5)
            
            # Create widgets for each ingredient
            recipe_vars = {}
            for ing, percentage in recipe_data["ingredients"].items():
                ing_frame = ttk.Frame(ingredients_frame)
                ing_frame.pack(fill=tk.X, padx=5, pady=2)
                
                ttk.Label(ing_frame, text=f"{ing}:").pack(side=tk.LEFT, padx=5)
                
                var = tk.DoubleVar(value=percentage)
                recipe_vars[ing] = var
                
                spinbox = ttk.Spinbox(ing_frame, from_=0.0, to=100.0, increment=0.1, textvariable=var, width=10)
                spinbox.pack(side=tk.LEFT, padx=5)
                
                # Add update function
                spinbox.bind("<KeyRelease>", lambda e, name=cocktail_name, ing=ing: 
                            self.update_recipe_ingredient(name, ing))
            
            # Store recipe variables
            self.recipe_vars[cocktail_name] = recipe_vars
            
            # Total percentage
            total_frame = ttk.Frame(recipe_frame)
            total_frame.pack(fill=tk.X, padx=5, pady=5)
            
            total_var = tk.StringVar(value=f"Gesamtsumme: {sum(recipe_data['ingredients'].values()):.1f}%")
            total_label = ttk.Label(total_frame, textvariable=total_var)
            total_label.pack(side=tk.LEFT, padx=5)
            
            # ML amounts
            ml_frame = ttk.Frame(recipe_frame)
            ml_frame.pack(fill=tk.X, padx=5, pady=5)
            
            ttk.Label(ml_frame, text="Mengen in ml (basierend auf Glasgröße):").pack(anchor=tk.W, padx=5, pady=5)
            
            for ing, percentage in recipe_data["ingredients"].items():
                ml_amount = (percentage / 100) * self.glass_size
                
                ml_ing_frame = ttk.Frame(ml_frame)
                ml_ing_frame.pack(fill=tk.X, padx=5, pady=2)
                
                ttk.Label(ml_ing_frame, text=f"{ing}:").pack(side=tk.LEFT, padx=5)
                ttk.Label(ml_ing_frame, text=f"{ml_amount:.1f}ml").pack(side=tk.LEFT, padx=5)
            
            # Save button
            save_btn = ttk.Button(recipe_frame, text="Rezept speichern", 
                                 command=lambda name=cocktail_name: self.save_recipe(name))
            save_btn.pack(pady=10)
        
        # Add save all button
        save_all_btn = ttk.Button(scrollable_frame, text="Alle Rezepte speichern", command=self.save_all_recipes)
        save_all_btn.pack(pady=10)
    
    def update_recipe_ingredient(self, cocktail_name, ingredient):
        """Update recipe ingredient when changed"""
        if cocktail_name in self.recipe_vars and ingredient in self.recipe_vars[cocktail_name]:
            percentage = self.recipe_vars[cocktail_name][ingredient].get()
            self.recipes[cocktail_name]["ingredients"][ingredient] = percentage
            self.save_data()
    
    def save_recipe(self, cocktail_name):
        """Save a specific recipe"""
        if cocktail_name in self.recipe_vars:
            # Validate percentages
            ingredients = {ing: var.get() for ing, var in self.recipe_vars[cocktail_name].items()}
            total = sum(ingredients.values())
            
            if abs(total - 100) < 0.1:  # Allow small rounding errors
                self.recipes[cocktail_name]["ingredients"] = ingredients
                self.save_data()
                messagebox.showinfo("Erfolg", f"Rezept für {cocktail_name} wurde gespeichert!")
            else:
                messagebox.showerror("Fehler", f"Die Summe der Prozente muss 100% ergeben! Aktuelle Summe: {total:.1f}%")
    
    def save_all_recipes(self):
        """Save all recipes"""
        for cocktail_name in self.recipe_vars:
            self.save_recipe(cocktail_name)
        messagebox.showinfo("Erfolg", "Alle Rezepte wurden gespeichert!")
    
    def delete_recipe(self, cocktail_name):
        """Delete a recipe"""
        if messagebox.askyesno("Bestätigung", f"Möchten Sie das Rezept für {cocktail_name} wirklich löschen?"):
            # Remove the cocktail's image file if it exists
            image_path = self.recipes[cocktail_name]["image"]
            try:
                if os.path.exists(image_path):
                    os.remove(image_path)
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Löschen des Bildes für {cocktail_name}: {e}")
            
            # Remove the cocktail from recipes
            del self.recipes[cocktail_name]
            self.save_data()
            
            # Refresh the recipes tab
            self.setup_recipes_tab(self.admin_frame.winfo_children()[0].select(2))
            messagebox.showinfo("Erfolg", f"Cocktail {cocktail_name} wurde gelöscht!")
    
    def setup_new_recipe_tab(self, parent):
        """Set up the new recipe tab"""
        # Title
        title_label = ttk.Label(parent, text="Neuen Cocktail hinzufügen", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Create form
        form_frame = ttk.Frame(parent)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Name input
        name_frame = ttk.Frame(form_frame)
        name_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(name_frame, text="Name des neuen Cocktails:").pack(side=tk.LEFT, padx=5)
        
        name_var = tk.StringVar()
        name_entry = ttk.Entry(name_frame, textvariable=name_var)
        name_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Image upload
        image_frame = ttk.Frame(form_frame)
        image_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(image_frame, text="Cocktail-Bild hochladen:").pack(side=tk.LEFT, padx=5)
        
        image_path_var = tk.StringVar()
        image_path_label = ttk.Label(image_frame, textvariable=image_path_var)
        image_path_label.pack(side=tk.LEFT, padx=5)
        
        def browse_image():
            file_path = filedialog.askopenfilename(
                title="Bild auswählen",
                filetypes=[("Image files", "*.jpg *.jpeg *.png")]
            )
            if file_path:
                image_path_var.set(file_path)
        
        browse_btn = ttk.Button(image_frame, text="Durchsuchen", command=browse_image)
        browse_btn.pack(side=tk.LEFT, padx=5)
        
        # Ingredients section
        ingredients_frame = ttk.LabelFrame(form_frame, text="Zutaten (in %):")
        ingredients_frame.pack(fill=tk.X, padx=5, pady=10)
        
        # Create widgets for each ingredient
        new_recipe_vars = {}
        for ingredient in self.ingredients.keys():
            ing_frame = ttk.Frame(ingredients_frame)
            ing_frame.pack(fill=tk.X, padx=5, pady=2)
            
            ttk.Label(ing_frame, text=f"{ingredient}:").pack(side=tk.LEFT, padx=5)
            
            var = tk.DoubleVar(value=0.0)
            new_recipe_vars[ingredient] = var
            
            spinbox = ttk.Spinbox(ing_frame, from_=0.0, to=100.0, increment=0.1, textvariable=var, width=10)
            spinbox.pack(side=tk.LEFT, padx=5)
        
        # Total percentage
        total_frame = ttk.Frame(form_frame)
        total_frame.pack(fill=tk.X, padx=5, pady=5)
        
        total_var = tk.StringVar(value="Gesamtsumme: 0.0%")
        total_label = ttk.Label(total_frame, textvariable=total_var)
        total_label.pack(side=tk.LEFT, padx=5)
        
        # Update total when any ingredient changes
        def update_total(*args):
            total = sum(var.get() for var in new_recipe_vars.values())
            total_var.set(f"Gesamtsumme: {total:.1f}%")
        
        for var in new_recipe_vars.values():
            var.trace_add("write", update_total)
        
        # ML amounts
        ml_frame = ttk.LabelFrame(form_frame, text="Mengen in ml (basierend auf Glasgröße):")
        ml_frame.pack(fill=tk.X, padx=5, pady=10)
        
        # Add button
        add_btn = ttk.Button(form_frame, text="Cocktail hinzufügen", 
                            command=lambda: self.add_new_recipe(name_var.get(), image_path_var.get(), new_recipe_vars))
        add_btn.pack(pady=10)
    
    def add_new_recipe(self, name, image_path, ingredient_vars):
        """Add a new recipe"""
        if not name:
            messagebox.showerror("Fehler", "Bitte geben Sie einen Namen ein!")
            return
        
        if not image_path:
            messagebox.showerror("Fehler", "Bitte wählen Sie ein Bild aus!")
            return
        
        # Get ingredients with percentage > 0
        ingredients = {ing: var.get() for ing, var in ingredient_vars.items() if var.get() > 0}
        
        if not ingredients:
            messagebox.showerror("Fehler", "Bitte fügen Sie mindestens eine Zutat hinzu!")
            return
        
        # Validate percentages
        total = sum(ingredients.values())
        if abs(total - 100) >= 0.1:  # Allow small rounding errors
            messagebox.showerror("Fehler", f"Die Summe der Prozente muss 100% ergeben! Aktuelle Summe: {total:.1f}%")
            return
        
        # Copy and resize image
        try:
            # Create filename
            file_extension = os.path.splitext(image_path)[1]
            file_name = f"{name.lower().replace(' ', '_')}{file_extension}"
            new_image_path = os.path.join(self.assets_dir, file_name)
            
            # Open and resize image
            img = Image.open(image_path)
            img = img.resize((700, 933), Image.Resampling.LANCZOS)
            
            # Save image
            img.save(new_image_path, format='JPEG', quality=95)
            
            # Add recipe
            self.recipes[name] = {
                "image": new_image_path,
                "glass_size": self.glass_size,
                "ingredients": ingredients
            }
            
            self.save_data()
            
            # Refresh the recipes tab and main tab
            self.setup_recipes_tab(self.admin_frame.winfo_children()[0].select(2))
            self.update_cocktail_grid()
            
            messagebox.showinfo("Erfolg", f"{name} wurde erfolgreich hinzugefügt!")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Verarbeiten des Bildes: {e}")
    
    def on_closing(self):
        """Handle window closing"""
        self.save_data()
        self.root.destroy()
    
    def run(self):
        """Run the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = MainWindow()
    app.run()
        