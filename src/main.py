import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import threading
import time

class CocktailDisplayApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MixMasterX Cocktail Display")
        
        # Set window size to match Waveshare 4.3-inch display resolution
        self.root.geometry("800x430")
        self.root.resizable(False, False)
        
        # Configure the main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create a frame for the images
        self.images_frame = ttk.Frame(self.main_frame)
        self.images_frame.pack(fill=tk.BOTH, expand=True)
        
        # Dictionary to store name labels
        self.name_labels = {}
        
        # Load and display the images
        self.load_images()
        
    def load_images(self):
        # Get the path to the assets folder
        assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
        
        # List of image files
        image_files = ["gin_tonic.jpg", "wildberry_lillet.jpg", "aperol_spritz.jpg"]
        
        # Create a frame for each image
        for i, image_file in enumerate(image_files):
            image_path = os.path.join(assets_dir, image_file)
            
            # Load and resize the image
            img = Image.open(image_path)
            # Resize to fit in the display (approximately 250x250 each)
            img = img.resize((250, 250), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            
            # Create a label for the image
            img_label = ttk.Label(self.images_frame, image=photo)
            img_label.image = photo  # Keep a reference to prevent garbage collection
            img_label.grid(row=0, column=i, padx=5, pady=5)
            
            # Make the image clickable
            img_label.bind("<Button-1>", lambda event, idx=i: self.on_image_click(idx))
            
            # Add a label with the cocktail name
            cocktail_name = image_file.replace(".jpg", "").replace("_", " ").title()
            name_label = ttk.Label(self.images_frame, text=cocktail_name, font=("Arial", 12))
            name_label.grid(row=1, column=i, padx=5, pady=5)
            
            # Store the name label for later reference
            self.name_labels[i] = name_label
    
    def on_image_click(self, index):
        """Handle image click event"""
        # Get the name label for the clicked image
        name_label = self.name_labels[index]
        
        # Change the label color to green
        name_label.configure(foreground="green")
        
        # Start a thread to reset the color after 2 seconds
        threading.Thread(target=self.reset_label_color, args=(name_label,), daemon=True).start()
    
    def reset_label_color(self, label):
        """Reset the label color after 2 seconds"""
        time.sleep(2)
        # Use after() to safely update the UI from a non-main thread
        self.root.after(0, lambda: label.configure(foreground="white"))

if __name__ == "__main__":
    root = tk.Tk()
    app = CocktailDisplayApp(root)
    root.mainloop()
