#!/usr/bin/env python
# coding: utf-8



from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification
import re
from textblob import TextBlob
import torch




class FixedAutoIngredientExtractor:
    def __init__(self):
        print("Loading models...")
        
        # Grammar correction model
        self.grammar_corrector = pipeline(
            "text2text-generation",
            model="vennify/t5-base-grammar-correction"
        )
        
        # Recipe-specific NER model with proper tokenizer handling
        self.recipe_tokenizer = AutoTokenizer.from_pretrained("edwardjross/xlm-roberta-base-finetuned-recipe-all")
        self.recipe_model = AutoModelForTokenClassification.from_pretrained("edwardjross/xlm-roberta-base-finetuned-recipe-all")
        
        # Food-specific NER model as backup
        self.food_ner = pipeline(
            "ner", 
            model="Dizex/InstaFoodRoBERTa-NER",
            aggregation_strategy="simple"
        )
        
        print("Models loaded successfully!")
    
    def correct_grammar(self, text):
        """Correct grammar using pre-trained model"""
        try:
            result = self.grammar_corrector(f"grammar: {text}", max_length=512)
            return result[0]['generated_text']
        except Exception as e:
            print(f"Grammar correction failed: {e}")
            return text
    
    def extract_with_recipe_model(self, text):
        """Extract using recipe model with proper token reconstruction"""
        try:
            # Tokenize the input
            inputs = self.recipe_tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
            
            # Get predictions
            with torch.no_grad():
                outputs = self.recipe_model(**inputs)
                predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
                predicted_token_class = predictions.argmax().item()
            
            # Get token predictions
            tokens = self.recipe_tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
            
            # Reconstruct ingredients from tokens
            ingredients = []
            current_ingredient = ""
            
            for i, token in enumerate(tokens):
                if token.startswith("##"):
                    # This is a continuation of the previous token
                    current_ingredient += token[2:]  # Remove ##
                elif token in ["<s>", "</s>", "<pad>"]:
                    # Skip special tokens
                    if current_ingredient.strip():
                        ingredients.append(current_ingredient.strip().lower())
                        current_ingredient = ""
                else:
                    # New token - save previous ingredient if exists
                    if current_ingredient.strip():
                        ingredients.append(current_ingredient.strip().lower())
                    current_ingredient = token
            
            # Add final ingredient
            if current_ingredient.strip():
                ingredients.append(current_ingredient.strip().lower())
            
            # Filter out non-food words
            food_ingredients = []
            for ingredient in ingredients:
                # Skip very short words and common non-food words
                if (len(ingredient) > 2 and 
                    ingredient not in ['the', 'and', 'or', 'in', 'to', 'for', 'with', 'make', 'add', 'mix', 'bake', 'cook']):
                    food_ingredients.append(ingredient)
            
            return list(set(food_ingredients))
            
        except Exception as e:
            print(f"Recipe model extraction failed: {e}")
            return []
    
    def extract_with_food_ner_fixed(self, text):
        """Extract using food NER with better token handling"""
        try:
            entities = self.food_ner(text)
            ingredients = []
            
            for entity in entities:
                if entity['score'] > 0.3:  # Lower threshold for more results
                    ingredient = entity['word'].strip()
                    
                    # Fix common tokenization issues
                    ingredient = re.sub(r'\s+##', '', ingredient)  # Remove ## with spaces
                    ingredient = re.sub(r'##\s*', '', ingredient)  # Remove ## 
                    ingredient = ingredient.replace('Ġ', ' ')  # Fix GPT-style spaces
                    ingredient = re.sub(r'\s+', ' ', ingredient)  # Fix multiple spaces
                    
                    # Clean and validate
                    ingredient = ingredient.lower().strip()
                    if (len(ingredient) > 2 and 
                        not ingredient.isdigit() and
                        ingredient not in ['the', 'and', 'or', 'in', 'to', 'for', 'with']):
                        ingredients.append(ingredient)
            
            return list(set(ingredients))
            
        except Exception as e:
            print(f"Food NER failed: {e}")
            return []
    
    def extract_fallback_regex(self, text):
        """Fallback regex extraction for anything the models missed"""
        ingredients = []
        
        # Look for patterns like "1 cup flour", "2 eggs", etc.
        pattern = r'(?:[½¼¾\d]+(?:\/\d+)?\s*(?:cup|cups|tbsp|tsp|tablespoon|teaspoon|oz|lb|gram|kg|liter|ml|piece|slice|clove|stick|large|medium|small)s?\s*(?:of\s+)?)([\w\s-]+?)(?=\s*[,\.\n;]|$)'
        
        matches = re.finditer(pattern, text, re.IGNORECASE)
        
        for match in matches:
            ingredient = match.group(1).strip().lower()
            # Basic cleaning
            ingredient = re.sub(r'\b(?:and|then|until|smooth|combined|evenly|completely)\b', '', ingredient)
            ingredient = re.sub(r'\s+', ' ', ingredient).strip()
            
            if len(ingredient) > 2:
                ingredients.append(ingredient)
        
        return ingredients
    
    def extract_quantities_improved(self, text, ingredients):
        """Extract quantities for found ingredients"""
        ingredients_with_units = []
        
        for ingredient in ingredients:
            # Look for quantity patterns before this ingredient
            # Handle fractions properly
            pattern = rf'([½¼¾\d]+(?:\/\d+)?\s*(?:cup|cups|tbsp|tsp|tablespoon|tablespoon|teaspoon|teaspoons|oz|ounce|ounces|lb|lbs|pound|pounds|gram|grams|kg|liter|ml|piece|pieces|slice|slices|stick|sticks|clove|cloves|large|medium|small)s?)\s*(?:of\s+)?.*?{re.escape(ingredient)}'
            
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                quantity = match.group(1).strip()
                ingredients_with_units.append(f"{quantity} {ingredient}")
            else:
                ingredients_with_units.append(ingredient)
        
        return ingredients_with_units
    
    def process_input(self, user_input):
        """Main processing function with fixed tokenization"""
        print("Correcting grammar...")
        corrected_text = self.correct_grammar(user_input)
        
        print("Extracting with recipe model...")
        recipe_ingredients = self.extract_with_recipe_model(corrected_text)
        
        print("Extracting with food NER...")  
        food_ingredients = self.extract_with_food_ner_fixed(corrected_text)
        
        print("Fallback regex extraction...")
        regex_ingredients = self.extract_fallback_regex(corrected_text)
        
        # Combine all results
        all_ingredients = list(set(recipe_ingredients + food_ingredients + regex_ingredients))
        
        # Final cleaning
        final_ingredients = []
        for ing in all_ingredients:
            # Remove very short or clearly non-food items
            if (len(ing) > 2 and 
                not ing.isdigit() and
                ing not in ['cup', 'cups', 'tbsp', 'tsp', 'the', 'and', 'or']):
                final_ingredients.append(ing)
        
        print("Extracting quantities...")
        ingredients_with_units = self.extract_quantities_improved(corrected_text, final_ingredients)
        
        return {
            'original_text': user_input,
            'corrected_text': corrected_text,
            'ingredients_only': final_ingredients,
            'ingredients_with_units': ingredients_with_units
        }







