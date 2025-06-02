from recommander.file_extraction import FixedAutoIngredientExtractor

class Extractor:

    def __init__(self):
        self.extractor = FixedAutoIngredientExtractor()

    def extract_ingredients_fixed(self,user_input):
        """Fixed automated ingredient extraction"""
        result = self.extractor.process_input(user_input)
        return result['ingredients_only']
    
    def extract_with_quantities_fixed(self,user_input):
        """Fixed automated extraction with quantities"""
        result = self.extractor.process_input(user_input)
        return result['ingredients_with_units']
    
    def filter_good_ingredients(self,ingredients_list):
        # Define common valid ingredients (can be expanded)
        valid_ingredients = {
        'baking powder', 'sugar', 'salt', 'vanilla extract', 'eggs', 
        'flour', 'purpose flour', 'all purpose flour', 'cocoa powder', 
        'butter', 'brown sugar', 'white sugar', 'milk', 'oil', 
        'vegetable oil', 'olive oil', 'water', 'honey', 'cinnamon',
        'baking soda', 'yeast', 'cream', 'cheese', 'chocolate',
        'nuts', 'almonds', 'walnuts', 'pecans', 'raisins','yaourt'
        }
        # Filter criteria
        def is_valid_ingredient(ingredient):
            ingredient = ingredient.lower().strip()
            if len(ingredient) < 3:
                return False
            invalid_fragments = {
            'uns', 'all', 'unsweeten', 'cup', 'ies', 'unsal', 'alted', 
            'bak', 'brown', 'large', 'fud'}
            if ingredient in invalid_fragments:
                return False
            if len(ingredient) == 1 or ingredient.isdigit():
                return False
            units = {'cup', 'cups', 'tsp', 'tbsp', 'oz', 'lb', 'g', 'kg', 'ml', 'l'}
            if ingredient in units:
                return False
            if ingredient in valid_ingredients:
                return True
            ingredient_keywords = ['powder', 'extract', 'flour', 'sugar', 'oil', 'butter', 'milk']
            if any(keyword in ingredient for keyword in ingredient_keywords):
                return True
            if len(ingredient) >= 4 and ingredient.isalpha():
                return True
            return False
        filtered = [ing for ing in ingredients_list if is_valid_ingredient(ing)]
        seen = set()
        unique_filtered = []
        for ing in filtered:
            if ing.lower() not in seen:
                seen.add(ing.lower())
                unique_filtered.append(ing)
        return unique_filtered
    
    def __call__(self,recipe):
        ingredients = self.extract_ingredients_fixed(recipe)
        good_ingredients = self.filter_good_ingredients(ingredients)
        return list(set(map(lambda x : x.replace("▁",""),good_ingredients)))

