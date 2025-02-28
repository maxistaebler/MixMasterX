# MixMasterX - Smart Cocktail Mixer 🍹

MixMasterX is a Streamlit-based web application for managing and controlling an automated cocktail mixing system. The application consists of two main components: an admin interface for managing recipes and configurations, and a user interface for selecting and mixing cocktails.

## System Overview

The application is split into two main pages:
1. Main App (`1_🏠_APP.py`) - User interface for cocktail selection
2. Admin Panel (`pages/2_⚙️_ADMIN.py`) - Management interface for recipes and system configuration

### Main Features

- Recipe management with percentage-based ingredients
- Dynamic glass size adjustment
- Image-based cocktail selection
- Slot-based ingredient management
- Protected default recipes
- Real-time ml calculations based on glass size

## Admin Panel (2_⚙️_ADMIN.py)

The admin panel provides comprehensive management capabilities for the cocktail mixing system.

### 1. Glass Size Management
- Global glass size setting (100ml - 1000ml)
- Affects all cocktail recipes automatically
- Real-time ml calculations based on percentage values

### 2. Ingredient Management
- Configure available ingredients
- Assign pump slots (1-10) to ingredients
- Prevent duplicate slot assignments
- Add new ingredients with automatic slot validation

### 3. Recipe Management
- View and edit existing recipes
- Create new cocktails with:
  - Custom name
  - Ingredient percentages (must total 100%)
  - Automatic image resizing (700x933 pixels)
  - Real-time ml calculations
- Protected default recipes (cannot be deleted)
- Delete custom recipes

### Default Cocktails
The system comes with three pre-configured cocktails:
1. Aperol Spritz
   - Aperol (33%)
   - Secco (50%)
   - Mineralwasser (17%)

2. Wildberry Lillet
   - Lillet (40%)
   - Schweppes Raspberry (60%)

3. Gin Tonic
   - Gin (20%)
   - Tonic (80%)

## User Interface (1_🏠_APP.py)

The main app provides an intuitive interface for users to select and mix cocktails.

### Features
- Clean, grid-based layout
- Large cocktail images
- Centered cocktail names as buttons
- Recipe display showing:
  - Current glass size
  - Ingredient percentages
  - Calculated amounts in ml
- Success confirmation after selection

## Technical Details

### Image Management
- Automatic image resizing to 700x933 pixels
- JPG format with 95% quality
- Stored in local assets folder

### Recipe Storage
Recipes are stored with:
- Ingredient percentages
- Image paths
- Calculated ml values based on global glass size

### Slot System
- 10 available slots for ingredients
- One-to-one mapping of ingredients to pump slots
- Prevents double assignments

## Usage Example

1. Admin Setup:
   ```
   1. Set desired glass size (e.g., 400ml)
   2. Configure ingredients and their pump slots
   3. Create or modify cocktail recipes
   ```

2. User Selection:
   ```
   1. Browse available cocktails
   2. Click desired cocktail
   3. View recipe details (percentages and ml)
   4. Confirm selection
   ```

## Recipe Calculation Example

For a 400ml glass size and Gin Tonic recipe:
```json
{
    "Gin": {
        "percentage": "20.0%",
        "amount": "80.0ml"
    },
    "Tonic": {
        "percentage": "80.0%",
        "amount": "320.0ml"
    }
}
```

## Benefits of Percentage-Based Recipes

1. **Scalability**: Recipes automatically adjust to different glass sizes
2. **Consistency**: Maintains proper ratios regardless of volume
3. **Flexibility**: Easy to adjust and fine-tune recipes
4. **Validation**: Ensures ingredients always total 100%

## Installation

1. Clone the repository
2. Install requirements:
   ```bash
   pip install streamlit Pillow
   ```
3. Run the application:
   ```bash
   streamlit run 1_🏠_APP.py
   ```

## Dependencies

- Streamlit
- Pillow (PIL)
- Python 3.x

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Notes

- Default recipes are protected and cannot be deleted
- Images are automatically resized to maintain consistent layout
- All recipes must total exactly 100%
- Glass size affects all cocktails globally