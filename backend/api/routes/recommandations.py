from fastapi import APIRouter
from schemas.recipe import Recipe


route = APIRouter(
    prefix='/recommendations',
    tags=["recommendations"]
)



@route.post(status_code=200)
def recommand(recipe:Recipe):
    print(recipe)
    return {"message":"Hello World"}