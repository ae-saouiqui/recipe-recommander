
from recommander.Extractor import Extractor
from recommander.Recommandation import Recommandation
from api.schemas.recipe import Recipe
from api.schemas.products import Product
from api.models.database import products_collection


def recommand(recipe:Recipe):
    recipe_list= Extractor()(recipe.recipe)
    ids= Recommandation(recipe.country).recommand(recipe_list,1)
    # ids = [1,43,54,6,65]
    cursor = products_collection.find({"id":{"$in":ids}})
    products = [Product(**product) for product in cursor]
    return products