# # Global variable to hold the single instance of the extractor
# _extractor = None

# def get_extractor():
#     global _extractor
#     if _extractor is None:
#         _extractor = FixedAutoIngredientExtractor()  # Create the instance only once
#     return _extractor  # Return the same instance every time






def extract_ingredients_fixed(user_input):
    """Fixed automated ingredient extraction"""
    extractor = get_extractor()
    result = extractor.process_input(user_input)
    return result['ingredients_only']





def extract_with_quantities_fixed(user_input):
    """Fixed automated extraction with quantities"""
    extractor = get_extractor()
    result = extractor.process_input(user_input)
    return result['ingredients_with_units']





def filter_good_ingredients(ingredients_list):
    
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
            'bak', 'brown', 'large', 'fud'
        }
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






# if __name__ == "__main__":
#     brownie_recipe = "To make classic fudgy brownies, start by preheating your oven to 350°F (175°C) and greasing or lining an 8x8 inch baking pan. Melt ½ cup of unsalted butter, then stir in 1 cup of sugar, 2 large eggs, and 1 teaspoon of vanilla extract until smooth. In a separate bowl, mix ⅓ cup unsweetened cocoa powder, ½ cup all-purpose flour, ¼ teaspoon salt, and ¼ teaspoon baking powder. Gradually add the dry ingredients into the wet mixture and stir just until combined. If you like, fold in ½ cup of chopped nuts or chocolate chips. Pour the batter into the prepared pan, spread evenly, and bake for 20 to 25 minutes until a toothpick inserted in the center comes out with a few moist crumbs. Let the brownies cool completely before cutting into squares and enjoying!"
#     print("Testing automated extraction...")
#     ingredients = extract_ingredients_fixed(brownie_recipe)
#     print(f"Found ingredients: {ingredients}")

#     good_ingredients = filter_good_ingredients(ingredients)
#     print(f"Final ingredients: {good_ingredients}")



