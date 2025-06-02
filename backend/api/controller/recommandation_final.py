
from recommander.Extractor import Extractor
from recommander.Recommandation import Recommandation
from schemas.recipe import Recipe
def recommand(recipe:Recipe):
    recipe = Extractor()(recipe.recipe)
    recommandation = Recommandation().recommand(recipe,1)
    return recommandation



# print(recommand("To make classic fudgy brownies, start by preheating your oven to 350°F (175°C) and greasing or lining an 8x8 inch baking pan. Melt ½ cup of unsalted butter, then stir in 1 cup of sugar, 2 large eggs, and 1 teaspoon of vanilla extract until smooth. In a separate bowl, mix ⅓ cup unsweetened cocoa powder, ½ cup all-purpose flour, ¼ teaspoon salt, and ¼ teaspoon baking powder. Gradually add the dry ingredients into the wet mixture and stir just until combined. If you like, fold in ½ cup of chopped nuts or chocolate chips. Pour the batter into the prepared pan, spread evenly, and bake for 20 to 25 minutes until a toothpick inserted in the center comes out with a few moist crumbs. Let the brownies cool completely before cutting into squares and enjoying!"))

