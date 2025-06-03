from fastapi import APIRouter
from api.schemas.recipe import Recipe
from api.schemas.products  import Product
from typing import List
import api.controller.recommandation_final as controller
route = APIRouter(
    prefix='/recommendations',
    tags=["recommendations"]
)



@route.post('/',status_code=200,response_model=List[Product])
async def recommand(recipe:Recipe):
    return controller.recommand(recipe)